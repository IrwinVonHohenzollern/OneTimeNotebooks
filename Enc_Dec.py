#Our program allows to encode, decode and break message
import string, random as rnd, math
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Checkbutton

#Version of this program
version = '1.0'

alphabet, titles = [], []
possible_symbols = {
'RusLow': ''.join([chr(i) for i in range(1072, 1104)]) + chr(1105),
'RusHigh': ''.join([chr(i).upper() for i in range(1072, 1104)]) + chr(1105).upper(),
'EngLow': string.ascii_lowercase, 'EngHigh': string.ascii_uppercase, 'Numbers': string.digits,
'Punctuation': string.punctuation, 'Space_Symbols': string.whitespace
    }

message = ''
key, nkey = 0, 0
tabTitle = ('Times New Roman', 24)

#Here we create our alphabet
class ch:
    def __init__(self, master, title, data):
        self.var = IntVar()
        self.var.set(0)
        self.title = title
        self.name = data
        self.data = possible_symbols[data]
        self.cb = Checkbutton(master, text = title, var = self.var, onvalue = 1, offvalue = 0)
        self.cb.pack()
    

def check_state():
    global alphabet, titles, lst, l02
    for i in lst:
        if i.var.get() == 1:
            if i.data not in alphabet:
                alphabet += [i.data]
            if i.name not in titles:
                titles.append(i.name)
        elif i.var.get() == 0:
            if i.data in alphabet:
                alphabet.remove(i.data)
            if i.name in titles:
                titles.remove(i.name)
    l02.config(text = 'Here is your alphabet:\n' + ' '.join(titles))

def confirm():
    global alphabet
    if type(alphabet) != "<class 'list'>":
        alphabet = ''.join(alphabet)

def erase():
    global alphabet
    alphabet = []

#This block creates window for our software
window = Tk()
window.title('Encrypting_Decrypting_Software ' + version)
window.geometry('640x360')
tab_control = ttk.Notebook(window)
tab0 = ttk.Frame(tab_control)

#This block creates panels for our software
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab0, text = 'Alphabet')
tab_control.add(tab1, text = 'Encryption')
tab_control.add(tab2, text = 'Decryption')
tab_control.add(tab3, text = 'Message_breaking')
tab_control.pack(expand = 1, fill = 'both')

#Here we design the first panel 'Alphabet'
f0 = Frame(master = tab0)
f1 = Frame(master = tab0)
l01 = Label(f0, text = 'Сhoose symbols for alphabet', font = tabTitle)
f0.pack()
f1.pack()
l01.pack()

ch1 = ch(f0, 'English little letters', 'EngLow')
ch2 = ch(f0, 'English big letters', 'EngHigh')
ch3 = ch(f0, 'Numbers', 'Numbers')
ch4 = ch(f0, 'Russian little letters', 'RusLow')
ch5 = ch(f0, 'Russian big letters', 'RusHigh')
ch6 = ch(f0, 'Punctuation symbols', 'Punctuation')
ch7 = ch(f0, 'Space_symbols', 'Space_Symbols')
lst = [ch1, ch2, ch3, ch4, ch5, ch6, ch7]

l02 = Label(f1, text = 'Your alphabet: ')
l03 = Label(f1, text = 'You must clear your alphabet\n if you want to add new symbols\n after confirmation')
b01 = Button(f1, text = 'Create alphabet', command = check_state)
b02 = Button(f1, text = 'Record alphabet', command = confirm)
b03 = Button(f1, text = 'Erase alphabet', command = erase)
b01.pack()
l02.pack()
b02.pack()
l03.pack(side = RIGHT)
b03.pack(side = RIGHT)


#Now we read our message


def get_message():
    global e11, message
    message = str(e11.get())
    l12.config(text = 'Message is recorded')


    
def get_key():
    global e12, key
    key = int(e12.get())
    l13.config(text = 'Key is recorded')



def Caesar_encrypt():
    '''
    This is a program to encrypt the message with chosen key. It returns encrypted string.
    '''
    global message, key
    new_message = ''
    for symbol in message:
        if symbol in alphabet:
            index = alphabet.index(symbol)
            new_index = (index + key) % len(alphabet)
            new_message += alphabet[new_index]
        else:
            new_message += symbol
    with open('Encrypted_Caesar.txt', 'w') as ouf:
        ouf.write(new_message)
    l14.config(text = 'Encoded Caesar-method message is written in file')

        
def QDK_encrypt():
    global message
    '''
    This is Quantum cypher. The size of shift is a m, where 2 ** m >= length of alphabet and m is primal number.
    This program returns a typle of 2 lists: encrypted message and its key.
    '''
    size = math.ceil(math.log(len(alphabet), 2))

    def number_generator():
        '''
        This function returns random number.
        '''
        x = 0
        for i in range(size):
            r = rnd.choice([0, 1])
            x += r * 2 ** i
        return rnd.choice([-1, 1]) * x
    
    new_message, key = '', []
    for symbol in message:
        if symbol in alphabet:
            index = alphabet.index(symbol)
            num = number_generator()
            new_index = (index + num) % len(alphabet)
            new_message += alphabet[new_index]
            key += [bin(num)]
        else:
            new_message += symbol
            key += [bin(0)]
    with open('QDK.txt', 'w') as ouf:
        ouf.write(str(key))

    with open('QDK-message.txt', 'w') as ouf:
        ouf.write(new_message) 

    l15.config(text = 'Key and message with QDK method are recorded')



