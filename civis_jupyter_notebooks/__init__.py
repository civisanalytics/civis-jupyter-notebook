try:
    from importlib.metadata import version
except ModuleNotFoundError:
    # For Python 3.7
    from importlib_metadata import version


__version__ = version("civis-jupyter-notebook")
