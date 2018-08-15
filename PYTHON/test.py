def Wysylanie():
    print("Wysylanie() start")

    e = 50.8474756930
    b = 20.034
    c = 60
    distLeft = min(e, 60)
    distFront = min(int(b), 40)
    distRight = min(c, 40)

    print(f"Left sensor: {distLeft}")
    print(f"Front sensor: {distFront}")
    print(f"Right sensor: {distRight}")

    #sock.send(json.dumps([distLeft, distFront, distRight]).encode())

    print("Wysylanie() end")

Wysylanie()