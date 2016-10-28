import os

from cffi import FFI

ffi = FFI()
ffi.set_source('rure._ffi', None)

cur_dir = os.path.dirname(os.path.abspath(__file__))
header_fname = os.path.join(cur_dir, "..", "include", "rure.h")
header_lines = open(header_fname).readlines()
header = []
for line in header_lines:
    # Strip lines known to break cdef
    if line.startswith(('}\n', '#ifdef', 'extern "C"', '#ifndef',
                        '#endif', '#define', '#include')):
        continue
    else:
        header.append(line)
ffi.cdef('\n'.join(header))

if __name__ == '__main__':
    ffi.compile(verbose=True)
