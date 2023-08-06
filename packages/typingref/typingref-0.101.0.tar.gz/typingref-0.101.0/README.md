![logo.png](docs%2Fassets%2Flogo.png)

*Introspect Python type annotation, with ease.*

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/nrbnlulu/typingref/tests.yml?style=for-the-badge)

Modern Python libraries often use type annotations,
this library is intended to help "de/serialize" Python type hints to something
you can work with.


### Sample Usage:

```python
from typingref import TypeHinter
from typing import Union

class MyType:
    ...

def foo(p: Union[int, str, float]) -> MyType:
    ...

p_type = TypeHinter.from_annotations(foo.__annotations__['p'])

if p_type.is_union():
    for t in p_type.of_type:
        ...

assert Union[int, str, float] == p_type.as_annotation()
```
