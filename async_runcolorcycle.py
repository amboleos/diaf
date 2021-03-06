#!/usr/bin/env python3
"""Sample script to run a few colour tests on the strip."""
from apa102_pi.colorschemes import colorschemes

from apa102_pi.driver import colorcycletemplate
from apa102_pi.driver import apa102

import asyncio

NUM_LED = 430

# # One Cycle with one step and a pause of three seconds. Hence three seconds of white light
# print('Three Seconds of white light')
# MY_CYCLE = colorschemes.Solid(num_led=NUM_LED, pause_value=3,
#                               num_steps_per_cycle=1, num_cycles=1)
# MY_CYCLE.start()

# # Go twice around the clock
# print('Go twice around the clock')
# MY_CYCLE = colorschemes.RoundAndRound(num_led=NUM_LED, pause_value=0,
#                                       num_steps_per_cycle=NUM_LED, num_cycles=2)
# MY_CYCLE.start()

# # One cycle of red, green and blue each
# print('One strandtest of red, green and blue each')
# MY_CYCLE = colorschemes.StrandTest(num_led=NUM_LED, pause_value=0,
#                                    num_steps_per_cycle=NUM_LED, num_cycles=3)
# MY_CYCLE.start()

# # One slow trip through the rainbow
# print('One slow trip through the rainbow')
# MY_CYCLE = colorschemes.Rainbow(num_led=NUM_LED, pause_value=0,
#                                 num_steps_per_cycle=255, num_cycles=1)
# MY_CYCLE.start()

# # Five quick trips through the rainbow
# print('Five quick trips through the rainbow')
# MY_CYCLE = colorschemes.TheaterChase(num_led=NUM_LED, pause_value=0.04,
#                                      num_steps_per_cycle=35, num_cycles=5)
# MY_CYCLE.start()

# print('Finished the test')

class Solid_Async (colorschemes.Solid):
    async def start(self):
        """This method does the actual work."""
        strip = None
        try:
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            while True:  # Loop forever
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    await asyncio.sleep(self.pause_value)
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)

class RoundAndRound_Async (colorschemes.RoundAndRound):
    async def start(self):
        """This method does the actual work."""
        strip = None
        try:
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            while True:  # Loop forever
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    await asyncio.sleep(self.pause_value)
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)

class StrandTest_Async (colorschemes.StrandTest):
    async def start(self):
        """This method does the actual work."""
        strip = None
        try:
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            while True:  # Loop forever
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    await asyncio.sleep(self.pause_value)
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)

class Rainbow_Async (colorschemes.Rainbow):
    async def start(self):
        """This method does the actual work."""
        strip = None
        try:
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            while True:  # Loop forever
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    await asyncio.sleep(self.pause_value)
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)

class TheaterChase_Async (colorschemes.TheaterChase):
    async def start(self):
        """This method does the actual work."""
        strip = None
        try:
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            # strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            while True:  # Loop forever
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    await asyncio.sleep(self.pause_value)
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            # self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)

class Solid_Green_Async (colorschemes.Solid):

    def update(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        stripcolour = 0xFF00FF
        if current_step == 1:
            stripcolour = 0xFF0000
        if current_step == 2:
            stripcolour = 0x00FF00
        if current_step == 3:
            stripcolour = 0x0000FF
        for led in range(0, num_led):
            strip.set_pixel_rgb(led, stripcolour, 5)  # Paint 5% white
        return 1

    async def start(self):
        """This method does the actual work."""
        strip = None
        try:
            strip = apa102.APA102(num_led=self.num_led,
                                  global_brightness=self.global_brightness,
                                  mosi=self.mosi, sclk=self.sclk,
                                  order=self.order)  # Initialize the strip
            strip.clear_strip()
            self.init(strip, self.num_led)  # Call the subclasses init method
            strip.show()
            current_cycle = 0
            while True:  # Loop forever
                for current_step in range(self.num_steps_per_cycle):
                    need_repaint = self.update(strip, self.num_led,
                                               self.num_steps_per_cycle,
                                               current_step, current_cycle)
                    if need_repaint:
                        strip.show()  # repaint if required
                    await asyncio.sleep(self.pause_value)
                current_cycle += 1
                if self.num_cycles != -1:
                    if current_cycle >= self.num_cycles:
                        break
            # Finished, cleanup everything
            self.cleanup(strip)

        except KeyboardInterrupt:  # Ctrl-C can halt the light program
            print('Interrupted...')
            if self.cleanup is not None:
                self.cleanup(strip)




async def print_some():
    while True:
        await asyncio.sleep(.1)
        print("yes")

# idle = Solid_Async (num_led=NUM_LED, pause_value=3,
#                               num_steps_per_cycle=1, num_cycles=1)
# error = RoundAndRound_Async (num_led=NUM_LED, pause_value=0,
#                                       num_steps_per_cycle=NUM_LED, num_cycles=2)
# MY_CYCLE3 = StrandTest_Async (num_led=NUM_LED, pause_value=0,
#                                    num_steps_per_cycle=NUM_LED, num_cycles=3)
# loading = Rainbow_Async (num_led=NUM_LED, pause_value=0,
#                                 num_steps_per_cycle=255, num_cycles=1)
# connecting = TheaterChase_Async (num_led=NUM_LED, pause_value=0.04,
#                                      num_steps_per_cycle=35, num_cycles=5)


# # One cycle of red, green and blue each
# print('One strandtest of red, green and blue each')
# MY_CYCLE = CT_Async(num_led=NUM_LED, pause_value=0,
#                                    num_steps_per_cycle=NUM_LED, num_cycles=3)


# async def main ():
#     print("efe")
#     await asyncio.gather(
#             MY_CYCLE3.start(),
#             print_some(),
#             )
# asyncio.run(main())
