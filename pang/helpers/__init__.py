import os


def create_dirs():
    if not os.path.exists('host_vars'):
        os.makedirs('host_vars')

    if not os.path.exists('group_vars'):
        os.makedirs('group_vars')

    if not os.path.exists('inventory'):
        os.makedirs('inventory')
