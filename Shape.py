import curses
import copy

class Shape(object):

    def __init__(self, shape_def, shape_name, shape_char):
        """ The shape_def is a list of 5 numbers.
        Each number defines one line in the 5x5
        shape table matrix.  The base two representation
        of the number defines if a pixel is on or off.
        """
        self.shape_table = []
        self.shape_dim = len(shape_def)
        self.shape_name = shape_name
        self.shape_char = shape_char

        # Create shape_table from the shape_def.
        # shape_table is a list of lists.
        # The 1st dimension specifies the line (row).
        # The 2nd dimension specifies the pixel in the line (column).
        # (0,0) is the upper left corner.
        # A value of 1 indicates the pixel is set.
        # A value of 0 indicates the pixel is not set.
        for line in shape_def:
            line_list = []
            mask = 0x01
            for i in range(self.shape_dim):
                if line & mask:
                    line_list.append(1)
                else:
                    line_list.append(0)
                line = line >> 1
            line_list.reverse()
            self.shape_table.append(line_list)


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
        for pixel in line:
            if pixel==1:
                stdscr.addch(curses.ACS_CKBOARD)
            else:
                stdscr.addch(' ')
            stdscr.addch(curses.ACS_VLINE)

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

    def rotate_cw(self):
        rot_shape = copy.deepcopy(self.shape_table)
        for y in range(self.shape_dim):
            for x in range(self.shape_dim):
                ry = x
                rx = (self.shape_dim - 1) - y
                rot_shape[ry][rx] = self.shape_table[y][x]
        self.shape_table = rot_shape

    def reflect(self):
        reflect_shape = copy.deepcopy(self.shape_table)
        for y in range(self.shape_dim):
            for x in range(self.shape_dim):
                ry = y
                rx = (self.shape_dim - 1) - x
                reflect_shape[ry][rx] = self.shape_table[y][x]
        self.shape_table = reflect_shape


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

    shape3 = Shape([0x04,0x06,0x06,0x00], "six", '3')
    shape3.draw(stdscr, 5, 35)

    trans = 0
    while True:


        ch = stdscr.getch()
        if ch == ord('q'):
            return
        elif ch == ord('r'):
            if trans == 3:
                shape1.rotate_cw()
                shape2.rotate_cw()
                shape3.rotate_cw()

                shape1.reflect()
                shape2.reflect()
                shape3.reflect()
                trans = 0
            else:
                shape1.rotate_cw()
                shape2.rotate_cw()
                shape3.rotate_cw()
                trans = trans + 1 

            shape1.draw(stdscr, 5, 5)
            shape2.draw(stdscr, 5, 20)
            shape3.draw(stdscr, 5, 35)


        curses.napms(100)


if __name__ == "__main__":
    curses.wrapper(main)

