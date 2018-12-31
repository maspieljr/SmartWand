from kano_wand.kano_wand import Shop, Wand, PATTERN
import moosegesture as mg
import time
import random
import math
import os


class GestureWand(Wand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Basic gesture dictionary
        # We use them as tuples so we can use them as keys
        self.gestures = {
            ("DL", "R", "DL"): "stupefy",
            ("DR", "R", "UR", "D"): "wingardium_leviosa",
            ("UL", "UR"): "reducio",
            ("DR", "U", "UR", "DR", "UR"): "flipendo",
            ("R", "D"): "expelliarmus",
            ("UR", "U", "D", "UL", "L", "DL"): "incendio",
            ("U", "U"): "lumos",
            ("D", "D"): "nox",
            ("U", "D", "DR", "R", "L"): "locomotor",
            ("DR", "DL"): "engorgio",
            ("UR", "R", "DR"): "aguamenti",
            ("UR", "R", "DR", "UR", "R", "DR"): "avis",
            ("D", "R", "U"): "reducto"
        }
        self.spell = None
        self.pressed = False
        self.positions = []

    def post_connect(self):
        self.subscribe_button()
        self.subscribe_position()

    def on_position(self, x, y, pitch, roll):
        if self.pressed:
            # While holding the button,
            #   append the position to the positions array
            self.positions.append(tuple([x, -1 * y]))

    def on_button(self, pressed):
        self.pressed = pressed

        if pressed:
            self.spell = None
        else:
            # If releasing the button, get the gesture
            gesture = mg.getGesture(self.positions)
            self.positions = []
            closest = mg.findClosestMatchingGesture(gesture, self.gestures, maxDifference=1)

            if closest != None:
                # Just use the first gesture in the list using the gesture key
                self.spell = self.gestures[closest[0]]
                self.vibrate(PATTERN.SHORT)
            # Print out the gesture
            print("{}: {}".format(gesture, self.spell))


def main():
    # Create the manager and shop to search for wands
    shop = Shop(wand_class=GestureWand)
    wands = []

    try:
        # Scan for wands until it finds some
        while len(wands) == 0:
            print("Scanning...")
            wands = shop.scan(connect=True)

        wand = wands[0]
        while wand.connected:
            # Make a random sleep and transition time
            sleep = random.uniform(0.1, 0.2)
#            transition = math.ceil(sleep * 10)
            if wand.spell == "lumos":
                print('lumos spell detected turn on tree')
                os.system('python3 ChristmasTree_on.py')
                wand.spell = None
            if wand.spell == "nox":
                print('mox spell detected turn off tree')
                os.system('python3 ChristmasTree_off.py')
                wand.spell = None
            time.sleep(sleep)


#    # Detect keyboard interrupt and disconnect wands, reset light
    except KeyboardInterrupt as e:
        for wand in wands:
            wand.disconnect()
#        manager.reset()


if __name__ == "__main__":
    main()
