"""
TEST todo.py todo_class.py
"""
###############################################################################
# Imports
import os
import sys
import pytest

# Add the ../src directory to the system path to import the script for testing.
src_dir = os.path.abspath("../src")
sys.path.insert(0, src_dir)

from todo import todo_error, todo

###############################################################################

def test_todo_error():
    "Test the todo_error() function raises SystemError"
    error_str = "raises a SystemExit exception"
    with pytest.raises(SystemExit) as error_msg:
        todo_error(error_str) 
    assert error_str in str(error_msg.value)

def test_bad_todo_dir():
    """Test a SystemExit error is produced if the todo_dir passed to the class 
    does not exist"""
    with pytest.raises(SystemExit) as error_msg:
        todo("c://made-up-dir")
    assert "does not exist" in str(error_msg.value)

###############################################################################
