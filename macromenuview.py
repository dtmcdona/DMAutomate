import os

# The main purpose of this View is to show options to the user
# Basic editor/inserter allows user to edit macro without another program
# Most of this will be replaced/modified with a GUI at some point

class MacroMenuView:
    def __init__(self):
        # Action keeps track of current operation for the console
        self.action = "display"

    def display_menu(self):
        if self.action == "display":
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
        currentdir = os.path.dirname(os.path.abspath(__file__))+'\\'
        files = os.listdir(currentdir)
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

    def delete_input(self):
        self.action = "delete"
        print('What filename and extension would you like to delete')
        # Take input

    def insert_input(self, filename):
        self.action = "insert"
        inserting = True
        while inserting:
            print('What line of {0} do you want to insert code?'.format(filename))
            # Take input
            insert_line = 10
            print('Enter the line of code to insert. Make sure to use newline/tab characters.')
            # Take input
            user_input = "\t# Inserted here\n"
            # Read file and store in array
            lines = []
            currentdir = os.path.dirname(os.path.abspath(__file__)) + '\\'
            with open(r''+currentdir+filename, 'r') as file_input:
                lines = file_input.readlines()

            with open(r''+currentdir+filename, 'w') as file_input:
                for i, line in enumerate(lines):
                    if i not in [(insert_line-1)]:
                        file_input.write(line)
                    elif i is (insert_line-1):
                        file_input.write(user_input)

            file_input.close()
            print("Would you like to insert again? (y/n)")
            # Loop if 'y' or return to main menu but just quit for now
            inserting = False



# mmv = MacroMenuView()
# mmv.display_menu()
# mmv.display_list()
# mmv.display_file('dm_macro2.py')
# mmv.insert_input('dm_macro2.py')