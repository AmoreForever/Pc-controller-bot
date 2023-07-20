import re

def find_commands_in_file(file_path = 'main.py'):
    commands = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        pattern = r'@dp\.message_handler.*commands=[\'"](.*?)[\'"]'
        matches = re.findall(pattern, content)
        commands.extend(matches)
    return commands
