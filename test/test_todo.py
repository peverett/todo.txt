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

def check_sta(task_str):
    """Convert the task_str string to an Action, then check the Action str 
    matches the original task_str.
    """
    act = str_to_action(task_str)
    #print(f"\nCONVERT_STA\n\t{task_str}\n\t{act}")
    assert task_str == f"{act}"

def test_str_to_action_simple():
    """Convert a simple task string to an Action"""
    act = str_to_action("2021-07-07 Invade Planet Earth")
    assert act.added == "2021-07-07"
    assert act.done == None
    assert act.task == "Invade Planet Earth"
    assert act.project == None
    assert act.context == None
    assert act.due == None

def test_str_to_action_with_project():
    """Convert a task string with project to Action"""
    act = str_to_action("2021-07-07 Invade Planet Earth +KillAllHumans")
    assert act.priority == None
    assert act.added == "2021-07-07"
    assert act.done == None
    assert act.task == "Invade Planet Earth"
    assert act.project == "KillAllHumans"
    assert act.context == None
    assert act.due == None

def test_str_to_action_with_context():
    """Convert a task string with context to Action"""
    act = str_to_action("2021-07-07 Invade Planet Earth @SolarSystem")
    assert act.priority == None
    assert act.added == "2021-07-07"
    assert act.done == None
    assert act.task == "Invade Planet Earth"
    assert act.project == None
    assert act.context == "SolarSystem"
    assert act.due == None

def test_str_to_action_with_context_and_project():
    """Convert a task string with context and context and project to Action"""
    act = str_to_action("2021-07-07 Invade Planet Earth @SolarSystem +KillAllHumans")
    assert act.priority == None
    assert act.added == "2021-07-07"
    assert act.done == None
    assert act.task == "Invade Planet Earth"
    assert act.project == "KillAllHumans"
    assert act.context == "SolarSystem"
    assert act.due == None

def test_str_to_action_with_priority():
    """Convert a task string with priority to Action"""
    act = str_to_action("(A) 2021-07-07 Invade Planet Earth")
    assert act.priority == "A"
    assert act.added == "2021-07-07"
    assert act.done == None
    assert act.task == "Invade Planet Earth"
    assert act.project == None
    assert act.context == None
    assert act.due == None

def test_str_to_action_task_that_is_done():
    """Convert a task string that has been done to Action"""
    act = str_to_action("X 2021-07-07 2021-06-06 Invade Planet Earth")
    #print(f"{act}")
    assert act.priority == None
    assert act.task == "Invade Planet Earth"
    assert act.added == "2021-06-06"
    assert act.done == "2021-07-07"
    assert act.project == None
    assert act.context == None
    assert act.due == None

def test_str_to_action_done_task_with_priority():
    """Convert a done task string with priority to Action"""
    act = str_to_action("X 2021-07-07 (B) 2021-06-06 Invade Planet Earth")
    assert act.priority == "B"
    assert act.task == "Invade Planet Earth"
    assert act.added == "2021-06-06"
    assert act.done == "2021-07-07"
    assert act.project == None
    assert act.context == None
    assert act.due == None


def test_str_to_action_with_due_date():
    """Convert a task with DUE date to Action"""
    act = str_to_action("2021-06-06 Invade Planet Earth DUE:2021-07-07")
    assert act.priority == None
    assert act.task == "Invade Planet Earth"
    assert act.added == "2021-06-06"
    assert act.done == None
    assert act.project == None
    assert act.context == None
    assert act.due == "2021-07-07"

