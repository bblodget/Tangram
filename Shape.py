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
        self.transformation = []
        self.shape_dim = len(shape_def)
        self.shape_name = shape_name
        self.shape_char = shape_char
        self.transform_num = 0

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

        # Initialize the transformation list
        self._init_transformation()

    def _init_transformation(self):
        trans = self.shape_table

        # Check the 4 non reflective rotations
        for i in range(4):
            if not self._already_in_transformation(trans):
                self.transformation.append(trans)
            trans = self._rotate_cw(trans)

        # Check the 4 reflective rotations
        trans = self._reflect(self.shape_table)
        for i in range(4):
            if not self._already_in_transformation(trans):
                self.transformation.append(trans)
            trans = self._rotate_cw(trans)

    def _already_in_transformation(self,test_trans):
        # Test every transformation in the transformation list
        for trans in self.transformation:
            match = True
            # Tests every line of trans against test_trans
            # If not equal then unique
            for y in range(len(trans)):
                if trans[y] != test_trans[y]:
                    match = False
            if match:
                return True

        return False
                

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
        line = self.transformation[self.transform_num][row]
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
        stdscr.move(y, x)
        stdscr.addstr(str(self.transform_num))
        y = y + 1

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

    def _rotate_cw(self, shape):
        rot_shape = copy.deepcopy(shape)
        dim = len(shape)
        for y in range(dim):
            for x in range(dim):
                ry = x
                rx = (dim - 1) - y
                rot_shape[ry][rx] = shape[y][x]
        return rot_shape

    def _reflect(self, shape):
        reflect_shape = copy.deepcopy(shape)
        dim = len(shape)
        for y in range(dim):
            for x in range(dim):
                ry = y
                rx = (dim - 1) - x
                reflect_shape[ry][rx] = shape[y][x]
        return reflect_shape

    def next_transform(self):
        self.transform_num = (self.transform_num+1) % len(self.transformation)



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
            shape1.next_transform()
            shape2.next_transform()
            shape3.next_transform()

            shape1.draw(stdscr, 5, 5)
            shape2.draw(stdscr, 5, 20)
            shape3.draw(stdscr, 5, 35)


        curses.napms(100)


if __name__ == "__main__":
    curses.wrapper(main)

