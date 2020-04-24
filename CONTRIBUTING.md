# Contributing

## Linting

This project utilizes [Pylama](https://pylama.readthedocs.io/en/latest/) for code linting. This was chosen because it it is an algamation of other linters so we can attempt to follow as many of the various Python style guides as we can. We don't heavily enforce its usage, but we strongly prefer it.

Pylama is provided as a dependency in the requirements.txt file to be installed in the virtualenv used by this project.
Config file: `pylama.ini`

### Integration with Editors

Pylama can be integrated with several different text editors to provide on-the-fly or on-save linting in the editor window for open files. We have tested and used the Visual Studio Code integration and have partially played around with the Atom integration. Any others are unknown to use and there may be configuration details we miss below that will be needed to make them work as expected.

* **Visual Studio Code:** If you allow the usage of the settings provided by this project in the `.vscode/settings.json` file, this will be set up for you automatically.
* **Atom:** You'll need to install the following extensions for it to work:
  * [`linter`](https://atom.io/packages/linter): The base linter extension used for linting a variety of languages in Atom
  * [`linter-ui-default`](https://atom.io/packages/linter-ui-default): The default UI for the `linter` extension.
  * [`linter-pylama`](https://atom.io/packages/linter-pylama): The extension for the `linter` extension that enables linting with Pylama
* **PyCharm:** PyCharm has some built-in linting via its [Code Style settings](https://www.jetbrains.com/help/pycharm/code-style-python.html). A [Pylint plugin](https://plugins.jetbrains.com/plugin/11084-pylint) also exist for integrating Pylint with it. There dooesn't seem to be any direct support for integrating with Pylama, though.

### Markdown Linting

For Markdown styling, there is the [markdownlint](https://github.com/DavidAnson/markdownlint) tool. It's an npm package, so we don't include it in this project. If you want to use it, you can either install it yourself external to the project, or just install the extension to use it in your editor of choice. The project's README contains links to various editor extensions for it.

## Branching

feature/{branch-name} - For new features  
enhance/{branch-name} - Updating an existing feature  
fix/{branch-name} - For bug fixes

## Documentation Format

```python
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

### Example

```python
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
