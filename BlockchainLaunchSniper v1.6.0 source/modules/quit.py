import sys
import os
from . import variables
from . import resume_snipe
from . import time_thread

def quitSniper(delSnipeState):

    if delSnipeState:
        resume_snipe.delSnipeState()
    input(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Bot has been shutdown. Either close the bot or press ENTER to restart." + variables.BLACK)
    print(variables.RESET)
    python = sys.executable
    os.execl(python, python, *sys.argv)