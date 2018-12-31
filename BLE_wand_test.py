from kano_wand.kano_wand import Shop, Wand, PATTERN
import moosegesture as mg
import time
import random
import math

class GestureWand(Wand):
    def post_connect(self):
        print(self.name)
shop = Shop(wand_class=GestureWand)
wands = []
while len(wands) == 0:
    print("Scanning...")
    wands = shop.scan(connect=True)
for wand in wands:
    wand.disconnect()
