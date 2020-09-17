import numpy as np
import argparse
import time
import sys
import os

from gridvid import *
import tests

globals()['status_entries'] = []

def parse_args():

    argparse_desc = (
        'A high level way to access and interact with Gridvid utilities.'
    )

    help_grid = (
        'Loads a video from a user-determined location, and guides the user '
        'through the process of placing a custom-sized grid on the video.'
    )

    parser = argparse.ArgumentParser(description = argparse_desc)

    parser.add_argument(
        '--unittests', action='store_true', help = 'Runs all unit tests'
    )
    parser.add_argument(
        '--test', action='store_true', help = 'Runs the latest test script'
    )
    parser.add_argument(
        '--grid', action='store_true', help = help_grid
    )

    return parser.parse_args()

def update_status(new_entry):
    tab_len = len('Prev. Selections:') + 7
    tot_len = tab_len
    max_len = 80
    for entry in globals()['status_entries']:
        if entry == '<newline>':
            continue
        elif tot_len + len(entry) + 3 >= max_len:
            tot_len = tab_len + len(entry) + 3
        else:
            tot_len += len(entry) + 3
    if tot_len + len(new_entry) >= max_len:
        globals()['status_entries'].append('<newline>')
    globals()['status_entries'].append(new_entry)

def display_status():
    tab_len = len('Prev. Selections:') + 7
    status = text.bold('Prev. Selections:') + ' '*7
    for n,entry in enumerate(globals()['status_entries']):
        if entry == '<newline>':
            status += '\n' + ' '*tab_len
        elif n == len(globals()['status_entries'])-1:
            status += f'{text.italic(entry)}'
        else:
            status += f'{text.italic(entry)} > '
    return status + '\n'

"""SCRIPT PROCEDURES"""

def procedure_grid():
    pass

"""MAIN SCRIPT"""

args = parse_args()

if args.unittests is True:
    tests.run_all()

if args.test is True:
    print('No Tests Implemented')

if args.grid is True:
    procedure_grid()
