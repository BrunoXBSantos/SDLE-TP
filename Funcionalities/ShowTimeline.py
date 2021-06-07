# show own timeline
async def show_timeline(menu, timeline):
    menu.clear_screen()
    print('_______________ Timeline _______________')
    print("")
    for m in timeline:
        print(m['id'] + ' - ' + m['message'])
    print("")
    print('________________________________________')
    input('Press Enter')
    menu.clear_screen()
    return False