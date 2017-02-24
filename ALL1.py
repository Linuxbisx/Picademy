from threading import Thread

from mcpi.minecraft import Minecraft

from w1thermsensor import W1ThermSensor


from time import sleep

from gpiozero import LED

from gpiozero import Button

from signal import pause

mc = Minecraft.create()

## Setup buttons -> pins
fwdButton = Button(19)
backButton = Button(16)
leftButton = Button(13)
rightButton = Button(20)

x, y, z = mc.player.getPos()

def moveFwd():
    ## Function: move player forward
    ##print("fwdButton pressed")
    global x, y, z
    fwdBlock = mc.getBlock(x, y, z+1)
    if fwdBlock == 0:
        mc.player.setPos(x, y, z+1)
        x, y, z = mc.player.getPos()

def moveBack():
    ## Function: move player back
    ##print("backButton pressed")
    global x, y, z
    fwdBlock = mc.getBlock(x, y, z-1)   
    if fwdBlock == 0:
        mc.player.setPos(x, y, z-1)
        x, y, z = mc.player.getPos()

def moveLeft():
    ## Function: move player left
    ##print("leftButton pressed")
    global x, y, z
    fwdBlock = mc.getBlock(x-1, y, z)
    if fwdBlock == 0:
        mc.player.setPos(x-1, y, z)
        x, y, z = mc.player.getPos()

def moveRight():
    ## Function: move player right
    ##print("rightButton pressed")
    global x, y, z
    fwdBlock = mc.getBlock(x+1, y, z)
    if fwdBlock == 0:
        mc.player.setPos(x+1, y, z)
        x, y, z = mc.player.getPos()


def handle_lights():

    r = LED(17)
    a = LED(27)
    g = LED(22)

    air = 0 # light up red
    sand = 12 # light up amber
    grass = 2 # light up green

    sleep(2)

    x, y, z = mc.player.getPos()

    block_below = mc.getBlock(x, y-1, z)

    while True:

        #print("i'm walking on..." + str(block_below))
        
        
        if block_below == air:
            r.on()
        else:
            r.off()

        if block_below == sand:
            a.on()
        else:
            a.off()

        if block_below == grass:
            g.on()
        else:
            g.off()
            
        sleep(0.1)
        x, y, z = mc.player.getPos()
        block_below = mc.getBlock(x, y-1, z)

def handle_temperature():

    print("in temp")

    sensor = W1ThermSensor()

    temp = sensor.get_temperature()

    tempread = (int(float(temp)))

    block = 1

    #this_block = mc.getBlock(x, y, z) ##Get what block the user is on

    x, y, z = mc.player.getPos()
    x+=5
    z=z+15

    while True:
        temp = sensor.get_temperature()
        tempread = (int(float(temp)))
        x+=1
        
        for upwards in range(tempread):
            if (upwards < 22):
                block = 12
            elif (upwards < 24):
                block = 1
            else:
                block = 46
            mc.setBlock(x, upwards, z, block)




def handle_movement():
    print("hi")
    ## message ready to player   
    mc.postToChat("External control ENABLED.")

    ## move player forward
    fwdButton.when_pressed = moveFwd

    ## move player back
    backButton.when_pressed = moveBack

    ## move player left
    leftButton.when_pressed = moveLeft

    ## move player right
    rightButton.when_pressed = moveRight






if __name__ == '__main__':
    Thread(target = handle_lights).start()
    Thread(target = handle_movement).start()
    Thread(target = handle_temperature).start()
    
    
