import click
import loci
import loci.cli

from loci_sarif import PROG_NAME
from loci_sarif.add import add
from loci_sarif.summary import summary


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    loci.cli.print_version(PROG_NAME)
    ctx.exit()


@click.group()
@click.option("-v", "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def loci_sarif():
    pass


loci_sarif.add_command(add)
loci_sarif.add_command(summary)


def root_entry():
    try:
        # Run environment checks on every single command. We should know the ENV of each.
        if loci.get_env() is None:
            loci_config_location = loci.get_local_loci_config_location()
            loci.cli.print_warning("Unable to detect the operating environment of this command. Unless you are "
                                   "setting up a new server, this is likely an error, and you should set "
                                   f"[bold]default.env[/bold] in [bold]{loci_config_location}[/bold], or set the "
                                   "LOCI_ENV environment variable in your system.")
        if loci.get_env() != loci.get_default_env():
            loci.cli.print_warning(f"Using non-default environment [bold]{loci.get_env()}[/bold].")
        # Print nothing for default environments

        # This sets all API calls to show the same "working" animation, so that users know something is happening.
        loci.cli.set_global_working_func()

        # Run the command.
        loci_sarif()
    except loci.cli.LociError as e:
        loci.cli.print_loci_error_msg(e)


if __name__ == "__main__":
    root_entry()
