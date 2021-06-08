class Menu:
    def __init__(self, name):
        self.name = name

    def draw(self):
        print('_______________ ' + self.name + ' _______________')
        print("")
        print('     1 - Timeline')
        print('     2 - Subscribe username')
        print('     3 - Post message')
        print('     4 - Show Subscribers')
        print("")
        print('     0 - Exit')
        print("")
        print('_______________________________________________________________')

def clear_screen():
        for i in range(40):
            print()