import sys
import os
from . import variables
from . import time_thread

def quitSniper(displayMsg):

    if displayMsg:
        input(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.YELLOW + "Bot has been shutdown. Either close the bot or press ENTER to restart." + variables.RESET)

    os.execl(sys.executable, sys.executable, *sys.argv)

