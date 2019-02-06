import os
import subprocess

import click

from .sb_core import Note, get_notes_with_tag, get_tags, get_notes_with_project, get_projects, init_slipbox, get_all_notes, NOTES_DIR


@click.group('note')
def cli():
    pass


@click.command()
def init():
    init_slipbox()


@click.command()
@click.argument('title')
@click.option('-t', '--tag', default=None, multiple=True, type=str, help='tag for note, each tag has to be added separately')
@click.option('-pr', '--project', default=None, type=str, help='project')
@click.option('-p', '--parent', default=None, multiple=True, type=str, help='parent of note, each parent has to be added separately')
@click.option('-type', '--type', default=None, type=str, help='Note type')
@click.option('-bib', '--bibkey', default=None, type=str, help='Bibkey of reference')
@click.option('-c', '--content', default=None, type=str, help='Content of Note')
def create(title, tag, project, parent, type, content, bibkey):
    tags = [str(t) for t in tag]
    parents = [str(p) for p in parent]
    Note.create(title, tags, project, parents, type, content, bibkey)


@click.command()
@click.argument('id', type=int)
def edit(id):
    fp = os.path.join(NOTES_DIR, '{}.md'.format(id))
    subprocess.call(['editor', fp])


@click.command()
@click.option('-pr', '--project', default=None, type=str, help='project')
@click.option('-t', '--tag', multiple=True, default=None, type=str, help='tag for note, each tag has to be added separately')
def notes(project, tag):
    output_str = 'Notes:\n'
    all_notes = get_all_notes()
    notes = []
    if project:
        for note in all_notes:
            if project == note.project:
                notes.append(note)
    else:
        notes = all_notes
            
    tags = [str(t) for t in tag]
    if tags:
        for note in notes:
            for _tag in tags:
                if _tag in note.tags:
                    output_str += ' - {}\n'.format(repr(note))
    else:
        for note in notes:
            output_str += ' - {}\n'.format(repr(note))

    print(output_str)


@click.command()
@click.argument('id', type=int)
def links(id):
    note = Note.load(id)
    note.print_links()


@click.command()
@click.argument('id', type=int)
def sequence(id):
    note = Note.load(id)
    note.print_sequence()


@click.command()
@click.argument('id', type=int)
def show(id):
    note = Note.load(id)
    note.show()


@click.command()
def tags():
    tags = get_tags()
    output_str = 'Tags:\n'
    for tag in tags:
        output_str += ' - {}\n'.format(tag)
    print(output_str)


# @click.command()
# @click.argument('tag', type=str)
# def notes_with_tag(tag):
#     notes_with_tag = get_notes_with_tag(tag)
#     output_str = 'Notes with tag "{}":\n'.format(tag)
#     for note in notes_with_tag:
#         output_str += ' - {}\n'.format(repr(note))
#     print(output_str)


@click.command()
def projects():
    projects = get_projects()
    output_str = 'Projects:\n'
    for project in projects:
        output_str += ' - {}\n'.format(project)
    print(output_str)


# @click.command()
# @click.argument('project', type=str)
# def notes_with_project(project):
#     notes_with_project = get_notes_with_project(project)
#     output_str = 'Notes with project "{}":\n'.format(project)
#     for note in notes_with_project:
#         output_str += ' - {}\n'.format(repr(note))
#     print(output_str)


cli.add_command(init)
cli.add_command(create)
cli.add_command(edit)
cli.add_command(notes)
cli.add_command(links)
cli.add_command(sequence)
cli.add_command(show)
cli.add_command(tags)
# cli.add_command(notes_with_tag)
cli.add_command(show)
cli.add_command(projects)
# cli.add_command(notes_with_project)


if __name__ == '__main__':
    cli()
