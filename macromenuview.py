import os
from sys import platform

# The main purpose of this View is to show options to the user
# Basic editor/inserter allows user to edit macro without another program
# Most of this will be replaced/modified with a GUI at some point

class MacroMenuView:
    def __init__(self):
        # Action keeps track of current operation for the console
        self.action = "display"
        self.editing = False
        if platform == "linux" or platform == "linux2":
            self.currentdir = os.path.dirname(os.path.abspath(__file__)) + '/'
        elif platform == "win32":
            self.currentdir = os.path.dirname(os.path.abspath(__file__)) + '\\'

    def display_menu(self):
        self.action == "display"
        print('|========== -(Main menu)- ==========|')
        print('|   Hotkeys      |     Options      |')
        print('|-----------------------------------|')
        print('|  1  | Create Macro...             |')
        print('|  2  | Open macro...               |')
        print('|  3  | Edit macro...               |')
        print('|  4  | Save macro as...            |')
        print('|  5  | Delete macro...             |')
        print('|  6  | Insert into current macro   |')
        print('|  7  | Continue recording          |')
        print('|===================================|')

    def display_list(self):
        self.action = "list"
        print('|========== -(File list)- ==========|')
        files = os.listdir(self.currentdir)
        pyfiles = []
        counter = 0
        # Maybe give macros a unique identifier to only show macros
        for f in files:
            if '.py' in f:
                print('| Index '+str(counter)+' | '+str(f))
                pyfiles.append(str(f))
                counter += 1

    def display_file(self, filename):
        self.action = "file"
        print('|========== -('+filename+')- ==========|')
        with open(filename) as input_file:
            for i, line in enumerate(input_file):
                print("{0} |".format(i+1)+line, end=""),
        print("|There are {0} lines of code in ".format(i+1)+filename+"|")
        print('|===================================|')
        input_file.close()

    def create_input(self):
        self.action = "create"
        print('What filename and extension would you like to use?')
        # Take input
        user_input = input()
        return user_input

    def delete_input(self):
        self.action = "delete"
        print('What filename and extension would you like to delete?')
        # Take input
        user_input = input()
        if os.path.exists(user_input):
            os.remove(user_input)
        else:
            print("That file does not exist.")

    def insert_input(self, filename):
        self.action = "insert"
        self.editing = True
        while self.editing:
            print('What line of {0} do you want to insert code?'.format(filename))
            # Take input
            insert_line = int(input())
            if insert_line < 1:
                print('Cannot do less than line 1.  What line of {0} do you want to insert code?')
                # Take input
                insert_line = int(input())
            print('Enter the line of code to insert.')
            # Take input
            user_input = input()+'\n'
            print('How many tabs for this line of code?')
            tabs_input = int(input())
            while tabs_input > 0:
                user_input = '\t'+user_input
                tabs_input -= 1
            # Read file and store in array
            lines = []
            with open(r''+self.currentdir+filename, 'r') as file_input:
                lines = file_input.readlines()

            with open(r''+self.currentdir+filename, 'w') as file_input:
                for i, line in enumerate(lines):
                    if i not in [(insert_line-1)]:
                        file_input.write(line)
                    elif i is (insert_line-1):
                        file_input.write(user_input)

            file_input.close()
            print("Would you like to insert again? (y/n)")
            # Loop if 'y' or return to main menu but just quit for now
            user_input = input()
            if user_input == 'y' or user_input == 'yes':
                self.editing = True
            elif user_input == 'n' or user_input == 'no':
                self.editing = False
            else:
                self.editing = False



mmv = MacroMenuView()
mmv.display_menu()
mmv.display_list()
mmv.display_file('dm_macro.py')
mmv.insert_input('dm_macro.py')