f12 = Frame(master = tab1)
f13 = Frame(master = tab1)
f14 = Frame(master = tab1)
f12.pack()
f13.pack()
f14.pack()

l11 = Label(f12, text = 'Encrypt message', font = tabTitle)

l12 = Label(f13, text = 'Type your message here:')
e11 = Entry(f13, width = 50)
e11.focus()
b11 = Button(f13, text = 'Get the message', command = get_message)

l13 = Label(f13, text = 'Type number for Caesar key')
e12 = Entry(f13, width = 20)
b12 = Button(f13, text = 'Get the key', command = get_key)


l14 = Label(f14, text = 'Encode your message with Caesar sypher')
b13 = Button(f14, text = 'Encode', command = Caesar_encrypt)

l15 = Label(f14, text = 'Encode with QDK method')
b14 = Button(f14, text = 'Encode', command = QDK_encrypt)

l11.pack(side = LEFT)
l12.pack(side = TOP)
e11.pack(side = TOP)
b11.pack(side = TOP)


l13.pack(side = TOP)
e12.pack(side = TOP)
b12.pack(side = TOP)

l14.pack()
b13.pack()
l15.pack()
b14.pack()

##########################################################
def Caesar_decrypt():
    global nkey, e21
    nkey = int(e21.get())
    key = nkey
    with open('Encrypted_Caesar.txt', 'r') as inf:
        message = '\n'.join(inf.readlines())
    new_message = ''
    for symbol in message:
        if symbol in alphabet:
            index = alphabet.index(symbol)
            new_index = (index - key) % len(alphabet)
            new_message += alphabet[new_index]
        else:
            new_message += symbol
    e21.insert(0, new_message)
    with open('Decrypted_Caesar.txt', 'w') as ouf:
        ouf.write(new_message)
    l22.config(text = 'Message is decrypted and written in file')

    
def Unbreakable_decrypt():
    with open('QDK.txt', 'r') as inf:
        key = eval(inf.readline())
    with open('QDK-message.txt', 'r') as inf:
        message = inf.readline()
    new_message = ''
    for i in range(len(message)):
        if message[i] in alphabet:
            new_message += alphabet[(alphabet.index(message[i]) - int(key[i], 2)) % len(alphabet)]
        else:
            new_message += message[i]
    with open('Decrypted_QDK.txt', 'w') as ouf:
        ouf.write(new_message)
        l23.config(text = 'Message is decrypted and written in file')

f21 = Frame(tab2)
f22 = Frame(tab2)
f23 = Frame(tab2)
f21.pack()
f22.pack()
f23.pack()

l21 = Label(f21, text = 'Decrypt message', font = tabTitle)
l22 = Label(f22, text = 'Enter key for Caesar method')
e21 = Entry(f22)
b21 = Button(f22, text = 'Get the key and decrypt', command = Caesar_decrypt)
l23 = Label(f23, text = 'QDK-method decryption')
b22 = Button(f23, text = 'Decrypt', command = Unbreakable_decrypt)

l21.pack()
l22.pack()
e21.pack()
b21.pack()
l23.pack()
b22.pack()



#Here we write our Caesar cyphered message to file 


#We create a variable which will allow us to record data of encrypting 



############################################################################
import itertools


def Caesar_break():
    '''
    This program adds one number for every letter in message.
    '''
    with open ('Encrypted_Caesar.txt', 'r') as inf:
        message = ''.join(inf.readlines())
    ouf = open('Broken_Caesar.txt', 'w')
    for k in range(1, len(alphabet)):
        new_message = ''
        for symbol in message:
            if symbol in alphabet:
                index = alphabet.index(symbol)
                new_message += alphabet[(index + k) % len(alphabet)]
            else: mew_message += symbol
        ouf.write(new_message + '\n')
    l32.config(text = 'Caesar message is broken')


#Here we read the message cyphered with Quantum method.


def Super_break():
    l33.config(text = 'Breaking process has started')
    with open('QDK-message.txt', 'r') as inf:
        message = inf.readline()
    '''
    This program calculates all possible combinations
    with the message's length and symbols
    from our alphabet. This will be TOO slow for the long messages.
    '''
    s1 = 0
    for symbol in message:
        if symbol not in alphabet:
            s1 += 1
            break
    if s1 == 0:
        x = list(map(''.join, itertools.permutations(alphabet, len(message))))
    with open('Broken_QDK.txt', 'w') as ouf:
        ouf.write(str(x))
    l33.config(text = 'Breaking process was completed')

f31 = Frame(tab3)
f32 = Frame(tab3)
f31.pack()
f32.pack()

l31 = Label(f31, text = 'Breaking process', font = tabTitle)
l32 = Label(f32, text = 'Caesar breaking')
b31 = Button(f32, text = 'Break', command = Caesar_break)
l33 = Label(f32, text = 'QDK breaking')
b32 = Button(f32, text = 'Break', command = Super_break)

l31.pack()
l32.pack()
b31.pack()
l33.pack()
b32.pack()

window.mainloop()
