title = "Dashboard"
lines = {}
__lastPrintedLines = 0
exists: bool = False

# prints the dashboard to the console for the first time
def printOut():
    global exists
    exists = True
    global __lastPrintedLines
    consoleWidth = 50
    keyWidth = 0
    for key in lines.keys():
        if len(key) > keyWidth:
            keyWidth = len(key)
    keyWidth += 5
    
    number_ralign = 1
    # Go through all the values and find the longest one which is a number
    for key, value in lines.items():
        if str(value).isdigit() and len(str(value)) > number_ralign:
            number_ralign = len(str(value))
    
    __lastPrintedLines = 1
    
    print(f"{title}".ljust(consoleWidth))
    for key, value in lines.items():
        printout = "| "
        # Add padded key
        printout += f"{key}:".ljust(keyWidth)
        # Add value
        if str(value).isdigit():
            printout += str(value).rjust(number_ralign)
        else:
            printout += str(value)
        
        printout = printout[:consoleWidth].ljust(consoleWidth)
        
        print(printout)
        
        __lastPrintedLines += 1


# removes the dashboard from the console
def remove():
    global exists
    if(exists):
        print("\033[A" * __lastPrintedLines, end="")
    exists = False


# updates the dashboard with new data
def update():
    global exists
    if(exists):
        print("\033[A" * __lastPrintedLines, end="")
    printOut()


def addLine(key: str, value: str, autoUpdate=True):
    lines[key] = value
    if(autoUpdate and exists):
        update()


def removeLine(key: str, autoUpdate=True):
    del lines[key]
    if(autoUpdate and exists):
        update()


def changeValue(key: str, value: str, autoUpdate=True):
    lines[key] = value
    if(autoUpdate and exists):
        update()