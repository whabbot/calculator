'''Currently, this takes in a sequence of numbers and multiplies them all together'''

from tkinter import *
from tkinter import ttk
import calculate as calc

def calculate(*args):
    '''https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    https://en.wikipedia.org/wiki/Parsing'''
    global currently_inserting
    global previous_answer
    alerts.set('')
    if numbers.get():
        answer = calc.calculateFromString(numbers.get())
        if answer is not None:
            # If the expression is valid and returns an answer, display it.
            numbers.set(answer)
            previous_answer = answer
        else:
            # Else, alert the user
            alerts.set('Please enter a valid expression')
        currently_inserting = False
        

def add_character(character):
    # if the button pressed is a number, a decimal or a bracket, clear the entry before inserting
    clearing_types = [int, float]
    clearing_characters = [".", "(", ")"]
    global currently_inserting
    if not currently_inserting and (type(character) in clearing_types or character in clearing_characters):
        clear_numbers()
    # insert the character provided it doesn't evaluate to None
    if character is not None:
        numbers_entry.insert(INSERT, character)
    numbers_entry.focus()

def clear_numbers():
    # wipes the entry widget (sets the variable numbers to the empty string)
    numbers_entry.focus()
    numbers_entry.delete(0, END)

def backspace():
    # note: insert_into_entry() won't run until after this code is finished running (I think)
    numbers_entry.focus() 
    numbers_entry.delete(numbers_entry.index(INSERT)-1)

def insert_into_entry(*args):
    # whenever the entry is focussed, currently inserting is set to True
    global currently_inserting
    if not currently_inserting:
        currently_inserting = True

root = Tk()
root.title("Calculator")

# two frames: one with all the buttons, one with only the entry widget
calc_frame = ttk.Frame(root, padding="3 3 12 12")
calc_frame.grid(column=0, row=0, sticky=(N, W, E, S))
button_frame = ttk.Frame(root, padding="3 3 12 12")
button_frame.grid(column=0, row=1, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

numbers = StringVar()
alerts = StringVar()
currently_inserting = True # I feel like this is a bit jank, so maybe come up with a better way?
previous_answer = None

numbers_entry = ttk.Entry(calc_frame, width=30, textvariable=numbers)
numbers_entry.grid(column=1, row=1, sticky=(W, E))
numbers_entry.bind("<FocusIn>", insert_into_entry)

numbers_alert = ttk.Label(calc_frame, width=30, textvariable=alerts)
numbers_alert.grid(column=2, row=1, sticky=(W, E))


sevenButton = ttk.Button(button_frame, text="7", command=lambda: add_character(7))
sevenButton.grid(column=1, row=2, sticky=W)
eightButton = ttk.Button(button_frame, text="8", command=lambda: add_character(8))
eightButton.grid(column=2, row=2, sticky=W)
nineButton = ttk.Button(button_frame, text="9", command=lambda: add_character(9))
nineButton.grid(column=3, row=2, sticky=W)
fourButton = ttk.Button(button_frame, text="4", command=lambda: add_character(4))
fourButton.grid(column=1, row=3, sticky=W)
fiveButton = ttk.Button(button_frame, text="5", command=lambda: add_character(5))
fiveButton.grid(column=2, row=3, sticky=W)
sixButton = ttk.Button(button_frame, text="6", command=lambda: add_character(6))
sixButton.grid(column=3, row=3, sticky=W)
oneButton = ttk.Button(button_frame, text="1", command=lambda: add_character(1))
oneButton.grid(column=1, row=4, sticky=W)
twoButton = ttk.Button(button_frame, text="2", command=lambda: add_character(2))
twoButton.grid(column=2, row=4, sticky=W)
threeButton = ttk.Button(button_frame, text="3", command=lambda: add_character(3))
threeButton.grid(column=3, row=4, sticky=W)
zeroButton = ttk.Button(button_frame, text="0", command=lambda: add_character(0))
zeroButton.grid(column=2, row=5, sticky=W)
pointButton = ttk.Button(button_frame, text=".", command=lambda: add_character("."))
pointButton.grid(column=1, row=5, sticky=W)

plusButton = ttk.Button(button_frame, text="+", command=lambda: add_character("+"))
plusButton.grid(column=4, row=2, sticky=W)
minusButton = ttk.Button(button_frame, text="-", command=lambda: add_character("-"))
minusButton.grid(column=4, row=3, sticky=W)
timesButton = ttk.Button(button_frame, text="*", command=lambda: add_character("*"))
timesButton.grid(column=4, row=4, sticky=W)
divButton = ttk.Button(button_frame, text="/", command=lambda: add_character("/"))
divButton.grid(column=4, row=5, sticky=W)
expButton = ttk.Button(button_frame, text="**", command=lambda: add_character("**"))
expButton.grid(column=4, row=6, sticky=W)

leftBracketButton = ttk.Button(button_frame, text="(", command=lambda: add_character("("))
leftBracketButton.grid(column=2, row=6, sticky=W)
rightBracketButton = ttk.Button(button_frame, text=")", command=lambda: add_character(")"))
rightBracketButton.grid(column=3, row=6, sticky=W)

equalsButton = ttk.Button(button_frame, text="=", command=calculate)
equalsButton.grid(column=3, row=5, sticky=W)
clearButton = ttk.Button(button_frame, text="CLEAR", command=clear_numbers)
clearButton.grid(column=4, row=1, sticky=W)
backspaceButton = ttk.Button(button_frame, text="DEL", command=backspace)
backspaceButton.grid(column=3, row=1, sticky=W)
prevAnswerButton = ttk.Button(button_frame, text="ANS", command=lambda: add_character(previous_answer))
prevAnswerButton.grid(column=1, row=6, sticky=W)

for child in button_frame.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

numbers_entry.focus()
root.bind('<Return>', calculate)

root.mainloop()