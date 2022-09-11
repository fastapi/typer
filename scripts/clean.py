from os import name,system

def clear():
    if name == 'nt':_ = system('cls')
    else : _ = system('clear')
