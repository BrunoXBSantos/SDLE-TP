import json


async def getSubscribers(server, username, menu):
    result = await server.get(username)
    print("SSSSSSSSSSSSSSSSSSSSSSS")
    print(result)
    result2 = json.loads(result)
    subscribers = result2["subscribers"]
    print(subscribers)
    menu.clear_screen()
    print("-----------------------------------------")
    print(" 2 - Subscribers")
    print('')
    for s in subscribers:
        print("\t" + s)
    print("")
    print("-----------------------------------------")
    input('Press Enter to return')
    menu.clear_screen()
    return True
