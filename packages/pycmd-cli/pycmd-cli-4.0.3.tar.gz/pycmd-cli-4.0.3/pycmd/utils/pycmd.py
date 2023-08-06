from asyncore import write
import sys
from difflib import SequenceMatcher
import tkinter as tk
from tkinter import filedialog
from colorama import Fore as fc, Back as bg, Style as st, init
from subprocess import run
init(autoreset=True)

def execute(command, exit=False, rewrite=False):
    
    """
    ### Shell Commands Executer
    
    Silently executes a command and handles the errors.
    If the command fails to run, logs the error message and returns `None`
    Else returns the output of the command 
    
    If `exit` is `True`, exists the program if an error occurs
    
    `rewrite` will print with `\\r` instead of `\\n`
    """
    
    output = run(command, shell=True, capture_output=True)
    
    if output.returncode == 0:
        return output.stdout.decode('utf-8')
    else:
        if rewrite:
            print('\n' + bg.YELLOW + fc.BLACK + 'LOG' + fc.RESET + bg.RESET + ' ' + f'While executing: {fc.CYAN}"' + command + f'"{fc.RESET}: \n')
        else:
            print('\r' + bg.YELLOW + fc.BLACK + 'LOG' + fc.RESET + bg.RESET + ' ' + f'While executing: {fc.CYAN}"' + command + f'"{fc.RESET}: \n')
        print(bg.RED + 'ERR' + bg.RESET +
              ' ' + output.stderr.decode('utf-8') + " " * 20)
        if exit:
            sys.exit(1)
            
        return None

def autocorrect(word: str, word_list: list[str], tolerance: float = 0.6, return_none=True) -> str:
    """
    ### Autocorrect
    Returns autocorrected `word` from the `word_list`.
    
    Returns `None` if no match found and `return_none` is `True` else returns `word`
    """
    
    for filter_word in word_list:
        if SequenceMatcher(a=word, b=filter_word).ratio() > tolerance:
            return filter_word
        
    return None if return_none else word 

def argparse(args: list=sys.argv):
    """
    ### Argument Parser
    Returns argument and flags from `sys.argv` or `args` list
    ```py
    return argument, flags
    ```
    """
    argument = ''
    flags = []
    for arg in args:
        if arg.startswith('-'):
            flags.append(arg)
        else:
            argument = arg
    return argument, flags

def get_path(prompt:str='Open'):
    """
    Get folder path by input
    
    `prompt` is the title of the dialog
    
    """

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askdirectory()
        
    return file_path if file_path else None

