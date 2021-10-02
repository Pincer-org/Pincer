import os
from typing import List


def split_80_space(string: str, goal_list: List[str] = None) -> str:
    if goal_list is None:
        goal_list = []

    if len(string) < 80:
        goal_list.append(string)
        return '\n'.join(goal_list)

    left, right = string[:80], string[80:]
    left = left[::-1]
    first_space = left.find(' ')
    left_left, left_right = left[first_space:], left[:first_space]

    goal_list.append(left_left[::-1])
    return split_80_space('    ' + left_right[::-1] + right, goal_list)


def sort_all(file_content: str) -> str:
    all_pos = file_content.index('__all__')

    left_parsed_var = file_content[all_pos:]
    end_parenthesis_pos = left_parsed_var.index(')') - 1

    right_parsed = left_parsed_var[:end_parenthesis_pos]
    left_parsed = right_parsed[right_parsed.index('(') + 1:]

    sorted_parsed = [
        f'"{w}"' for w in sorted(
            left_parsed.replace('\n', '')
                .replace('"', '')
                .replace(' ', '')
                .split(',')
        )
    ]

    joined_string = ', '.join(sorted_parsed)
    with_all_name = '__all__ = (\n\t' + joined_string + '\n)'
    all_formatted = split_80_space(with_all_name)

    return (
            file_content[:all_pos]
            + all_formatted
            + file_content[all_pos + end_parenthesis_pos + 2:]
    ).replace('\t', '    ')


def main():
    for directory, sub_folders, files in os.walk('pincer'):
        if '__' in directory:
            continue

        if '__init__.py' not in files:
            continue

        with open(os.path.join(directory, '__init__.py')) as f:
            file_content = f.read()

        if '__all__' not in file_content:
            continue

        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            f.write(sort_all(file_content))


if __name__ == '__main__':
    main()
