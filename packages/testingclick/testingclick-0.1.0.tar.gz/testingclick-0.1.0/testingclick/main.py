import click

def validate_rolls(ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        rolls, _, dice = value.partition("d")
        return int(dice), int(rolls)
    except ValueError:
        raise click.BadParameter("format must be 'NdM'")

@click.command()
@click.option(
    "--rolls", type=click.UNPROCESSED, callback=validate_rolls,
    default="1d6", prompt=True,
)
def main(rolls):
    sides, times = rolls
    click.echo(f"Rolling a {sides}-sided dice {times} time(s)")
