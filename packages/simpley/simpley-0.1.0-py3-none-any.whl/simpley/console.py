import os

def write(*text):
	print("".join(text), end="")

def read():
	return input()

def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")