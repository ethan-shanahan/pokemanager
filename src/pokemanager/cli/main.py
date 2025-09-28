"""CLI.

Usage: pokemanager [OPTIONS] COMMAND [ARGS]...
  Your very own command-line PC.

Options:
  --help  Show this message and exit.

Commands:
  clean  Clean your system of pokemanager files.
"""

from click import Context, group, option, pass_context, version_option

from pokemanager.cli.box import box
from pokemanager.cli.stubs import clean
from pokemanager.cli.utils import CLIRuntime, MainGroup


@group(cls=MainGroup)
@option("-v", "--verbose", count=True)
@version_option(message="pokemanager v%(version)s")
@pass_context
def main(ctx: Context, verbose: int):
    """Your very own command-line PC."""
    runtime = CLIRuntime(verbosity=verbose)
    runtime.verb("Pokemanager...")

    ctx.obj = runtime
    # ctx.obj = 1


main.add_command(clean)
main.add_command(box)
