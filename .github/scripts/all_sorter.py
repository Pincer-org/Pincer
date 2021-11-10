import os
from typing import List

LINE_WRAP: int = 80


def split_80_space(string: str, goal_list: List[str] = None) -> str:
    if goal_list is None:
        goal_list = []

    if len(string) < LINE_WRAP:
        goal_list.append(string)
        return '\n'.join(goal_list)

    to_reduce = string[:LINE_WRAP][::-1]
    first_space = to_reduce.find(' ')

    reduced, next_parse = to_reduce[first_space:], to_reduce[:first_space]

    goal_list.append(reduced[::-1].rstrip())

    return split_80_space(
        '    ' + next_parse[::-1] + string[LINE_WRAP:],
        goal_list
    )


def parse_list(string: str) -> List[str]:
    return (
        string.replace('\n', '')
            .replace('"', '')
            .replace(' ', '')
            .split(',')
    )


def sort__all__(content: str) -> str:
    pos__all__ = content.index('__all__')

    left_parsed__all__ = content[pos__all__:]
    end_parenthesis_pos = left_parsed__all__.index(')') - 1

    right_parsed = left_parsed__all__[:end_parenthesis_pos]
    __all__list = right_parsed[right_parsed.index('(') + 1:]

    __all__declaration = '__all__ = (\n\t%s\n)' % ', '.join(
        f'"{w}"' for w in sorted(set(parse_list(__all__list)))
    )

    return (
            content[:pos__all__]
            + split_80_space(__all__declaration)
            + content[pos__all__ + end_parenthesis_pos + 2:]
    ).replace('\t', '    ')


def main():
    for directory, _sub_folders, files in os.walk('pincer'):
        if '__' in directory:
            continue

        if '__init__.py' not in files:
            continue

        with open(os.path.join(directory, '__init__.py')) as f:
            file_content = f.read()

        if '__all__' not in file_content:
            continue

        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            f.write(sort__all__(file_content))


if __name__ == '__main__':
    main()
