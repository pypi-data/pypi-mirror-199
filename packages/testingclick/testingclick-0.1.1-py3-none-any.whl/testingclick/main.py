import click

h = 5

def validate_rolls(ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        rolls, _, dice = value.partition("d")
        h = int(dice)

        return int(dice), int(rolls)
    except ValueError:
        raise click.BadParameter("format must be 'NdM'")

@click.command()
@click.option(
    "--rolls", type=click.UNPROCESSED, callback=validate_rolls,
    default="1d6", prompt=True,
)
def main(rolls, h):
    sides, times = rolls
    h = h
    click.echo(f"Rolling a {sides}-sided dice {times} time(s)")
    click.echo(f'{h}')
