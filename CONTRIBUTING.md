# Branching
feature/{branch-name} - For new features<br />
enhance/{branch-name} - Updating an existing feature<br />
fix/{branch-name} - For bug fixes

# Documentation Format
```
"""
Summary line.

Extended description of function. (Optional)

Parameters
----------
param : Type

Returns
-------
Type
    description of return (optional)
"""
```
## Example
```
def add(num1, num2):
    """
    adds 2 numbers
    
    Parameters
    ----------
    num1 : Int
    num2 : Int
    
    Returns
    -------
    Int
        sum of 2 numbers
    """
    return num1 + num2
```
