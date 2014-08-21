#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack import LEDBackpack

# ===========================================================================
# 7-Segment Display
# ===========================================================================

# This class is meant to be used with the four-character, seven segment
# displays available from Adafruit

class SevenSegment:
  disp = None
  invert = False

  # Hexadecimal character lookup table (row 1 = 0..9, row 2 = A..F)
  digits = [ 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F, \
             0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71 ]

  # The same, but upside-down
  idigits = [ 0x3F, 0x30, 0x5B, 0x79, 0x74, 0x6D, 0x6F, 0x38, 0x7F, 0x7D, \
              0x7E, 0x67, 0x0F, 0x73, 0x4F, 0x4E ]

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    self.disp = LEDBackpack(address=address, debug=debug)

  def writeDigitRaw(self, charNumber, value):
    "Sets a digit using the raw 16-bit value"
    if (charNumber > 7):
      return
    # Set the appropriate digit
    self.disp.setBufferRow(charNumber, value)

  def writeDigit(self, charNumber, value, dot=False):
    "Sets a single decimal or hexademical value (0..9 and A..F)"
    if (charNumber > 7):
      return
    if (value > 0xF):
      return

    # Decide which digit set to use: check self.invert
    d = self.idigits[value] if self.invert else self.digits[value]

    # If inverted, also reverse the character positions
    c = (4-charNumber) if self.invert else charNumber

    # Set the appropriate digit
    self.disp.setBufferRow(c, d | (dot << 7))

  def setColon(self, state=True):
    "Enables or disables the colon character"
    # Warning: This function assumes that the colon is character '2',
    # which is the case on 4 char displays, but may need to be modified
    # if another display type is used
    # This sets all non-digit LEDs.  Change (2,0xFFFF) to (2,2) to just
    # set colon on the 1.2" 7-Segment display.
    if (state):
      self.disp.setBufferRow(2, 0xFFFF)
    else:
      self.disp.setBufferRow(2, 0)

