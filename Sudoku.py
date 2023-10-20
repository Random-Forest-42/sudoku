
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
                    "060043002",
                    "703085941",
                    "040001000",
                    "390100005",
                    "104092000",
                    "502430007",
                    "407809000",
                    "010250830",
                    "008304000",
                ]
                # rows = [
                #     "000400370",
                #     "801000020",
                #     "743908000",
                #     "300070980",
                #     "006000050",
                #     "000040603",
                #     "530204000",
                #     "000090740",
                #     "900050030",
                # ]
                # rows = [
                #     "100000000",
                #     "205000000",
                #     "306000000",
                #     "000000000",
                #     "000000000",
                #     "000000000",
                #     "070000000",
                #     "000000000",
                #     "000000000",
                # ]
                # rows = ['600400370', '801000020', '743908060', '315672984', '406000257', '200040613', '530204090', '100090740', '900050030']
                # rows = ['600400379', '801000020', '743908060', '315672984', '406000257', '200040613', '530204090', '100090740', '900050030']
            self.char_to_list(rows)
        self.update_sudoku(based_on="rows")
        if not self.check_valid():
            raise Exception("input sudoku is invalid")

    def check_finished(self):
        if not self.check_valid():
            return False
        else:
            for r in self.rows:
                if sum(r) != 45:
                    return False
        return True

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

    def list_to_char(self):
        chars = []
        for r in self.rows:
            char = ""
            for rr in r:
                char += str(rr)
            chars.append(char)
        print(chars)

    def update_sudoku(self, based_on="rows"):
        # TODO: permitir otros. tiene sentido??
        if based_on == 'rows':
            self.set_columns()
            self.set_boxes()


    def set_columns(self):
        columns = [[0 for _ in range(9)] for _ in range(9)]
        for i, r in enumerate(self.rows):
            for j, rr in enumerate(r):
                columns[j][i] = rr
        self.columns = columns

    def set_boxes(self):
        boxes = [[] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                boxes[self.get_box_from_position(i, j)].append(self.rows[i][j])
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
        box_numbers = self.boxes[self.get_box_from_position(i, j)]
        row_numbers = self.rows[i]
        column_numbers = self.columns[j]
        impossible_numbers = list(set(box_numbers + row_numbers + column_numbers))
        possible_numbers = [p for p in possible_numbers if p not in impossible_numbers]
        return possible_numbers

    ## METODOS RESOLUCION
    def fill_naked_singles(self):
        """Easies resolution method:
            fills cells that only can have 1 digit
        """
        it = 0
        found_something = False
        while it < 90 and (found_something is True or it == 0):
            # print("-----")
            found_something = False
            for i in range(9):
                for j in range(9):
                    if it == 1 and i == 0 and j == 7:
                        print(self.rows[i][j])
                        print(self.get_possible_numbers_from_position(i, j))
                    if self.rows[i][j] == 0:
                        possible_numbers = self.get_possible_numbers_from_position(i, j)
                        if len(possible_numbers) == 1:
                            only_possible_number = possible_numbers[0]
                            if self.print_debug:
                                print(f"i = {i}, j = {j}, only possible number: {only_possible_number}")
                            self.rows[i][j] = only_possible_number
                            found_something = True
            if found_something:
                if self.print_debug:
                    print("updating")
                self.update_sudoku(based_on="rows")
                self.draw()
            it += 1
        return found_something

    def fill_by_box(self):
        """
        """
        for i in range(9):
            pass

s = Sudoku()
s.draw()
s.fill_naked_singles()
# s.draw()
# i = 0
# j = 8
# possible_numbers = [k+1 for k in range(9)]
# box_numbers = s.boxes[s.get_box_from_position(i, j)]
# row_numbers = s.rows[i]
# column_numbers = srows[j]
# s.check_finished()
s.list_to_char()
# for i in range(9):
#     for j in range(9):
#         # print(s.get_possible_numbers_from_position(i, j))
#         # print(f"i = {i}, j = {j}, box = {s.get_box_from_position(i, j)}")
#         print(f"i = {i}, j = {j}, possible_numbers = {s.get_possible_numbers_from_position(i, j)}")

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
