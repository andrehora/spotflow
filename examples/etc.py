from happyflow.utils import obj_value, is_safe_iterator
import happyflow

class Foo:

    def bar(self):
        return

    def __str__(self):
        return "Oi"

s = (1, 2, 3, 4)

print(s[0])

# obj = is_safe_iterator(s)
# print(obj)