#!/usr/bin/env python

# Core Library modules
import platform

# Third party modules
import click

# First party modules
import fbro


@click.command()
@click.version_option(version=fbro.__version__)
def entry_point():
    """Browse files on aws."""
    if platform.system() == "Windows":
        print(f"fbro uses curses which is not supported by Windows.")
        return
    import fbro.interactive

    print(fbro.interactive.main())
