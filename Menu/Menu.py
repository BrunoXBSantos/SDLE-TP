class Menu:
    def __init__(self, name, items=None):
        self.name = name

    def draw(self):
        print('_______________ ' + self.name + ' _______________')
        print("")
        print('     1 - Timeline')
        print('     2 - Subscribe username')
        print('     3 - Post message')
        print("")
        print('     0 - Exit')
        print("")
        print('___________________________________________________')

def clear_screen():
    for i in range(40):
        print()
