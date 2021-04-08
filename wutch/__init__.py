from .app import WutchApplication
from .version import __version__


def cli():
    """Script invokation function used by poetry."""

    wutch_app = WutchApplication()
    wutch_app.cli()


if __name__ == "__main__":
    # This gets launched if the wutch package is invoked as a python script:
    #   python -m wutch
    #   python wutch/__init__.py
    cli()
