"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Comprise."""


if __name__ == "__main__":
    main(prog_name="comprise")  # pragma: no cover
