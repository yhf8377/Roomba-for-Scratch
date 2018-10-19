import time

import hardware.RoombaOI as OI
import hardware.RaspberryPi as PI

pi = PI.UARTDevice()
roomba = OI.RoombaOI(pi)

roomba.set_mode(OI.Mode.Safe)

# Replace song #4 with Old McDondald Had A Farm
roomba.set_song(1,
    # C   C   C   G   A   A   G   E   E   D   D   C
    [60, 60, 60, 55, 57, 57, 55, 64, 64, 62, 62, 60],
    [32, 32, 32, 32, 32, 32, 64, 32, 32, 32, 32, 64]
)

roomba.play_song(1)

roomba.drive(velocity=0, radius=1)
time.sleep(1)
roomba.drive(velocity=0, radius=-1)
time.sleep(1)
roomba.drive(velocity=0, radius=1)
time.sleep(1)
roomba.drive(velocity=0, radius=-1)
time.sleep(1)
roomba.drive(velocity=0, radius=1)
time.sleep(3)

roomba.set_mode(OI.Mode.Off)
