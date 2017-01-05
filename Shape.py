import curses

class Shape(object):

    def __init__(self, shape_table, shape_name, shape_char):
        """ The shape_table is a list of 5 numbers.
        Each number defines one line in the 5x5
        shape table matrix.  The base two representation
        of the number defines if a pixel is on or off.
        """
        self.shape_table = list(shape_table)
        self.shape_dim = len(shape_table)
        self.shape_name = shape_name
        self.shape_char = shape_char

    def __str__(self):
        s = "shape_name: "+self.shape_name+"\n"
        s = s + "shape_char: "+self.shape_char
        return s

    def _draw_top(self, stdscr, y, x):
        stdscr.move(y, x)
        stdscr.addch(curses.ACS_ULCORNER)
        for i in range(self.shape_dim):
            stdscr.addch(curses.ACS_HLINE)
            if i<self.shape_dim-1:
                stdscr.addch(curses.ACS_TTEE)
            else: 
                stdscr.addch(curses.ACS_URCORNER)

    def _draw_row(self, stdscr, y, x, row):
        line = self.shape_table[row]
        stdscr.move(y, x)
        stdscr.addch(curses.ACS_VLINE)
        mask = 1 << (self.shape_dim-1)
        for i in range(self.shape_dim):
            if line & mask:
                stdscr.addch(curses.ACS_CKBOARD)
            else:
                stdscr.addch(' ')
            stdscr.addch(curses.ACS_VLINE)
            line = line << 1

    def _draw_sep(self, stdscr, y, x):
        stdscr.move(y, x)
        stdscr.addch(curses.ACS_LTEE)
        for i in range(self.shape_dim):
            stdscr.addch(curses.ACS_HLINE)
            if i<self.shape_dim-1:
                stdscr.addch(curses.ACS_PLUS)
            else:
                stdscr.addch(curses.ACS_RTEE)

    def _draw_bot(self, stdscr, y, x):
        stdscr.move(y, x)
        stdscr.addch(curses.ACS_LLCORNER)
        for i in range(self.shape_dim):
            stdscr.addch(curses.ACS_HLINE)
            if i<self.shape_dim-1:
                stdscr.addch(curses.ACS_BTEE)
            else: 
                stdscr.addch(curses.ACS_LRCORNER)

    def draw(self, stdscr, y, x):
        self._draw_top(stdscr,y,x)
        y = y + 1

        for row in range(self.shape_dim-1):
            self._draw_row(stdscr,y,x,row)
            y = y + 1
            self._draw_sep(stdscr,y,x)
            y = y + 1

        self._draw_row(stdscr,y,x,row+1)
        y = y + 1
        self._draw_bot(stdscr,y,x)

    def rotate(self):
        pass


def main(stdscr):

    # Turn off automatic echoing of keys
    curses.noecho()

    # Cbreak-mode.  Don't require return
    curses.cbreak()

    # Enable keypad mode. Get navigation keys
    stdscr.keypad(1)

    # Turn off the blinking cursor
    curses.curs_set(0)

    # Don't block for keyboard input
    stdscr.timeout(0)

    (height, width) = stdscr.getmaxyx()
    stdscr.addstr(0, 0, "window width :      ")
    stdscr.addstr(0, 16, str(width))
    stdscr.addstr(1, 0, "window height:      ")
    stdscr.addstr(1, 16, str(height))


    shape1 = Shape([0x04,0x04,0x04,0x04,0x04], "line", '1')
    shape1.draw(stdscr, 5, 5)

    shape2 = Shape([0x00,0x06,0x06,0x00], "square", '2')
    shape2.draw(stdscr, 5, 20)

    while True:


        ch = stdscr.getch()
        if ch == ord('q'):
            return

        curses.napms(100)


if __name__ == "__main__":
    curses.wrapper(main)

