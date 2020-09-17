'''
    Main testing utility for large-scale testing of program functionality
'''
from tests.obj import tests_Video

def run_obj() -> None:
    '''
        Runs all the tests listed in src/tests/obj/;
        returns True if all tests succeed, False otherwise.
    '''
    tests_Video.run_all()

def run_utils() -> None:
    '''
        Runs all the tests listed in src/tests/utils/;
        returns True if all tests succeed, False otherwise.
    '''

def run_all() -> None:
    '''
        Runs all the tests listed in the src/tests/ subdirectories;
        returns True if all tests succeed, False otherwise.
    '''
    run_obj()
    run_utils()
