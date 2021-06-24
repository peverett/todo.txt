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

from todo import todo_error, todo, Action, str_to_action

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

def test_action_default(today, task):
    """Create a simple action, just the task nothing else. This is the default.
    """
    action = Action(task)
    assert f"{action}" == f"{today} {task}"

def test_action_with_added_date(task):
    """Create a simple action, with the date it was added."""
    aDate = "1999-12-31"
    action = Action(task, added=aDate)
    assert action.added == aDate
    assert f"{action}" == f"{aDate} {task}"

def test_action_with_added_context(today, task):
    """Simple task with a context"""
    context = "SolarSystem"
    action = Action(task, context=context)
    assert f"{action}" == f"{today} {task} @{context}"

def test_action_with_added_project(today, task):
    """Simple task with a project"""
    proj = "DestoryAllHumans"
    action = Action(task, project=proj)
    assert f"{action}" == f"{today} {task} +{proj}"

def test_action_with_priority(today, action, task):
    """Simple task with Priority. Test that only the first char is set as the
    priority and it is capitalised. Set it to None and it should 'disappear'.
    """
    action.priority = "abced"
    assert action.priority == "A"
    assert f"{action}" == f"(A) {today} {task}"
    action.priority = None
    assert f"{action}" == f"{today} {task}"

def test_action_with_due_date(today, task):
    """Simple task with a due date."""
    dueDate = today
    action = Action(task, due=dueDate)
    assert f"{action}" == f"{today} {task} DUE:{today}"

def test_action_set_to_done(today, action, task):
    """Set the task to done."""
    action.done = today
    assert action.done == today
    assert f"{action}" == f"X {today} {today} {task}"

def test_action_with_everything_then_set_to_done(today, task):
    """Set a task with priority, context, project and DUE date, and then set 
    it to done."""
    context = "SolarSystem"
    proj = "DestroyAllHumans"
    priority = "b"
    dueDate = "2022-06-12"
    action = Action(task, priority=priority, context=context, project=proj, due=dueDate)
    expected = f"(B) {today} {task} @{context} +{proj} DUE:{dueDate}"
    assert f"{action}" == expected
    action.done = today
    assert f"{action}" == f"X {today} {expected}"

###############################################################################

def test_str_to_action_simple(task, action):
    """Convert a simple task string to an Action"""
    actual = str_to_action(task)
    assert f"{action}" == f"{actual}"