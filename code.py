import usb_hid
from adafruit_hid.keyboard import Keyboard
from keycode_win_be import Keycode # import your local keymap or use from adafruit_hid.keycode import Keycode for US
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import board
import digitalio
import time
import microcontroller


# Function to set a pin as an input (external pullup is soldered to the board) so it's high unless grounded by a key press
def go_z(p):
    pins[p].direction = digitalio.Direction.INPUT #set as input
    pins[p].pull = None

# Function to set a pin as an output and drive it to a logic low (0 volts)
def go_0(p):
    pins[p].pull = None                            #disable pullup
    pins[p].direction = digitalio.Direction.OUTPUT #set as output
    pins[p].value = 0                              #drive low


# definition of matrix keymap (which pin connection belongs to which key). YOURS WILL BE DIFFERENT
keymap=[
    [ 3, 21, Keycode.LEFT_CONTROL, Keycode.LEFT_CONTROL ],
    [ 5, 19, Keycode.LEFT_SHIFT, Keycode.LEFT_SHIFT ],
    [ 5, 16, Keycode.RIGHT_SHIFT, Keycode.RIGHT_SHIFT ],
    [ 10, 23, Keycode.ALT, Keycode.ALT ],
    [ 10, 20, Keycode.ALTGR, Keycode.ALTGR ],
    [ 11, 22, Keycode.WINDOWS, Keycode.WINDOWS ],
    [ 0, 17, 0, 0 ], #this is the FN key - it isn't reported via USB, but handeled internally
    [ 14, 20, Keycode.A, Keycode.A ],
    [ 6, 17, Keycode.B, Keycode.B ],
    [ 2, 18, Keycode.C, Keycode.C ],
    [ 2, 19, Keycode.D, Keycode.D ],
    [ 2, 20, Keycode.E, Keycode.E ],
    [ 6, 18, Keycode.F, Keycode.F ],
    [ 6, 19, Keycode.G, Keycode.G ],
    [ 0, 21, Keycode.H, Keycode.H ],
    [ 4, 20, Keycode.I, Keycode.KEYPAD_FIVE ],
    [ 7, 18, Keycode.J, Keycode.KEYPAD_ONE ],
    [ 4, 19, Keycode.K, Keycode.KEYPAD_TWO ],
    [ 8, 19, Keycode.L, Keycode.KEYPAD_THREE ],
    [ 9, 19, Keycode.M, Keycode.KEYPAD_PLUS ],
    [ 7, 17, Keycode.N, Keycode.N ],
    [ 8, 20, Keycode.O, Keycode.KEYPAD_SIX ],
    [ 9, 20, Keycode.P, Keycode.KEYPAD_MINUS ],
    [ 14, 19, Keycode.Q, Keycode.Q ],
    [ 6, 22, Keycode.R, Keycode.R ],
    [ 1, 19, Keycode.S, Keycode.S ],
    [ 6, 20, Keycode.T, Keycode.T ],
    [ 7, 22, Keycode.U, Keycode.KEYPAD_FOUR ],
    [ 0, 16, Keycode.V, Keycode.V ],
    [ 14, 18, Keycode.W, Keycode.W ],
    [ 1, 18, Keycode.X, Keycode.X ],
    [ 0, 23, Keycode.Y, Keycode.Y ],
    [ 13, 17, Keycode.Z, Keycode.Z ],
    [ 14, 22, Keycode.ONE, Keycode.ONE ],
    [ 1, 22, Keycode.TWO, Keycode.TWO ],
    [ 2, 22, Keycode.THREE, Keycode.THREE ],
    [ 6, 21, Keycode.FOUR, Keycode.FOUR ],
    [ 6, 23, Keycode.FIVE, Keycode.FIVE ],
    [ 7, 21, Keycode.SIX, Keycode.SIX ],
    [ 7, 23, Keycode.SEVEN, Keycode.KEYPAD_SEVEN ],
    [ 4, 22, Keycode.EIGHT, Keycode.KEYPAD_EIGHT ],
    [ 8, 22, Keycode.NINE, Keycode.KEYPAD_NINE ],
    [ 9, 23, Keycode.ZERO, Keycode.KEYPAD_ASTERISK ],
    [ 12, 22, Keycode.MINUS, Keycode.MINUS ],
    [ 9, 18, Keycode.EQUALS, Keycode.KEYPAD_FORWARD_SLASH ],
    [ 12, 20, Keycode.BACKSPACE, Keycode.BACKSPACE ],
    [ 14, 23, Keycode.ESCAPE, Keycode.ESCAPE ],
    [ 1, 23, Keycode.F1, Keycode.F1 ],
    [ 1, 21, Keycode.F2, Keycode.F2 ],
    [ 2, 21, Keycode.F3, Keycode.F3 ],
    [ 2, 23, Keycode.F4, Keycode.F4 ],
    [ 4, 23, Keycode.F5, Keycode.F5 ],
    [ 4, 21, Keycode.F6, Keycode.F6 ],
    [ 8, 21, Keycode.F7, Keycode.F7 ],
    [ 8, 23, Keycode.F8, Keycode.F8 ],
    [ 9, 21, Keycode.F9, Keycode.F9 ],
    [ 12, 21, Keycode.F10, Keycode.F10 ],
    [ 12, 23, Keycode.F11, Keycode.F11 ],
    [ 13, 21, Keycode.F12, Keycode.F12 ],
    [ 13, 23, Keycode.INSERT, Keycode.INSERT ],
    [ 15, 23, Keycode.DELETE, Keycode.DELETE ],
    [ 14, 21, Keycode.HOME, Keycode.HOME ],
    [ 15, 16, Keycode.PAGE_UP, Keycode.PAGE_UP ],
    [ 15, 22, Keycode.PAGE_DOWN, Keycode.PAGE_DOWN ],
    [ 14, 16, Keycode.END, Keycode.END ],
    [ 13, 16, Keycode.RIGHT_ARROW, Keycode.RIGHT_ARROW ],
    [ 13, 18, Keycode.LEFT_ARROW, Keycode.LEFT_ARROW ],
    [ 13, 19, Keycode.UP_ARROW, Keycode.UP_ARROW ],
    [ 12, 17, Keycode.DOWN_ARROW, Keycode.DOWN_ARROW ],
    [ 15, 20, Keycode.APPLICATION, Keycode.APPLICATION ],
    [ 8, 18, Keycode.FORWARD_SLASH, Keycode.KEYPAD_PERIOD ],
    [ 7, 16, Keycode.COMMA, Keycode.KEYPAD_ZERO ],
    [ 4, 18, Keycode.PERIOD, Keycode.PERIOD ],
    [ 13, 20, Keycode.ENTER, Keycode.ENTER ],
    [ 0, 19, Keycode.CAPS_LOCK, Keycode.CAPS_LOCK ],
    [ 0, 20, Keycode.TAB, Keycode.TAB ],
    [ 12, 16, Keycode.SPACEBAR, Keycode.SPACEBAR ],
    [ 8, 17, Keycode.PRINT_SCREEN, Keycode.PRINT_SCREEN ],
    [ 13, 22, Keycode.KEYPAD_NUMLOCK, Keycode.KEYPAD_NUMLOCK ],
    [ 0, 22, Keycode.OEM_102, Keycode.OEM_102 ],
    [ 8, 16, Keycode.SCROLL_LOCK, Keycode.SCROLL_LOCK ],
    [ 15, 21, Keycode.PAUSE, Keycode.PAUSE ],
    [ 9, 22, Keycode.LEFT_BRACKET, Keycode.LEFT_BRACKET ],
    [ 12, 22, Keycode.MINUS, Keycode.MINUS ],
    [ 12, 19, Keycode.ACCENT_CIRCONFLEXE, Keycode.ACCENT_CIRCONFLEXE ],
    [ 12, 18, Keycode.SEMICOLON, Keycode.SEMICOLON ],
    [ 9, 16, Keycode.ACCENT_AIGU, Keycode.ACCENT_AIGU ],
    [ 15, 19, Keycode.ACCENT_GRAVE, Keycode.ACCENT_GRAVE ]
]
#list that saves the current state of each key, 1 = released, 0 = pressed
keystatus = [1] * len(keymap)

