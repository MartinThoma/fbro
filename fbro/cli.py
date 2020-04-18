#!/usr/bin/env python

# Third party modules
import click

# First party modules
import fbro.interactive


@click.command()
@click.version_option(version=fbro.__version__)
def entry_point():
    """Browse files on aws."""
    print(fbro.interactive.main())
