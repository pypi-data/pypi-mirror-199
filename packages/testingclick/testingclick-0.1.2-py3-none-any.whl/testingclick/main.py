import click



class ChoiceOption(click.Option):
    def __init__(self, param_decls=None, **attrs):
        click.Option.__init__(self, param_decls, **attrs)
        if not isinstance(self.type, click.Choice):
            raise Exception('ChoiceOption type arg must be click.Choice')

        if self.prompt:
            prompt_text = '{}:\n{}\n'.format(
                self.prompt,
                '\n'.join(f'{idx: >4}: {c}' for idx, c in enumerate(self.type.choices, start=1))
            )
            self.prompt = prompt_text

    def process_prompt_value(self, ctx, value, prompt_type):
        if value is not None:
            index = prompt_type(value, self, ctx)
            return self.type.choices[index - 1]

    def prompt_for_value(self, ctx):
        # Calculate the default before prompting anything to be stable.
        default = self.get_default(ctx)

        prompt_type = click.IntRange(min=1, max=len(self.type.choices))
        return click.prompt(
            self.prompt, default=default, type=prompt_type,
            hide_input=self.hide_input, show_choices=False,
            confirmation_prompt=self.confirmation_prompt,
            value_proc=lambda x: self.process_prompt_value(ctx, x, prompt_type))



h = list('HELLO')

def set_choice(ctx, param, value):
#	if not value or ctx.resilient_parsing:
#		return

	if value == 5:
		ctx.command.params[1].type=click.Choice(['a', 'b', 'c'])
		ctx.command.params[1].cls=ChoiceOption
		ctx.command.params[1].default='b'
	elif value == '7':
		ctx.command.params[1].type=click.Choice(['d', 'e', 'f'])


def set_choice_mod(ctx, param, value):
	if value == 7:
		ctx.command.params[3].type=click.Choice(['z', 'y', 'x'])
	elif value == '9':
		ctx.command.params[3].type=click.Choice(['w', 'p', 'u'])


def set_choice_chap(ctx, param, value):
	if value == 'a':
		ctx.command.params[2].type=click.Choice(['7', '9'])

@click.command()
@click.option(
    "--rolls", type=click.UNPROCESSED, callback=set_choice,
    default=5, prompt=True,expose_value=True, is_eager=True
)
@click.option('--chapters', prompt=True, callback=set_choice_chap, is_eager=True)
@click.option(
		'--mod',
	#	type=click.UNPROCESSED,
		callback=set_choice_mod,
		default=7,
		prompt=True,
		expose_value=True,
		is_eager=True
		)
@click.option('--chap', prompt=True, is_eager=True)
def main(rolls, chapters, mod, chap):
    click.echo(f"Rolling a {h}-sided dice {chapters} time(s)")
    click.echo(f'{rolls}')



def myfunct(v):
	if v == 'a':
		return ['c', 'd']

@click.command()
@click.option(
    "--param1",
    type=click.Choice(['a', 'b']),
    prompt="First parameter",
)
@click.option(
    "--param2",
    type=click.Choice([lambda:myfunct(click.get_current_context().params.get('param1', None))()]),
    prompt="Second parameter",
)
def cmd(param1, param2):
    print(param2, param1)
