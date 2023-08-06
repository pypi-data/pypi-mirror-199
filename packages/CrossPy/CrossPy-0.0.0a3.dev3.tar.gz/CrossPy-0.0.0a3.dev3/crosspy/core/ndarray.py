import numpy
import cupy

from typing import Optional, Tuple, Union, Iterable, Sequence
from collections import defaultdict
from contextlib import nullcontext
from ..device import Device, cpu
from ..array import ArrayType, register_array_type, get_array_module

__all__ = ['CrossPyArray', 'BasicIndexType', 'IndexType']

import logging
logger = logging.getLogger(__name__)

BasicIndexType = Union[int, slice, Iterable[int]]  # non-recursive
IndexType = Union[BasicIndexType, Tuple[BasicIndexType, ...]]  # recursive

ShapeType=Union[Tuple[()], Tuple[int, ...]]

def normalize_slice(slice_: slice, len_: int):
    def _wrap_to_positive(i: int):
        return i and (i + len_ if i < 0 else i)
    return slice(_wrap_to_positive(slice_.start) or 0, _wrap_to_positive(slice_.stop) or len_, slice_.step or 1)

def shape_of_slice(normalized_slice_: slice):
    """Assume normalized slice"""
    return (normalized_slice_.stop - normalized_slice_.start) // normalized_slice_.step


def _local_assignment(target, local_indices, source, source_indices: Optional[tuple]=None):
    if source_indices is None:
        src = source
    else:
        src = source[tuple(source_indices)
                        ] if len(source_indices) else source.item()
    if hasattr(target, 'device'):  # target is cupy array
        if isinstance(src, self.__class__):
            src = src.all_to(target.device)
        with target.device:
            target[tuple(local_indices)] = cupy.asarray(src)
    elif hasattr(source, 'devices'): # ??? <= crosspy
        mapping = source.plan_index_mapping(source_indices, local_indices)
        for t, s in mapping:
            target[tuple(t)] = cupy.asnumpy(s)
    elif hasattr(source, 'device'):  # numpy <= cupy
        target[tuple(local_indices)] = cupy.asnumpy(src)
    else:  # numpy <= numpy
        target[tuple(local_indices)] = src

def dim_to_concat(shapes, expected) -> Optional[int]:
    def are_all_values_same(l):
        return len(set(l)) == 1
    # a boolean list of size # dimensions, true for dimension where all parts share same size
    is_same_size_mask = [are_all_values_same(d) for d in zip(*shapes)]
    if len(is_same_size_mask) == 0:  # all scalars
        return None
    
    if all(is_same_size_mask):  # can be concat by any dim
        if expected is None:
            logger.info("Concat dim not specified; use 0 by default") # TODO should do nothing
            return 0
        return expected

    def all_except_one(bool_array):
        return sum(bool_array) == len(bool_array) - 1
    if all_except_one(is_same_size_mask):
        _dim = is_same_size_mask.index(False)
        if expected is not None and expected != _dim:
            raise ValueError(
                "Cannot concat on dim %s, but %s is feasible" %
                (expected, _dim)
            )
        return _dim

    raise ValueError(
        "Incompatible shapes with %s different dims" % (len(is_same_size_mask) - sum(is_same_size_mask))
    )

HANDLED_FUNCTIONS = {}


def implements(np_function):
    "Register an __array_function__ implementation."
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func

    return decorator

