# SPDX-License-Identifier: BSD-2-Clause

from sys    import _getframe, version_info
from typing import Optional, Union

from opcode import opname

__all__ = (
	'get_src_loc',
	'get_var_name',
	'NameNotFound',
)

class NameNotFound(Exception):
	pass

_raise_exception = object()

def get_var_name(depth: int = 2, default: Optional[Union[str, object]] = _raise_exception) -> Union[str, object]:
	frame = _getframe(depth)
	code = frame.f_code
	call_index = frame.f_lasti
	while call_index > 0 and opname[code.co_code[call_index]] == 'CACHE':
		call_index -= 2
	while True:
		call_opc = opname[code.co_code[call_index]]
		if call_opc in ('EXTENDED_ARG',):
			call_index += 2
		else:
			break
	if call_opc not in ('CALL_FUNCTION', 'CALL_FUNCTION_KW', 'CALL_FUNCTION_EX', 'CALL_METHOD', 'CALL'):
		return default

	index = call_index + 2
	while True:
		opc = opname[code.co_code[index]]
		if opc in ('STORE_NAME', 'STORE_ATTR'):
			name_index = int(code.co_code[index + 1])
			return code.co_names[name_index]
		elif opc == 'STORE_FAST':
			name_index = int(code.co_code[index + 1])
			return code.co_varnames[name_index]
		elif opc == 'STORE_DEREF':
			name_index = int(code.co_code[index + 1])
			if version_info >= (3, 11):
				name_index -= code.co_nlocals
			return code.co_cellvars[name_index]
		elif opc in (
			'LOAD_GLOBAL', 'LOAD_NAME', 'LOAD_ATTR', 'LOAD_FAST',
			'LOAD_DEREF', 'DUP_TOP', 'BUILD_LIST', 'CACHE', 'COPY'
		):
			index += 2
		else:
			if default is _raise_exception:
				raise NameNotFound
			else:
				return default


def get_src_loc(src_loc_at: int = 0) -> tuple[str, int]:
	# n-th  frame: get_src_loc()
	# n-1th frame: caller of get_src_loc() (usually constructor)
	# n-2th frame: caller of caller (usually user code)
	frame = _getframe(2 + src_loc_at)
	return (frame.f_code.co_filename, frame.f_lineno)
