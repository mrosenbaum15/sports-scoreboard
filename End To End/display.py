import machine
import neopixel
import uasyncio as asyncio

chars = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '!': [0x00, 0x00, 0x5F, 0x00, 0x00],
    '&': [0x36, 0x49, 0x55, 0x22, 0x50],
    '\'': [0x00, 0x05, 0x03, 0x00, 0x00],
    '*': [0x08, 0x2A, 0x1C, 0x2A, 0x08],
    '+': [0x08, 0x08, 0x3E, 0x08, 0x08],
    ',': [0x00, 0x50, 0x30, 0x00, 0x00],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '/': [0x20, 0x10, 0x08, 0x04, 0x02],
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
    '2': [0x42, 0x61, 0x51, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    '<': [0x00, 0x08, 0x14, 0x22, 0x41],
    '=': [0x14, 0x14, 0x14, 0x14, 0x14],
    '>': [0x41, 0x22, 0x14, 0x08, 0x00],
    '?': [0x02, 0x01, 0x51, 0x09, 0x06],
    '@': [0x32, 0x49, 0x79, 0x41, 0x3E],
    'A': [0x7E, 0x11, 0x11, 0x11, 0x7E],
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7F, 0x41, 0x41, 0x22, 0x1C],
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7F, 0x09, 0x09, 0x01, 0x01],
    'G': [0x3E, 0x41, 0x41, 0x51, 0x32],
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3F, 0x01],
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7F, 0x02, 0x04, 0x02, 0x7F],
    'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E],
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
    'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
    'W': [0x7F, 0x20, 0x18, 0x20, 0x7F],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x03, 0x04, 0x78, 0x04, 0x03],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
    '^': [0x04, 0x02, 0x01, 0x02, 0x04],
    '_': [0x40, 0x40, 0x40, 0x40, 0x40],
    '|': [0x00, 0x00, 0x7F, 0x00, 0x00],
    '->': [0x08, 0x08, 0x2A, 0x1C, 0x08],
    '<-': [0x08, 0x1C, 0x2A, 0x08, 0x08]
}

class Display:
    """Drives the 40x16 LED Matrix.

    The main mode for the display will be a 1 pixel top and bottom border
    and 2 rows of 8 characters in the middle.

    Example:

    ________     ________
    BEARS WL     ILLINI W
      17-0       !!!!!!!!
    ________     ________

    Attributes:
        np (:obj: `NeoPixel`): The NeoPixel object to control the LEDs.
        numLit (int): Number of LEDs currently on.

    """

    def __init__(self, n=640, p=5):
        """Initiate the display.

        Args:
            n (int): Number of LEDs in the strip. Default is 640.
            p (int): GPIO number. Default is 5.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        self.np = neopixel.NeoPixel(machine.Pin(p), n)
        self.numLit = 0

    def clear(self):
        """Helper function to clear the display.

        Returns:
            True if successful, False otherwise.
        """
        for i in range(640):
            self.np[i] = (0,0,0)

        self.np.write()
        self.numLit = 0

        return True

    async def draw_character(self, char, position, color):
        """Helper function to update the neopixel array with bitmap data.

        Args:
            char: the character to draw.
            position: the position in the matrix to draw the character. (0-15)
            color: RGB color for the character

        Returns:
            True if successful, False otherwise.
        """

        if char not in chars:
            print('Invalid Char')
            return False

        ledIndexX = position % 8
        ledIndexY = (position // 8) * 7
        ledIndex = 40 + (ledIndexY * 40 + (ledIndexX * 5))

        for y in range(7):
            for x in range(5):
                curIndex = ledIndex + y*40 + x
                prevLit = (self.np[curIndex] != (0, 0, 0))

                if int('{0:08b}'.format(chars[char][x])[7 - y]):
                    self.np[curIndex] = color
                    if not prevLit:
                        self.numLit += 1
                else:
                    self.np[curIndex] = (0, 0, 0)
                    if prevLit:
                        self.numLit -= 1

        self.np.write()
        return True

    async def draw_line(self, lineChars, lineNumber, color):
        """Helper function to draw a line of characters to the LED Matrix.

        Args:
            lineChars: The characters to write to the line. (length 8)
            lineNumber: Which line to write to. (0-1)
            color: RGB color for the characters

        Returns:
            True if successful, False otherwise.
        """
        if len(lineChars) != 8:
            print('too long')
            return False

        for idx, char in enumerate(lineChars):
            if not await self.draw_character(char, idx + lineNumber*8, color):
                return False

        print('Number of LEDs lit:', self.numLit)

        return True

    def bounce_border(self, color, curLED, movingRight, prev):
        """Helper function to Draw a line of characters to the LED Matrix.

        Args:
            color: RGB color for the characters

        Returns:
            Does not return.
        """
        if prev != 'slow':
            for i in range(0,40):
                self.np[i] = (0,0,0)

            for i in range(600,640):
                self.np[i] = (0,0,0)

            self.np.write()

        if movingRight:
            self.np[curLED - 1] = (0,0,0)
            self.np[curLED - 1 + 600] = (0,0,0)
        else:
            self.np[curLED + 1] = (0,0,0)
            self.np[curLED + 1 + 600] = (0,0,0)

        self.np[curLED] = color
        self.np[curLED+600] = color

        self.np.write()

    def sound_border(self, color, audio_level):
        for i in range(40):
            if i < audio_level:
                self.np[i] = color
                self.np[i+600] = color
            else:
                self.np[i] = (0,0,0)
                self.np[i+600] = (0,0,0)

        self.np.write()

    def static_border(self, color1, color2):
        for i in range(0,40):
            self.np[i] = color2

        for i in range(600,640):
            self.np[i] = color2

        self.np.write()