#try connecting to USB HID, if it fails, reset and try again after 15 seconds.
#(this is needed in my environment because USB devices aren't accepted for the first few seconds)
try:
    kbd = Keyboard(usb_hid.devices)
    cc = ConsumerControl(usb_hid.devices)
except:
    print("USB error! Restarting in 15 seconds")
    time.sleep(15)
    microcontroller.reset()

#which pins is the keyboard ribbon connector connected to?
KBD_pinnumbers = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10,
                  board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20,
                  board.GP21, board.GP22, board.GP26]

pins = []
for x,p in enumerate(KBD_pinnumbers):
    pins.append(digitalio.DigitalInOut(p))


#set each pin as input
for p in range(23):
    go_z(p)


while True:
    for idx, line in enumerate(keymap): #check each possible combination
        go_0(line[0])
        reading = pins[line[1]].value #pull down, read, pull up
        go_z(line[0])

        if not keystatus[idx] == reading: #key status changed, report it to USB HID keyboard
            keystatus[idx] = reading
            report = (not line[2] == 0) #FN key isn't reported via USB but handled directly on the pico

            if keystatus[6] == 0 and reading == 0: #If FN button is pressed too, handle it as FN-Combination (only on key down)
                report = False
                # customize these FN-combination responses to your liking
                if line[2] == Keycode.F6: #mute / unmute
                    cc.send(ConsumerControlCode.MUTE)
                if line[2] == Keycode.F8:
                    cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
                if line[2] == Keycode.F9:
                    cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
                if line[2] == Keycode.F10: #volume down
                    cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                if line[2] == Keycode.F11: #volume up
                    cc.send(ConsumerControlCode.VOLUME_INCREMENT)


            if report:
                #new code for NumLock
                keycode_to_use = line[2]
                
                if kbd.led_on(Keyboard.LED_NUM_LOCK):
                    keycode_to_use = line[3]
                #end new code for NumLock
                
                if reading == 0: #New key pressed
                    kbd.press(keycode_to_use)
                else: #Key released
                    kbd.release(keycode_to_use)
