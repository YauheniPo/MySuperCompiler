import sys

from compiler.entities.nodes import CallExpression
from compiler.my_super_compiler import compiler

print(compiler('(add 2 (subtract 4 2))'))  # add(2, subtract(4, 2));

obj1 = CallExpression(name="name", params='params', callee='callee', arguments='arguments')

print("sys.getsizeof(obj1):", sys.getsizeof(obj1))


def dump(obj):
    for attr in dir(obj):
        print(" obj.%s = %r" % (attr, getattr(obj, attr)))


dump(obj1)

print(obj1.to_json())


def get_size(obj, seen=None):
    # From https://goshippo.com/blog/measure-real-size-any-python-object/
    # Recursively finds size of objects
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0

    # Important mark as seen before entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


print("get_size(obj1):", get_size(obj1))

