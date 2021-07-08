"""
Python implementation of the TODO.TXT Command Line Interface
Original conception by: Gina Trapani (http://ginatrapani.org)
License: GPL, http://www.gnu.org/copyleft/gpl.html
More information and mailing list at http://todotxt.com
"""
###############################################################################
# Imports

import sys

# Uses the dataclass class, so python 3.7 or better is required
if sys.version_info < (3, 7):
    raise SystemExit("Python version 3.7 or better required.")

import os
import re 
from datetime import date
from dataclasses import dataclass, field

###############################################################################
# Common functions

def todo_error(error_msg: str):
    """Raises SystemError in a specific format, which causes program 
    termination."""
    raise SystemExit(f"--\nTODO:\tERROR: {error_msg}")

###############################################################################

@dataclass
class Action():
    """Represents an 'action' in the to do list, using dataclass. 
    Use the __str__() method to output the action as a string in the following format:
        X {done date} ({priority}) {task} @{context} +{project} DUE:{due date}
    So a task that isn't yet completed could look like this: 
        (A) 2021-06-24 Invade planet earth @SolarSysetm +KillAllHumans DUE: 2021-06-24
    And once that task is done, it would look like this:
        X 2021-06-24 (A) 2021-06-24 Invade planet eartth @SolarSystem +KillAllHumans DUE: 2021-06-24
    """
    task: str                                       # The text of the task
    added: str = date.today().strftime("%Y-%m-%d")  # Current date, if not set
    done: str = None                                # date task was done
    priority: str = None                            # A, B, C, etc...
    _priority: str = field(init=False)              # setter will init this       
    context: str = None                             # One @ context string
    project: str = None                             # One + project string
    due: str = None                                 # Due date

    def __str__(self):
        """String representation"""
        astr = list()
        if self.done:
            astr.append("X")
            astr.append(self.done)
        if self.priority:
            astr.append(f"({self.priority})")
        astr.append(self.added)
        astr.append(self.task)
        if self.context:
            astr.append(f"@{self.context}")
        if self.project:
            astr.append(f"+{self.project}")
        if self.due:
            astr.append(f"DUE:{self.due}")
        return " ".join(astr)
    
    @property 
    def priority(self) -> str:
        """Get the priority"""
        return self._priority

    @priority.setter
    def priority(self, p: str):
        """Set the priority, a single letter from A to Z (capital), can also
        be None."""
        self._priority = p.upper()[0] if isinstance(p, str) else None


###############################################################################

class todo(object):
    """Manages the list of todo actions, which are loaded/saved as a plain text
    files.
    """

    def __init__(self, todo_dir: str):
        """Initialise todo class by loading the list of todo actions from a 
        file.

        param: todo_dir The directory wher to load the todo.txt and done.txt
               files. 
        """
        if not os.path.exists(todo_dir):
            todo_error(f"\"{todo_dir}\" does not exist!")
        self.__todo_dir = todo_dir

        #TODO load the tasks from a todo.txt file if it exists
        self.__tasks = []

        self.__dispatcher = {
            "add":      self.__add,
        }

    @property
    def tasks(self):
        """Get the list of tasks in the todo class"""
        return self.__tasks

    def command(self, action):
        """Process a command action in the self.__dispatcher dictionary.

        param: action A list of words, the first word should be an 'action'
               string.
        """
        cmd = self.__dispatcher.get(action[0])
        if cmd:
            return cmd(action[1:])
        else:
            todo_error(f"Unknown action - \"{action}\"")

    def __add(self, task_words):
        """Add a new task to the task list.

        param: task as a list of words, making a string.
        """
        # Add the current date as the first 'word' of the task.
        task_words.insert(0, "{}".format(date.today().strftime("%Y-%m-%d")))

        # Join everything in the 'task' list together, this works 
        # even if the task is enclosed in quotes. 
        task_str = " ".join(task_words)
        self.__tasks.append(task_str)
    
###############################################################################

# Regexs
DATE_RE = re.compile( r"(\d{4}-\d{2}-\d{2})\s" )     # ISO 8601 date 
PRIORITY_RE = re.compile( r"^\(([A-Z])\)\s" )        # Priority A, B , C 
PROJECT_RE = re.compile( r"\W\+(\w+)" )              # +<word>
CONTEXT_RE = re.compile( r"\W\@(\w+)" )              # @<word>
DONE_RE = re.compile( r"^X\s" )                      # X is first char
DUE_RE = re.compile( r"DUE:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE )
LINE_NO_RE = re.compile( r"(^\d+\s+)(\S.*)" )

def str_to_action(task: str) -> Action:
    """From a todo task string input, break the string into the required 
    fields and create an Action instance for that task.
    """
    def match(match_re, input):
        "RegEx matches at the start of the string"
        res = match_re.match(input)
        if res:
            match_str = res.groups()[0]
            input = input[res.end():]
        else:
            match_str = None
        return (match_str, input.strip())

    if DONE_RE.match(task):
        (done_date, task) = match(DATE_RE, task[2:])
    else:
        done_date = None

    (priority, task) = match(PRIORITY_RE, task)
    (added, task) = match(DATE_RE, task)

    def search(search_re, input):
        """Regex search anywhere in the string the string without the regex part"""
        res = search_re.search(input)
        if res:
            search_str = res.groups()[0]
            input = "".join([
                input[:res.start()],
                input[res.end():]
            ])
        else:
            search_str = None
        return (search_str, input.strip())                

    (project, task) = search(PROJECT_RE, task)
    (context, task) = search(CONTEXT_RE, task)
    (due, task) = search(DUE_RE, task)
    
    #print(f"\nEXTRACTED:\n\t{done_date=}\n\t{priority=}\n\t{added=}\n\t{task=}\n\t{context=}\n\t{project=}")

    return Action(
        task = task, 
        done = done_date,
        priority = priority,
        added = added,
        context = context,
        project = project,
        due = due
        )


###############################################################################

def main():
    """Main function."""
    
    #td = todo(os.path.dirname(__file__))
    one = Action("A simple task")
    print(one)
    #TODO Try and load Config File
    #TODO process command line


###############################################################################

if __name__ == "__main__":
    main()