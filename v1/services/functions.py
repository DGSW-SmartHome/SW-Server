def getLightStatus(light):
    light1 = False
    light2 = False
    if light is 0:
        pass
    elif light is 1:
        light1 = True
        light2 = False
    elif light is 2:
        light1 = False
        light2 = True
    elif light is 3:
        light1 = True
        light2 = True
    return {
        "light1": light1,
        "light2": light2
    }
