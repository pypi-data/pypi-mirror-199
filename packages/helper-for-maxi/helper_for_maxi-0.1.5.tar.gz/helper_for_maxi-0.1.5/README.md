# Helper for Maxi

All the Functions I could need multiple times

## Instructions

1. Install:

```
pip install helper-for-maxi
```

2. Import package:

```python
from helper import *
OR
import helper
helper.*
# You can replace * with what you need!
``` 

## Currently Implemented Classes / Functions

AppendClipboard()
```python
import helper
helper.AppendClipboard(text: str)

OR

from helper import AppendClipboard
AppendClipboard(text: str)

# copies text
#
# Copies / Appends the given text to the windows clipboard using the utf-8 encoding
#
# Parameters
# ----------
# text: str
#     The text that is copied / appended to the clipboard
```

BetterColorInput()
```python
import helper
helper.BetterColorInput(text: str, delay: float = None)

OR

from helper import BetterColorInput
BetterInput(text: str, end: str = None, delay: float = None)

# Gets an input
# 
# Prints the given text letter by letter using the specified delay and gets an input() in cyan after
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed letter by letter
#     DEFAULT: None
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
# 
# beforeColor: Optional[Terminal.color.foreground]
#     The color to change back to after getting the input
#     DEFAULT: None
```

BetterInput()
```python
import helper
helper.BetterInput(text: str, end: str = None, delay: float = None)

OR

from helper import BetterInput
BetterInput(text: str, end: str = None, delay: float = None)

# Gets an input
# 
# Prints the given text letter by letter using the specified delay and gets an input() after
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed letter by letter
#     DEFAULT: None
# 
# end: Optional[str]
#     The text that is passed into the input() statement. 
#     Be aware that this part is not printed letter by letter.
#     DEFAULT: None
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
```

BetterPrint()
```python
import helper
helper.BetterPrint(text: str, delay: float = .01)

OR

from helper import BetterPrint
BetterPrint(text: str, delay: float = .01)

# Prints text
# 
# Prints the given text letter by letter to the command line using the specified delay
# 
# Parameters
# ----------
# text: str
#     The text that is printed letter by letter
# 
# delay: Optional[float]
#     Changes the time between each printed letter
#     DEFAULT: .01
# 
# newLine: Optional[bool]
#     whether to add a new line at the end or not
#     DEFAULT: True
```

ColorInput()
```python
import helper
helper.ColorInput(text: str = None, beforeColor: Terminal.color.foreground = None)

OR

from helper import ColorInput
ColorInput(text: str = None, beforeColor: Terminal.color.foreground = None)

# Gets an input
# 
# executes the input() function in cyan and changes the color back to beforeColor if given
# 
# Parameters
# ----------
# text: Optional[str]
#     The text that is printed before getting the input
#     DEFAULT: None
# beforeColor: Optional[Terminal.color.foreground]
#     The color that was used before (if u want it to change back)
#     DEFAULT: None
```

Output()
```python
import helper
helper.Output(outputValue)

OR

from helper import Output
Output(outputValue)

# Outputs to stdout
# 
# Outputs the given outputValue to stdout and flushes the stream after
# 
# Parameters
# ----------
# outputValue: Any
#     The value that's written to stdout
```

Terminal
```python
import helper
helper.Terminal._  # _ = subclass

OR

from helper import Terminal
Terminal._         # _ = subclass

# Functions & Stuff for the Windows Terminal
# 
# Contains classes and Functions to use for/in the Windows Terminal
# 
# Subclasses
# ----------
# color:
#     returns escape sequences to manipulate the color of the Terminal when printed
```