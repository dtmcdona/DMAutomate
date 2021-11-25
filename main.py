import macrofilecontroller
import macromenuview

class App:
    def __init__(self):
        self.action = "display"
        self.running = True
        self.currentfile = "dm_macro.py"

    def run_app(self):
        view = macromenuview.MacroView()
        controller = macrofilecontroller.MacroController()
        self.action = view.display_menu()
        print("Action is: "+self.action)
        while self.running:
            if self.action == "create":
                print("Would you like to save your current macro before loading? (y/n)")
                user_input = input().lower()
                if user_input == 'y' or user_input == 'yes':
                    print("What do you want to name it? (not including .py ext)")
                    filename_input = input()
                    controller.save(filename_input)
                    controller.create_macro()
                else:
                    controller.create_macro()
            elif self.action == "open":
                print("Would you like to save your current macro before loading? (y/n)")
                user_input = input().lower()
                if user_input == 'y' or user_input == 'yes':
                    print("What do you want to name it? (not including .py ext)")
                    filename_input = str(input())
                    controller.save_macro(filename_input)

                pyfiles = view.display_list()
                print('| Which index would you like to open? |')
                user_input = int(input())
                filename = pyfiles[user_input]
                controller.open_macro(filename)
            elif self.action == "edit":
                pyfiles = view.display_list()
                print('| Which index would you like to open? |')
                user_input = int(input())
                filename = str(pyfiles[user_input])
                view.display_file(filename)
                view.insert_input(filename)
            elif self.action == "save":
                print("What do you want to name it? (not including .py ext)")
                filename_input = str(input())
                controller.save_macro(filename_input)
            elif self.action == "delete":
                view.delete_input()
            elif self.action == "insert":
                view.display_file(self.currentfile)
                view.insert_input(self.currentfile)
            elif self.action == "record":
                print("Recording... (press 'Esc' to exit to main menu)")
                if not controller.listeners:
                    controller.activate_listeners()
                controller.running = True
                while controller.running:
                    pass
            elif self.action == "play":
                controller.play()
            elif self.action == "view":
                pyfiles = view.display_list()
                print('| Which index would you like to view? |')
                user_input = int(input())
                filename = pyfiles[user_input]
                view.display_file(filename)
            elif self.action == "settings":
                print('| Would you like random time intervals added between actions? (y/n)|')
                user_input = input().lower()
                if user_input == 'y' or user_input == 'yes':
                    controller.randomEnabled = True

            self.action = view.display_menu()
            print("Action is: " + self.action)



run = App()
App().run_app()