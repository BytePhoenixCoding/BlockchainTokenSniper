import os

# calling script

def windows():
    os.system('python BSCTokenSniper.py')


def linux():
    os.system('python BSCTokenSniper_Linux.py')
 

def wss()
    os.system('python BSCTokenSniper_Linux_wss.py')

    
def installdep():
    os.system('python -m pip install -r requirements.txt')
    os.system('python run.py')


## message box

def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


# ---------------------
msg = "1. Windows \n" \
      "2. Linux \n" \
      "3. Linux websocket \n" \
      "4. Install Dependency"

print_msg_box(msg=msg, indent=2, title='BSC TOKEN SNIPER')


choose = input("Please the menu :  ")


#if int(choose) == 1:
#    print("Runing on windows")
#    windows()
#else:
#    print("runing on linux")
#    linux()

if int(choose) == 1:
    print("Runing on windows")
    windows()
elif int(choose) == 2:
    print("Runing on Linux")
    linux()
elif int(choose) == 3:
    print("Runing on linux websocket version")
    wss()
elif int(choose) == 4:
    print("Installing Dependency")
    installdep()
