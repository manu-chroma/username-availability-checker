import click
import shutil

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=2, offset=2)


@click.command()
def add():
    # Get user input
    name = click.prompt('Enter website name', type=str, default=None)
    if name is None:
        click.echo('website name is required.')
        click.Abort()

    avatar_prompt = '''How to get Avatar?
    1. opengraph
    2. not supported
    Enter number(default is 2)
    '''
    avatar = click.prompt(avatar_prompt, type=int, default=2)

    characters_prompt = '''What characters are allowed?
    1. alphabet
    2. number
    3. underscore
    4. dot
    5. hypen
    Enter numbers(i.e. 1,2,3)
    '''
    characters = click.prompt(characters_prompt, type=str, default='1')
    split = characters.split(',')
    characters = ''
    for char in split:
        if char == '1':
            characters += 'a-zA-Z'
        elif char == '2':
            characters += '0-9'
        elif char == '3':
            characters += '_'
        elif char == '4':
            characters += '.'
        elif char == '5':
            characters += '-'

    available_min_length = click.prompt('Enter available minimum length',
                                        type=int,
                                        default=5)

    min_length = click.prompt('Enter minimum length',
                              type=int,
                              default=1)

    max_length = click.prompt('Enter max length',
                              type=int,
                              default=30)

    url = click.prompt('Enter url format',
                       type=str,
                       default='https://{w}.com/{u}')

    content_verification = click.prompt('Enter content verification(press enter to continue)',
                                        type=str,
                                        default='')

    constant_username = click.prompt(
        'Enter a constant username', type=str, default='constant_username')

    taken_usernames = []
    while True:
        taken_username = click.prompt('Enter a taken username', type=str, default='')
        if taken_username == '':
            break
        taken_usernames.append(taken_username)
    if not taken_usernames:
        click.echo('taken usernames are required at least one.')
        click.Abort()

    # Backup files
    shutil.copyfile('websites.yml', 'websites.yml.before')
    shutil.copyfile('tests/test_data.yml', 'tests/test_data.yml.before')

    # Insert data into websites.yml
    with open('websites.yml') as f:
        website = yaml.load(f)

    username_pattern = '''
    characters: {chars}
    available_min_length: {available_min}
    min_length: {min}
    max_length: {max}
    '''.format(chars=characters,
               available_min=available_min_length,
               min=min_length,
               max=max_length)

    insert_in_order(website['username_patterns'], name, yaml.load(username_pattern))

    avatar_yaml = 'opengraph' if avatar == '1' else False

    insert_in_order(website['avatar'], name, avatar_yaml)

    if content_verification != '':
        insert_in_order(website['content_verification'], name,
                        DoubleQuotedScalarString(content_verification))

    insert_in_order(website['urls'], name, url)

    insert_in_order(website['constant_usernames'], name,
                    DoubleQuotedScalarString(constant_username))

    with open('websites.yml', 'w') as f:
        yaml.dump(website, f)

    # Insert data into test_data.yml
    with open('tests/test_data.yml') as f:
        test_data = yaml.load(f)

    test_data_yaml = '''
    invalid_usernames:
      - "$very%long{invalid}user(name)"
    available_usernames:
      - "zNRe3jx3isA8CoM"
    '''
    test_data_yaml = yaml.load(test_data_yaml)
    test_data_yaml.insert(1, 'taken_usernames', [])
    for username in taken_usernames:
        test_data_yaml['taken_usernames'].append(DoubleQuotedScalarString(username))

    insert_in_order(test_data, name, test_data_yaml)

    with open('tests/test_data.yml', 'w') as f:
        yaml.dump(test_data, f)


def insert_in_order(source, name, target):
    for i, k in enumerate(source):
        if k > name:
            source.insert(i, name, target)
            return


if __name__ == '__main__':
    add()
