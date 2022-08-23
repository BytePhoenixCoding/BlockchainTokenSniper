from . import variables
from pynput.keyboard import Key, Listener, Controller
from pynput import keyboard
from . import debug
import traceback
from . import sell_token
from . import time_thread
import threading
import time

def on_press(key):
    if variables.keyboardListeningEnabled:
        try:
            if key == Key.space:
                sell_token.preSell(100)
            elif str(key.char) == '1' and not variables.enableTrailingStopLoss:
                sell_token.preSell(10)
            elif str(key.char) == '2' and not variables.enableTrailingStopLoss:
                sell_token.preSell(20)
            elif str(key.char) == '3' and not variables.enableTrailingStopLoss:
                sell_token.preSell(30)
            elif str(key.char) == '4' and not variables.enableTrailingStopLoss:
                sell_token.preSell(40)
            elif str(key.char) == '5' and not variables.enableTrailingStopLoss:
                sell_token.preSell(50)
            elif str(key.char) == '6' and not variables.enableTrailingStopLoss:
                sell_token.preSell(60)
            elif str(key.char) == '7' and not variables.enableTrailingStopLoss:
                sell_token.preSell(70)
            elif str(key.char) == '8' and not variables.enableTrailingStopLoss:
                sell_token.preSell(80)
            elif str(key.char) == '9' and not variables.enableTrailingStopLoss:
                sell_token.preSell(90)
            else:
                pass
        except:
            pass

def setup_hotkeys():
    try:
        if variables.enableHotkeys:
            variables.keyboardListeningEnabled = True

            listener = keyboard.Listener(on_press=on_press)
            listener.start()

            print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Use keys 1-9 to sell 10-90% of tokens at any time, use spacebar to sell all tokens at once.")
            if variables.autoSellMultiplier != None:
                print(variables.RESET + time_thread.currentTimeStamp + " [Info]     " + variables.GREEN + "Auto-selling all tokens at " + str(variables.autoSellMultiplier) + "x original value.")

            print(variables.RESET + time_thread.currentTimeStamp + " [Warning]  " + variables.YELLOW + "DO NOT type anything else in the keyboard until you want to sell.")
            print("")      


    except:
        debug.handleError(traceback.format_exc(), "setupHotkeys")






