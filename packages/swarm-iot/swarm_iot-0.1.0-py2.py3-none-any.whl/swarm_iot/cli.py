"""Console script for swarm_iot."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for swarm_iot."""
    click.echo("Replace this message by putting your code into "
               "swarm_iot.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
