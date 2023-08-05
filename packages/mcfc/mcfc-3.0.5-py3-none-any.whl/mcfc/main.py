# main.py
# Text formatting using Minecraft color codes.
# https://github.com/woidzero/MCFC.git

from __future__ import annotations

import os
import sys

if sys.platform.lower() == "win32": 
    os.system('color')


BLACK = '\x1b[30m'
WHITE = '\x1b[97m'
DARK_RED = '\x1b[31m'
DARK_GREEN = '\x1b[32m'
DARK_YELLOW = '\x1b[33m'
DARK_BLUE = '\x1b[34m'
DARK_PURPLE = '\x1b[35m'
DARK_AQUA = '\x1b[36m'
GRAY = '\x1b[37m'
DARK_GRAY = '\x1b[90m'

RED = '\x1b[91m'
GREEN = '\x1b[92m'
YELLOW  = '\x1b[93m'
BLUE  = '\x1b[94m'
PURPLE = '\x1b[95m'
AQUA  = '\x1b[96m'

OBFUSCATED = "\x1b[8m"
BOLD = '\x1b[1m'
STRIKETHROUGH = '\x1b[9m'
UNDERLINE = '\x1b[4m'
ITALIC = '\x1b[3m'
RESET = '\x1b[0m'

BLINK = "\x1b[5m"
OVERLINE = "\x1b[53m"
DOUBLE_UNDERLINE = "\x1b[21m"
INVERT = "\x1b[7m"


colorCodes = {
    "&0": BLACK,          "&f": WHITE,
    "&8": DARK_GRAY,      "&7": GRAY,
    "&1": DARK_BLUE,      "&9": BLUE,
    "&2": DARK_GREEN,     "&a": GREEN,
    "&3": DARK_AQUA,      "&b": AQUA,
    "&4": DARK_RED,       "&c": RED,
    "&5": DARK_PURPLE,    "&d": PURPLE,
    "&6": DARK_YELLOW,    "&e": YELLOW,
    "&r": RESET,
    "&l": BOLD,
    "&n": UNDERLINE,
    "&m": STRIKETHROUGH,
    "&o": ITALIC,
    "&k": OBFUSCATED,
    "&j": BLINK,
    "&p": OVERLINE,
    "&w": DOUBLE_UNDERLINE,
    "&i": INVERT
}


def echo(*values, sep: str = ' ') -> None:
    """Prints the colored text to a command prompt or terminal.

    ### Arguments
    sep (str): 
        separator between strings. Defaults a space.
    end (str): 
        string appended after the last value. Defaults a newline.
    """
    text = sep.join(tuple(map(str, values)))

    for code in colorCodes:
        text = text.replace(code, RESET + colorCodes[code])

    sys.stdout.write(u"{}".format(text) + RESET)


def info():
    """
    Prints all available formatting codes.
    """
    echo("""
    Text can be formatted using the section sign (&) followed by a character.
    ----- Default formatting codes:
    &00            &88            &77            &ff
    &11            &99            &22            &aa
    &33            &bb            &44            &cc
    &55            &dd            &66            &ee
    &rr (reset)&r                 &ll (bold)&r
    &nn (underline)&r             &oo (italic)&r
    &mm (strikethrough)&r             

    ----- Custom formatting codes (not widely supported):
    &jj (blink)&r                 &pp (overline)&r
    &ww (double underline)&r      &ii (invert)&r
    """)