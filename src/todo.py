"""
Python implementation of the TODO.TXT Command Line Interface
Original conception by: Gina Trapani (http://ginatrapani.org)
License: GPL, http://www.gnu.org/copyleft/gpl.html
More information and mailing list at http://todotxt.com
"""
###############################################################################
# Imports

import os
import sys
from datetime import date

if sys.version_info < (3, 6):
    raise SystemExit("Python version 3.6 or better required.")

###############################################################################
# Common functions

def todo_error(error_msg):
    """Raises SystemError in a specific format, which causes program 
    termination."""
    raise SystemExit(f"--\nTODO:\tERROR: {error_msg}")

###############################################################################

class todo(object):
    """Manages the list of todo actions, which are loaded/saved as a plain text
    files.
    """

    def __init__(self, todo_dir):
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

def main():
    """Main function."""
    
    td = todo(os.path.dirname(__file__))
    #TODO Try and load Config File
    #TODO process command line