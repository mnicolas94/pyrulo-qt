# Pyrulo-qt
Qt widgets to load classes at runtime with [pyrulo](https://github.com/mnicolas94/pyrulo) python package.

# Installation
`pip install pyrulo-qt`

# Usage

Lets say we have the following scripts
```python
# base.py script

class Base:
  pass
```

```python
# a.py script
from base import Base

class A(Base):

  def __init__(self):
        self._a = 42

  def __str__(self):
        return "A"

```

```python
# b.py script
from base import Base

class B(Base):

  def __init__(self):
        self._b = "dwqwdqw"

  def __str__(self):
        return "B"

```

```python
# c.py script
from base import Base

class C(Base):

  def __init__(self):
        self._c = 0.2
        self._d = None

  def __str__(self):
        return "C"
```

`ConfigurableSelector` Qt widget can be used to select from the child classes of a base class and return an instance of the selected class.
```python
from base import Base
from pyrulo import class_imports
from pyrulo_qt.ui_configurable_selector import ConfigurableSelector

folder_dir = "."
class_imports.import_classes_in_dir(folder_dir, Base)  # first import the classes with pyrulo
selector = ConfigurableSelector(base_class=Base)  # Qt widget to select the child classes
```
The resulting widget looks like this
![example](docs/example.jpg)
