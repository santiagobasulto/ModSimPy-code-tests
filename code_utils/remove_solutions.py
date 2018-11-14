from pathlib import Path
from copy import deepcopy
import click
import json

@click.group()
def cli():
    pass

# @cli.command()
# @click.argument('input', type=str)
# def single():
#     pass

EMPTY_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Solution goes here"
    ]
}

@cli.command()
@click.argument('input', type=click.File('r', encoding='utf-8'))
# @click.option(
#     '-b', '--base-path', type=str, default='.', help="Base path to look for directories")
# @click.option(
#     '-d', '--dir-path', type=str, help='B', required=True)
@click.option(
    '-n', '--name', type=str, help="Name of the generated notebook",
    required=True)
def single(input, name):
    original = json.load(input)
    found_solution = False
    new_cells = []

    for cell in original['cells']:
        if cell['cell_type'] == 'markdown' and 'solution:' in "".join(cell['source']).strip().lower():
            found_solution = True
            continue
        if cell['cell_type'] == 'markdown' and '(end solution)' in "".join(cell['source']).strip().lower():
            found_solution = False
            continue

        if not found_solution:
            new_cells.append(cell)
        else:
            new_cells.append(deepcopy(EMPTY_CELL))

    original['cells'] = new_cells
    with open(name, 'w') as fp:
        fp.write(json.dumps(original))

# One notebook
# python remove_solutions.py single file_path --new-name --name-extract --name-generate
# python remove_solutions.py --dir-path "Chapter *"

if __name__ == '__main__':
    cli()
