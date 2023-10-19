
class Sudoku:
    def __init__(self, rows=None, char_mode=True, print_debug=True) -> None:
        self.print_debug = print_debug
        if char_mode is False:
            if rows is not None:
                self.rows = rows
            else:
                raise Exception("must pass rows")
        else:
            if rows is None:
                print("default self.rows")
                rows = [
                    "961043002",
                    "703085941",
                    "045921000",
                    "390100005",
                    "104092368",
                    "502430007",
                    "437809200",
                    "010250830",
                    "058304700",
                ]
            self.char_to_list(rows)
        self.set_columns()
        self.set_boxes()
        if not self.check_valid():
            raise Exception("input sudoku is invalid")

    def draw(self, input="rows"):
        if input == "rows":
            input_to_draw = self.rows
        elif input == "columns":
            input_to_draw = self.columns
        elif input == "boxes":
            input_to_draw = self.boxes
        horizontal_line = '_'*22
        for i, row in enumerate(input_to_draw):
            if i in [0, 3, 6]:
                print(horizontal_line)
            number_row = ''
            for j, r in enumerate(row):
                if j in [0, 3, 6]:
                    number_row += '|'
                if r == 0:
                    number_row += '  '
                else:
                    number_row += f' {r}'
            number_row += '|'
            print(number_row)
        print(horizontal_line)
        pass

    def char_to_list(self, char_rows):
        rows = []
        for r in char_rows:
            r_s = []
            for c in r:
                r_s.append(int(c))
            rows.append(r_s)
        self.rows = rows

    def set_columns(self):
        columns = [[0 for _ in range(9)] for _ in range(9)]
        for i, r in enumerate(self.rows):
            for j, rr in enumerate(r):
                columns[j][i] = rr
        self.columns = columns

    def set_boxes(self):
        #TODO: mas elegante
        boxes = [[0 for _ in range(9)] for _ in range(9)]
        boxes[0] = [
            self.rows[0][0],
            self.rows[0][1],
            self.rows[0][2],
            self.rows[1][0],
            self.rows[1][1],
            self.rows[1][2],
            self.rows[2][0],
            self.rows[2][1],
            self.rows[2][2],
        ]
        boxes[1] = [
            self.rows[0][3],
            self.rows[0][4],
            self.rows[0][5],
            self.rows[1][3],
            self.rows[1][4],
            self.rows[1][5],
            self.rows[2][3],
            self.rows[2][4],
            self.rows[2][5],
        ]
        boxes[2] = [
            self.rows[0][6],
            self.rows[0][7],
            self.rows[0][8],
            self.rows[1][6],
            self.rows[1][7],
            self.rows[1][8],
            self.rows[2][6],
            self.rows[2][7],
            self.rows[2][8],
        ]
        boxes[3] = [
            self.rows[3][0],
            self.rows[3][1],
            self.rows[3][2],
            self.rows[4][0],
            self.rows[4][1],
            self.rows[4][2],
            self.rows[5][0],
            self.rows[5][1],
            self.rows[5][2],
        ]
        boxes[4] = [
            self.rows[3][3],
            self.rows[3][4],
            self.rows[3][5],
            self.rows[4][3],
            self.rows[4][4],
            self.rows[4][5],
            self.rows[5][3],
            self.rows[5][4],
            self.rows[5][5],
        ]
        boxes[5] = [
            self.rows[3][6],
            self.rows[3][7],
            self.rows[3][8],
            self.rows[4][6],
            self.rows[4][7],
            self.rows[4][8],
            self.rows[5][6],
            self.rows[5][7],
            self.rows[5][8],
        ]
        boxes[6] = [
            self.rows[6][0],
            self.rows[6][1],
            self.rows[6][2],
            self.rows[7][0],
            self.rows[7][1],
            self.rows[7][2],
            self.rows[8][0],
            self.rows[8][1],
            self.rows[8][2],
        ]
        boxes[7] = [
            self.rows[6][3],
            self.rows[6][4],
            self.rows[6][5],
            self.rows[7][3],
            self.rows[7][4],
            self.rows[7][5],
            self.rows[8][3],
            self.rows[8][4],
            self.rows[8][5],
        ]
        boxes[8] = [
            self.rows[6][6],
            self.rows[6][7],
            self.rows[6][8],
            self.rows[7][6],
            self.rows[7][7],
            self.rows[7][8],
            self.rows[8][6],
            self.rows[8][7],
            self.rows[8][8],
        ]
        self.boxes = boxes

    def check_valid_9(self, l):
        if len(l) != 9:
            if self.print_debug:
                print(f"l: {l} no tiene 9 elementos")
            return False
        l_0 = [ll for ll in l if ll != 0]
        if len(l_0) != len(set(l_0)):
            if self.print_debug:
                print(f"valores repetidos: {l_0}")
            return False
        return True

    def check_valid(self):
        is_valid = True
        for i, r in enumerate(self.rows):
            is_valid = self.check_valid_9(r)
            if not is_valid:
                if self.print_debug:
                    print(f"invalid row number {i+1}: {r}")
                return False
        for i, c in enumerate(self.columns):
            is_valid = self.check_valid_9(c)
            if not is_valid:
                if self.print_debug:
                    print(f"invalid column number {i+1}: {r}")
                return False
        for i, b in enumerate(self.boxes):
            is_valid = self.check_valid_9(b)
            if not is_valid:
                if self.print_debug:
                    print(f"invalid box number {i+1}: {r}")
                return False
        return is_valid

    def get_box_from_position(self, i, j):
        if i in [0, 1, 2]:
            box_aux_i = 0
        elif i in [3, 4, 5]:
            box_aux_i = 1
        else:
            box_aux_i = 2
        if j in [0, 1, 2]:
            box_aux_j = 0
        elif j in [3, 4, 5]:
            box_aux_j = 1
        else:
            box_aux_j = 2
        box = box_aux_i*3 + box_aux_j
        return box


    def get_possible_numbers_from_position(self, i, j):
        possible_numbers = [k+1 for k in range(9)]


    def fill_row_numbers(self):
        pass

s = Sudoku()
s.draw()
for i in range(9):
    for j in range(9):

        print(f"i = {i}, j = {j}, box = {s.get_box_from_position(i, j)}")

# sudoku_char = [
#     "961043002",
#     "703085941",
#     "045921000",
#     "390100005",
#     "104092368",
#     "502430007",
#     "437809200",
#     "010250830",
#     "058304702",
# ]
# s2 = Sudoku(rows=sudoku_char)