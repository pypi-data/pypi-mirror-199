# coding: utf-8

from bonnie.excel.actions import Actions
from bonnie.excel.transpose import transpose


actions = [
    Actions.TRANSPOSE,
]


def dispatch():
    for idx, action in enumerate(actions):
        print(f'{idx + 1}. {action}')

    selection = int(input(f'Please select action: '))
    action = actions[selection - 1]

    if action == Actions.TRANSPOSE:
        transpose()

    print('done!')
