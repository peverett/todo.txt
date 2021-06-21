"""
TEST todo.py todo_class.py
"""
###############################################################################
# Imports
import os
import sys
import pytest
from datetime import date

# Add the ../src directory to the system path to import the script for testing.
src_dir = os.path.abspath("../src")
sys.path.insert(0, src_dir)

from todo import todo_error, todo, Action

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
# Fixtures

@pytest.fixture
def today():
    """return today's date in ISO8601 format."""
    return date.today().strftime("%Y-%m-%d")

@pytest.fixture
def task():
    return "Invade planet Earth"

@pytest.fixture
def action(task):
    """A simple action instance."""
    return Action(task)

###############################################################################

def test_default_action(today, action, task):
    """Create a simple action, just the task nothing else."""
    assert action.added == today
    assert action.task == task
    assert f"{action}" == f"{today} {task}"

def test_action_with_added_date(task):
    """Create a simple action, with the date it was added."""
    aDate = "2021-01-01"
    action = Action(task, added=aDate)
    assert action.added == aDate
    assert f"{action}" == f"{aDate} {task}"

def test_action_with_priority(today, action, task):
    """Simple task with Priority"""
    action.priority = "a"
    assert action.priority == "A"
    assert f"{action}" == f"(A) {today} {task}"

def test_set_action_to_done(today, action, task):
    """Set the task to done."""
    action.done = today
    assert action.done == today
    assert f"{action}" == f"X {today} {today} {task}"

