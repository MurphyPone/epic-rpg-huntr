from utils import *
from conf import *
import time
import random

gather_count = 0    # used to evenly distribute resource gathering

driver = build_driver()
login(driver)


while True:
   sixty_cycle(driver, gather_count, focus="wood")