class CrossPyArray(numpy.lib.mixins.NDArrayOperatorsMixin):
    """
    Heterougeneous N-dimensional array compatible with the numpy API with custom implementations of numpy functionality.

    https://numpy.org/doc/stable/user/basics.dispatch.html#basics-dispatch
    """
    def __init__(self, obj, dim: Optional[int] = None, shape = None) -> None:
        # super().__init__()
        self._original_data = obj

        if not isinstance(obj, (list, tuple)):
            assert dim is None, "assumption: no concat for non-list objs"
            self._shape = getattr(obj, 'shape')
            return
        
        list_obj = obj
        try:
            shapes: tuple[ShapeType, ...] = tuple(a.shape for a in list_obj)
        except AttributeError:
            raise AttributeError("Arrays are required to have 'shape'")
            # TODO: __len__?

        assert len(shapes) > 0, NotImplementedError("array with no values not supported")

        self._shapes = shapes
        self._bounds = numpy.cumsum(shapes)

        # Check concatenation dimension
        if len(shapes) == 1:
            assert dim is None, "no concat for a single obj; check self._original_data"
            self._concat_dim = None
        else:
            self._concat_dim = dim and dim_to_concat(shapes, dim)

        self._shape = getattr(self._original_data, 'shape', self._init_shape(shapes))

        self._lazy_movement = defaultdict(list)

        # legacy
        self._distr_dims = [dim]

    def _init_shape(self, shapes: Sequence[ShapeType]) -> ShapeType:
        """
        :param shapes: shapes of each subarray
        :return: shape of the aggregated array
        """
        if len(shapes) == 1:
            return shapes[0]
        if not all([len(s) == len(shapes[0]) for s in shapes[1:]]):
            # TODO: optionally add 1 dimension to align
            raise ValueError("Array dimensions mismatch")
        logger.debug(shapes)

        logger.debug("Concat over dim ", self._concat_dim)
        if self._concat_dim is None:  # scalar
            final_shape: ShapeType = (len(shapes),) # TODO general dim lift
        else:
            # merge shapes
            shape = list(shapes[0])
            shape[self._concat_dim] = sum([s[self._concat_dim] for s in shapes])
            final_shape: ShapeType = tuple(shape)
        return final_shape

    @property
    def data_map(self):
        """
        :param shapes: 
        """
        if len(self._shapes) == 1:
            key = tuple([(0, s) for s in self._shapes[0]])
            array = self._original_data[0]  # TODO: for array in array_list; or zip
            logger.debug(type(array))
            return {key: array}

        def map_index_to_array(num_blocks, final_shape, concat_dim):
            array_map = {}
            offsets = [
                0 for _ in range(len(final_shape))
            ]  # TODO topological concat
            # TODO flatten crosspy array
            for ai in range(num_blocks):
                array = self._original_data[ai]  # TODO: for array in array_list; or zip
                logger.debug(type(array))
                key = list(array.shape)  # list[int]
                if len(offsets) > 0 and len(key) == 0:
                    key = [1,] # TODO general dim lift
                for i in range(len(offsets)):
                    key[i] = (
                        offsets[i], offsets[i] + key[i]
                    )  # gradually to list[tuple[int, int]]
                    if i == concat_dim:
                        offsets[i] = key[i][1]
                key = tuple(key)  # tuple[tuple[int, int]]
                array_map[key] = array
            return array_map
        array_map = map_index_to_array(len(self._shapes), self._shape, self._concat_dim)
        return array_map

    # @classmethod
    # def from_shapes(cls, shapes: Sequence[ShapeType], block_gen, dim=None) -> 'CrossPyArray':
    #     """
    #     :param block_gen: i -> array
    #     """
    #     return CrossPyArray(*init_from_shapes_builder(shapes, block_gen, dim=dim))

    @property
    def distributed_dims(self) -> list[int]:
        return self._distr_dims

    @property
    def nparts(self) -> int:
        return len(self.data_map)

    @property
    def shape(self) -> tuple[int, ...]:
        return tuple(self._shape)
    
    @property
    def boundaries(self):
        return self._bounds

    @property
    def device_map(self):
        return {
            k: getattr(v, 'device', 'cpu')
            for k, v in self.data_map.items()
        }

    @property
    def device(self) -> list:
        return [getattr(x, 'device', -1) for x in self._original_data]
    
    def block_at(self, i: int):
        loc = self._global_index_to_block_id(i)
        return self._original_data[loc]

    def device_at(self, i: int):
        return getattr(self.block_at(i), 'device', -1)

    @property
    def type_map(self):
        return {k: type(v) for k, v in self.data_map.items()}

    def to_dict(self):
        return self.data_map

    def values(self):
        return list(self.data_map.values())

    def keys(self):
        return list(self.data_map.keys())

    def item(self):
        if self._shape != ():
            raise IndexError("cannot get item from non-scalars")
        return self.data_map.get(())

    def __len__(self) -> int:
        return self.shape[0]

    def __repr__(self) -> str:
        return str("array %s" % self.data_map)

    def debug_print(self):
        print(str("CrossPy array of shape %s\nData: %s\nMapping: %s" % (self._shape, self._original_data, self.data_map)))

    def _index_intersection(
        self, part_range: tuple[int, int], target: BasicIndexType
    ) -> Union[BasicIndexType, None]:
        '''On one dimension, given the source range and target index, return

        TODO move to utils
        '''
        l, r = part_range
        if isinstance(
            target, int
        ) and l <= target < r:  # TODO negative indexing
            return (target - l)  # global to local
        elif isinstance(target, Iterable):
            in_range = [
                (i - l) for i in target if l <= i < r
            ]  # TODO negative indexing
            return in_range if len(in_range) else None
        elif isinstance(target, slice):
            # trivial case: target == part_range
            if target.start in (None, l) and target.stop in (None, r) and target.step in (None, 1):
                return slice(0, r-l)
            # trivial case: target and part_range are not overlapped
            if target.start and r <= target.start or target.stop and target.stop <= l:
                return None
            # long path
            new_start = None
            new_stop = None
            for i in range(
                target.start or 0, target.stop or r, target.step or 1
            ):
                if new_start is None and l <= i:
                    new_start = i
                if i < r:
                    new_stop = i + 1
            return slice(
                new_start - l, new_stop -
                l if new_stop is not None else None, target.step
            ) if new_start is not None else None
        elif isinstance(target, self.__class__):
            return target.to_dict()[((l, r),)] # TODO handle general bool mask
        return None

    def _global_index_to_block_id(self, i: int):
        """
        Computes which block the referred element resides in
        """
        # TODO: numpy batch version
        return numpy.sum(i >= self._bounds)
    
    def _indexing_check(self, index: IndexType):
        """Check before set and get item"""
        if self._shape == ():
            raise IndexError("scalar is not subscriptable")
        
        assert isinstance(index, (int, slice)) or isinstance(index, list) and all(isinstance(i, int) for i in index), NotImplementedError("Only support 1-D indexing")
        
        if isinstance(index, slice):
            index = normalize_slice(index, len(self))

        # unify the form to list of slices
        if not isinstance(index, tuple):
            index = (index, )

        # allow optional ellipsis [d0, d1, ...]
        if len(index) - len(self.shape) == 1 and index[-1] is Ellipsis:
            index = index[:-1]

        return index
    
    def _LEGACY_SLOW_check_index(self, index: Tuple[BasicIndexType]):
        def _meta_check(target, max):
            if isinstance(target,
                          int) and (0 <= target < max or 0 > target >= -max):
                return True
            elif isinstance(target, Iterable):
                return all([(0 <= i < max or 0 > i >= -max) for i in target])
            elif isinstance(target, slice):
                return all(
                    [
                        i < max for i in range(
                            target.start or 0, target.stop or max,
                            target.step or 1
                        )
                    ]
                )
            raise TypeError("index out of range", target, "vs", max)

        if not all(
            [_meta_check(i, self._shape[d]) for d, i in enumerate(index)]
        ):
            raise TypeError("index out of range")

    def __getitem__(self, index: IndexType):  # -> Union[Array, List[Array]]
        """
        Note
            CuPy handles out-of-bounds indices differently from NumPy: NumPy
            handles them by raising an error, but CuPy wraps them around.
            We currently raise an error.
        """
        index = self._indexing_check(index)

        if len(self._lazy_movement):
            raise NotImplementedError("implementing movement operator...")
            self._lazy_movement = defaultdict(list)
        
        # FIXME: ad hoc, should deal with negative indices
        if self._concat_dim == 0 and index == (-1,):
            return self._original_data[-1][-1]

        # FIXME: ad hoc for 1-D
        if self._concat_dim == 0 and len(index) == 1:
            if isinstance(index[0], slice):
                slice_ = index[0]
                left = self._global_index_to_block_id(slice_.start)
                right = self._global_index_to_block_id(slice_.stop)
                # right is not on boundary -> trailing partial block
                relevant_blocks = self._original_data[left:right + 1 if slice_.stop not in self._bounds else right]
                assert len(relevant_blocks), "Invalid slicing: empty array not supported yet"

                assert slice_.step in [None, 1], NotImplementedError("stepping not implemented")
                # trimming
                head_start, tail_stop = None, None
                if slice_.start > 0 and slice_.start not in self._bounds:
                    head_start = slice_.start - self._bounds[left - 1] if left > 0 else slice_.start
                if slice_.stop < len(self) and slice_.stop not in self._bounds:
                    tail_stop = slice_.stop - self._bounds[right - 1] if right > 0 else slice_.stop

                if len(relevant_blocks) == 1:
                    if head_start or tail_stop:
                        relevant_blocks[0] = relevant_blocks[0][head_start:tail_stop]
                    return CrossPyArray(relevant_blocks, dim = None)
                
                if head_start:
                    relevant_blocks[0] = relevant_blocks[0][head_start:]
                if tail_stop:
                    relevant_blocks[-1] = relevant_blocks[-1][:tail_stop]
                return CrossPyArray(relevant_blocks, dim = self._concat_dim)
            if isinstance(index[0], int):
                int_ = index[0]
                loc = self._global_index_to_block_id(int_)
                return CrossPyArray(self._original_data[loc][int_ - self._bounds[loc - 1] if loc > 0 else int_], dim = None)
            if isinstance(index[0], list):
                list_ = index[0]
                block_ids = [self._global_index_to_block_id(i) for i in list_]
                bounds = numpy.diff(block_ids, append=-1).nonzero()[0] + 1
                assert bounds[-1] == len(block_ids) == len(list_)
                obj = []
                left = 0
                for right in bounds:
                    # TODO lazy
                    block = self._original_data[block_ids[left]]
                    with getattr(block, 'device', nullcontext()):
                        obj.append(block[list_[left:right]])
                    left = right
                if len(obj) == 1:
                    return CrossPyArray(obj[0], dim=None)
                return CrossPyArray(obj, dim=0)
            raise NotImplementedError("this way of indexing is not supported")
        raise NotImplementedError("Only implemented for 1-D")

        # def _parse_bool_mask(mask):
        #     # assume mask is 1-D
        #     assert len(mask.shape) == 1
        #     return [i for i in range(mask.shape[0]) if mask[i].item()]
        # index = [(_parse_bool_mask(i) if isinstance(i, self.__class__) else i) for i in index]

        # 1. build a new index to data mapping
        # 2. build a new index to device mapping
        # ret = []
        # for k, v in self._index_to_data.items():
        #     local_indices = [
        #         self._index_intersection(
        #             k[d], i if i is not Ellipsis else slice(None)
        #         ) for d, i in enumerate(index)
        #     ]
        #     if all([i is not None for i in local_indices]):
        #         try:
        #             with v.device:
        #                 ret.append(v[tuple(local_indices)])
        #         except:
        #             ret.append(v[tuple(local_indices)])
        # # TODO check out of range in advance
        # if len(ret) == 0:
        #     raise IndexError("Index out of range")
        # # FIXME: shape may change!!!
        # return CrossPyArray.from_array_list(ret)

    def __setitem__(self, index: IndexType, value):
        """
        Assign :param:`value` to a partition which may not on the current device.

        :param index: index of the target partition(s)

        .. todo:
            Assignment of different values to multiple partitions (ndarrays) are currently NOT supported. The :param:`value` is assigned as a whole to each of the target partition(s).
        """
        index = self._indexing_check(index)

        if self._concat_dim == 0 and len(index) == 1:
            if isinstance(index[0], slice):
                slice_ = index[0]
                # check shape
                assert shape_of_slice(index[0]) == len(value), "shape mismatch; broadcasting not implemented"
                assert slice_.step in [None, 1], NotImplementedError("stepping not implemented")

                assert isinstance(value, CrossPyArray), "TODO: np/cp arrays"
                external_bounds = value.boundaries
                assert slice_.start + external_bounds[-1] == slice_.stop
                interal_bounds = self._bounds[self._bounds > slice_.start] - slice_.start
                bounds = numpy.unique(numpy.concatenate((external_bounds, interal_bounds)))
                bounds = bounds[bounds <= external_bounds[-1]]
                source_global_start = 0
                for source_global_stop in bounds:
                    source_obj, source_local_slice = value._locate(slice(source_global_start, source_global_stop))
                    target_obj, target_local_slice = self._locate(slice(slice_.start + source_global_start, slice_.start + source_global_stop))
                    from_device = getattr(source_obj, 'device', -1)
                    to_device = getattr(target_obj, 'device', -1)
                    if from_device == to_device:
                        target_obj[target_local_slice] = source_obj[source_local_slice]
                    else:
                        self._lazy_movement[(from_device, to_device)].append((source_obj, source_local_slice, target_obj, target_local_slice))
                    source_global_start = source_global_stop
                return
            elif isinstance(index[0], int):
                int_ = index[0]
                loc = self._global_index_to_block_id(int_)
                self._original_data[loc][int_ - self._bounds[loc - 1] if loc > 0 else int_] = value

        return

        # TODO set is much slower than get

        if self.nparts == 1: # short path
            _local_assignment(self.values()[0], index, value)
            return

        # propagate trivial slice (:)
        if index[0] == slice(None) and isinstance(value, self.__class__) and all(
            ok == ik[:len(ok)] for ok,ik in zip(value.keys(), self.keys())
        ):
            # TODO assuming keys/values ordered
            for src,dst in zip(value.values(), self.values()):
                _local_assignment(dst, index, src)
            return

        def _target_shape(index, caps: list[int]):
            """
            :return: The shape of target region defined by index
            """
            def _per_dim_size(target: BasicIndexType, max: int):
                if isinstance(target, int):
                    return 1
                elif isinstance(target, Iterable):
                    try:
                        return len(target) # len might not be available
                    except:
                        try:
                            return target.shape[0]
                        except:
                            # TODO slow!
                            return sum(
                                [1 for _ in target]
                            )
                elif isinstance(target, slice):
                    if target.step in (None, 1):
                        return (target.stop or max) - (target.start or 0)
                    # TODO slow
                    return sum(
                        [
                            1 for _ in range(
                                target.start or 0, target.stop or max,
                                target.step or 1
                            )
                        ]
                    )
                raise TypeError("unknown index type")

            return [_per_dim_size(i, caps[d]) for d, i in enumerate(index)]

        source_shape_start = [0 for _ in range(len(value.shape))]
        for k, v in self.data_map.items():
            local_indices = [
                self._index_intersection(k[d], i) for d, i in enumerate(index)
            ]
            if all([i is not None for i in local_indices]):
                target_shape = _target_shape(local_indices, [r[1] for r in k])
                for i in range(len(target_shape), len(k)):
                    target_shape.append(k[i][1] - k[i][0]) # fill up remaining dims
                target_shape = [x for x in target_shape if x > 1] # squeeze
                assert len(target_shape) == len(value.shape)
                source_shape_end = [
                    a + b for a, b in
                    zip(source_shape_start, target_shape)
                ]
                source_indices = [
                    slice(source_global_start, source_global_stop) for source_global_start, source_global_stop in
                    zip(source_shape_start, source_shape_end)
                ]
                source_shape_start = source_shape_end
                _local_assignment(v, local_indices, value, source_indices)

    def _locate(self, global_slice: slice):
        """
        Returns block id and block-local slice. Assume the slice is NOT crossing blocks.
        """
        block_id = self._global_index_to_block_id(global_slice.start)
        # TODO check assumption
        obj = self._original_data[block_id]
        l2g_offset = self._bounds[block_id - 1] if block_id > 0 else 0
        local_start = global_slice.start - l2g_offset
        local_stop = global_slice.stop - l2g_offset
        return obj, slice(local_start, local_stop, global_slice.step)

    def plan_index_mapping(self, my_indices, other_indices):
        mapping = []
        other_start = [other_indices[d].start for d in range(len(other_indices))]
        for k, v in self.data_map.items():
            local_indices = [
                self._index_intersection(k[d], i)
                for d, i in enumerate(my_indices)
            ]
            other_end = [
                a + b for a, b in zip(other_start, v[local_indices].shape)
            ]
            other_index = [
                slice(start, stop)
                for start, stop in zip(other_start, other_end)
            ]
            mapping.append((other_index, v[local_indices]))
            other_start = other_end
        return mapping

    # TODO unify attr
    def sum(self, axis=None, *args, **kwargs):
        # TODO: assuming 1-D
        new_map = {}
        v0 = None
        vv = None
        reduce = axis in self.distributed_dims or axis is None
        # TODO axis=None
        for k,v in self.data_map.items():
            try:
                with v.device:
                    if reduce and vv is not None:
                        v0 = get_array_module(vv).asarray(vv)
                    vv = get_array_module(v).sum(v, axis=axis)
                    if reduce and v0 is not None:
                        vv += v0
            except:
                if reduce and vv is not None:
                    v0 = get_array_module(vv).asarray(vv)
                vv = get_array_module(v).sum(v, axis=axis)
                if reduce and v0 is not None:
                    vv += v0
            new_map[k] = vv
        return CrossPyArray.from_array_list([vv] if reduce else list(new_map.values()))

    # TODO unify attr
    def argmin(self, axis=None, *args, **kwargs):
        new_map = {}
        for k,v in self.data_map.items():
            try:
                with v.device:
                    vv = get_array_module(v).argmin(v, axis=axis)
            except:
                vv = get_array_module(v).argmin(v, axis=axis)
            new_map[k] = vv
        return CrossPyArray.from_array_list(list(new_map.values()))

    def to(self, placement):
        if isinstance(placement, Iterable):
            return self._to_multidevice(placement)
        else:
            return self.all_to(placement)

    def _to_multidevice(self, placement):
        from ..ldevice import LDeviceSequenceBlocked
        Partitioner = LDeviceSequenceBlocked
        mapper = Partitioner(len(placement), placement=placement)
        arr_p = mapper.partition_tensor(self)
        return CrossPyArray.from_array_list(arr_p)

    def all_to(self, device):
        def _aggregate(concat, pull_op):
            output = None
            # ad hoc
            if not isinstance(self._original_data, list):
                return pull_op(self._original_data)
            output = concat([pull_op(x) for x in self._original_data])
            # legacy
            # for k, v in sorted(self._index_to_data.items()):
            #     pulled = pull_op(v)
            #     if output is None:
            #         output = pulled
            #     else:
            #         diff_dim = -1
            #         shape = [(0, s) for s in output.shape]
            #         assert len(shape) == len(k)
            #         for i, (range1, range2) in enumerate(zip(shape, k)):
            #             if range1 != range2:
            #                 diff_dim = i
            #                 break
            #         output = concat((output, pulled), axis=diff_dim)
            return output

        if (
            isinstance(device, Device) and
            device.__class__.__name__ == "_CPUDevice"
        ) or (isinstance(device, int) and device < 0):
            return _aggregate(numpy.concatenate, cupy.asnumpy)

        try:
            device = getattr(device, "cupy_device")
        except AttributeError:
            device = cupy.cuda.Device(device)
        with device:
            return _aggregate(cupy.concatenate, cupy.asarray)

    def __array__(self, dtype=None):
        """
        `numpy.array` or `numpy.asarray` that converts this array to a numpy array
        will call this __array__ method to obtain a standard numpy.ndarray.
        """
        logger.debug("ALL TO CPU!")
        return self.all_to(-1)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        """
        :param ufunc:   A function like numpy.multiply
        :param method:  A string, differentiating between numpy.multiply(...) and
                        variants like numpy.multiply.outer, numpy.multiply.accumulate,
                        and so on. For the common case, numpy.multiply(...), method == '__call__'.
        :param inputs:  A mixture of different types
        :param kwargs:  Keyword arguments passed to the function
        """
        # One might also consider adding the built-in list type to this
        # list, to support operations like np.add(array_like, list)
        _HANDLED_TYPES = (numpy.ndarray, Number, cupy._core.core.ndarray)
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, _HANDLED_TYPES + (CrossPyArray, )):
                logger.debug("not handling", type(x))
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        # inputs = tuple(x.values() if isinstance(x, CrossPyArray) else x
        #                for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.values() if isinstance(x, CrossPyArray) else x for x in out
            )

        if method == '__call__':
            unwrapped_inputs = []
            last_mapping = None
            for input in inputs:
                if isinstance(input, Number):
                    unwrapped_inputs.append([input])
                elif isinstance(input, self.__class__):
                    try:
                        unwrapped_inputs.append(input.values())
                    except:
                        unwrapped_inputs.append(numpy.asarray(input))
                    this_mapping = input.keys()
                    if last_mapping is None or last_mapping == [()]:
                        last_mapping = this_mapping
                    if this_mapping != [()] and not (
                        this_mapping == last_mapping or all(r in n for m in this_mapping for r in m for n in last_mapping)):
                        raise TypeError("inconsistent mappings not supported")
                else:
                    return NotImplemented
            # broadcast inputs
            if last_mapping is not None:
                for input in unwrapped_inputs:
                    while len(input) < len(last_mapping):
                        input.append(input[0]) # often just 2 inputs
                assert all(len(unwrapped_inputs[0]) == len(i) for i in unwrapped_inputs[1:])
            # result = getattr(ufunc, method)(*inputs, **kwargs)
            result = []
            for fine_inputs in zip(*unwrapped_inputs):
                has_device = [hasattr(i, 'device') for i in fine_inputs]
                if any(has_device):
                    with fine_inputs[has_device.index(True)].device: # on lhs device by default
                        fine_inputs = [cupy.asarray(i) for i in fine_inputs]
                        fine_result = getattr(ufunc,
                        method)(*fine_inputs, **kwargs)
                else:
                    fine_result = getattr(ufunc,
                        method)(*fine_inputs, **kwargs)
                result.append(fine_result)

            if type(result) is tuple:
                # multiple return values
                return tuple(type(self).from_array_list(x) for x in result)
            elif method == 'at':
                # no return value
                return None
            else:
                # one return value
                return type(self).from_array_list(result)  # self.__class__(result)
        else:
            raise NotImplementedError(method)
        return NotImplemented

    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            return NotImplemented
        # Note: this allows subclasses that don't override
        # __array_function__ to handle DiagonalArray objects.
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    def block_view(self):
        # FIXME: it assumes list of arrays
        return self._original_data

    @property
    def blockview(self):
        return CrossPyArray.BlockView(self)

    class BlockView:
        def __init__(self, xpa: 'CrossPyArray'):
            self.array = xpa

        def __getitem__(self, index):
            assert index >= 0, "Negative index not supported"
            # very ad hoc; assuming ordered keys
            dview = self.array.to_dict()
            for k in dview:
                if index == 0:
                    return dview[k]
                index -= 1
            raise Exception("Oops, it's so fragile right now...")

@implements(numpy.sum)
def _sum(a, axis=None):
    "Implementation of np.sum for CrossPyArray objects"
    return a.sum(axis)


class _CrossPyArrayType(ArrayType):
    def can_assign_from(self, a, b):
        # TODO: We should be able to do direct copies from numpy to cupy arrays, but it doesn't seem to be working.
        # return isinstance(b, (cupy.ndarray, numpy.ndarray))
        raise NotImplementedError
        return isinstance(b, _Array)

    def get_memory(self, a):
        raise NotImplementedError
        return gpu(a.device.id).memory()

    def get_array_module(self, a):
        import sys
        return sys.modules[__name__]


register_array_type(CrossPyArray)(_CrossPyArrayType())
