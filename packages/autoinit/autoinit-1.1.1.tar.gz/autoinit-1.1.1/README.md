![Tests Pypy](https://github.com/oversider-kosma/autoinit/actions/workflows/pylint.yml/badge.svg?branch=master)
![Tests CPython](https://github.com/oversider-kosma/autoinit/actions/workflows/test_cpython.yml/badge.svg?branch=master)
![Tests Pypy](https://github.com/oversider-kosma/autoinit/actions/workflows/test_pypy.yml/badge.svg?branch=master)

# autoinit
> Python decorator for automatic initialization instance attributes

### What
```python3
import autoinit  # same as `from autoinit import autoinit`

@autoinit
class X:
    def __init__(self, a, b, c, d:int, e=99.99, f='some_default_value'):
	    print("__init__ do some another things")

x = X(42, 100, 500, None)
#  Output: "__init__ do some another things"

print(x.__dict__)
# Output: {'a': 42, 'b': 100, 'c': 500, 'd': None, 'e': 99.99, 'f': 'some_default_value'}
```

### How
$ ```pip install autoinit```
### Where
Tested in:
* CPython: 2.7, 3.5-3.11
* Pypy: 2.7, 3.5-3.9
* Jython: 2.7


...but with a high probability will work with other implementations as well.

### Why
A lot of elementary assignments inside `__init__` are a fairly frequent and rather dull case.

```python3
class FiveDimensionRecord:
    def __init__(self, x:int, y:int, z:int, u:int,
                 v:int, dt:typing.Optional[datetime]=None, description:str=''):
        self.x = x
        self.y = y
        self.z = z
        self.u = u
        self.v = v
        self.dt = dt or datetime.now()
        self.description = description
```

Dataclasses do not make it much more fun, mainly because you still cannot declare attributes in one line
```python3
@dataclass
class FiveDimensionRecord:
    x: int
    y: int
    z: int
    u: int
    v: int
    dt: 'typing.Any' = None
    description: str = ''

    def __post_init__(self):
        self.dt = self.dt or datetime.now()
```

With `autoinit` it looks much more compact and minimalistic

```python3
class FiveDimensionRecord:
    @autoinit
    def __init__(self, x:int, y:int, z:int,
                 u:int, v:int, dt=None, description:str=''):
        self.dt = self.dt or datetime.now()
```

### Options
* `@autoinit(exclude='attr')` or `@autoinit(exclude=['attr1', 'attr2]')`: skip specified attributes. Default: `[]`

* `@autoinit(no_warn=True)`: do not throw warning if decorator applied to non-`__init__` method. Default: `False`.

* `@autoinit(reverse=True)`: invert the order of actions - first call the wrapped method (which is usually `__init__`), and then do assignment. Default: `False`.

The decorator itself can be equally applied to both the `__init__` method and the entire class.
