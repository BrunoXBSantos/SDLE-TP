# show own timeline
async def see_timeline(menu, timeline):
    menu.clear_screen()
    print("-----------------------------------------")
    print(" 1 - Timeline")
    print('')
    print(" Username\t\tPost")
    print('')
    print("")
    for m in timeline:
        print("    "+m['id'] + "\t\t      " + m['message'])
    print("")
    print("-----------------------------------------")
    input('Press Enter to return')
    menu.clear_screen()
    return False