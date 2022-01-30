# Core Library modules
import platform

# Third party modules
import click
from botocore.exceptions import ClientError

# First party modules
import fbro


@click.command()
@click.version_option(version=fbro.__version__)
def entry_point():
    """Browse files on aws."""
    if platform.system() in ["Windows", "Java"]:
        print(
            f"fbro uses curses which is not supported "
            f"by your system ({platform.system()})."
        )
        return
    # First party modules
    import fbro.interactive

    try:
        print(fbro.interactive.main())
    except ClientError as e:
        print(e)
        print("Potential explanation: Maybe you're not logged in?")
