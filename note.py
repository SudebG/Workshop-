import os

# Functions for CRUD operations
def add_note():
    note = input("Enter note: ")
    with open("notes.txt", "a") as f: f.write(note + "\n")

def view_notes():
    if os.path.exists("notes.txt"):
        with open("notes.txt", "r") as f: print(f.read())
    else: print("No notes.")

# Main loop
while True:
    choice = input("\n1.Add 2.View 3.Exit: ")
    if choice == '1': add_note()
    elif choice == '2': view_notes()
    elif choice == '3': break
