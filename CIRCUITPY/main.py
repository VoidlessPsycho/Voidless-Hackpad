print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.scanners.keypad import KeysScanner
from kmk.modules.macros import Press, Release, Tap, Delay, Macros
from kmk.extensions.RGB import RGB
from kmk.modules.encoder import EncoderHandler
import busio

from kmk.extensions.display import Display, TextEntry, ImageEntry

# For SSD1306
from kmk.extensions.display.ssd1306 import SSD1306

# Replace SCL and SDA according to your hardware configuration.
i2c_bus = busio.I2C(board.GP6, board.GP5)

driver = SSD1306(
    # Mandatory:
    i2c=i2c_bus,

)

encoder_handler = EncoderHandler()

keyboard = KMKKeyboard()
    
keyboard.col_pins = (board.GP0,board.GP1, board.GP2)
keyboard.row_pins = (board.GP8,board.GP9, board.GP10)  
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Fixed keymap: flat layer with exactly 9 entries (3x3). 
# Use modifier combos directly (KC.LCMD(...)) instead of incorrect KC.MACRO(...) usage.
keyboard.keymap = [
    [  # layer 0 (flattened, row0 left→right, then row1, then row2)
        KC.NO, KC.NO, KC.ENT,          # row 0
        KC.LCMD(KC.TAB), KC.LCMD(KC.A), KC.LCMD(KC.BSPC),  # row 1
        KC.LCMD(KC.X), KC.LCMD(KC.C), KC.LCMD(KC.V),      # row 2
    ]
]

rgb = RGB(pixel_pin=board.GP11, num_pixels=6, hue=255, sat=255, val=50)
keyboard.extensions.append(rgb)

# Only include modules that are defined; remove undefined 'layers' and 'holdtap'
keyboard.modules = [encoder_handler]

encoder_handler.pins = (
    # regular direction encoder and a button
    (board.GP7, board.GP4, None), # encoder #1 
    )

Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)

encoder_handler.map = [( KC.VOLD, KC.VOLU), # encoder 1 map
                        (Zoom_out, Zoom_in)]

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
)
display.entries = [
    TextEntry(text="Hey there!", x=0, y=24),
]

if __name__ == '__main__':
    keyboard.go()