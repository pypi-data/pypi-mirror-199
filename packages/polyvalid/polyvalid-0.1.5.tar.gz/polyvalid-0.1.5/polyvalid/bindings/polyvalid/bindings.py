from abc import abstractmethod
from typing import Any, Callable, Tuple
import wasmer # type: ignore

try:
    from typing import Protocol
except ImportError:
    class Protocol: # type: ignore
        pass


def _encode_utf8(val: str, realloc: wasmer.Function, mem: wasmer.Memory) -> Tuple[int, int]:
    bytes = val.encode('utf8')
    ptr = realloc(0, 0, 1, len(bytes))
    assert(isinstance(ptr, int))
    ptr = ptr & 0xffffffff
    if ptr + len(bytes) > mem.data_size:
        raise IndexError('string out of bounds')
    view = mem.uint8_view()
    view[ptr:ptr+len(bytes)] = bytes
    return (ptr, len(bytes))
class Polyvalid:
    instance: wasmer.Instance
    _canonical_abi_realloc: wasmer.Function
    _is_name_valid: wasmer.Function
    _memory: wasmer.Memory
    def __init__(self, store: wasmer.Store, imports: dict[str, dict[str, Any]], module: wasmer.Module):
        self.instance = wasmer.Instance(module, imports)
        
        canonical_abi_realloc = self.instance.exports.__getattribute__('canonical_abi_realloc')
        assert(isinstance(canonical_abi_realloc, wasmer.Function))
        self._canonical_abi_realloc = canonical_abi_realloc
        
        is_name_valid = self.instance.exports.__getattribute__('is-name-valid')
        assert(isinstance(is_name_valid, wasmer.Function))
        self._is_name_valid = is_name_valid
        
        memory = self.instance.exports.__getattribute__('memory')
        assert(isinstance(memory, wasmer.Memory))
        self._memory = memory
    def is_name_valid(self, name: str) -> bool:
        memory = self._memory;
        realloc = self._canonical_abi_realloc
        ptr, len0 = _encode_utf8(name, realloc, memory)
        ret = self._is_name_valid(ptr, len0)
        assert(isinstance(ret, int))
        
        operand = ret
        if operand == 0:
            boolean = False
        elif operand == 1:
            boolean = True
        else:
            raise TypeError("invalid variant discriminant for bool")
        return boolean
