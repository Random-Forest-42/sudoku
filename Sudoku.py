
class Sudoku:
    def __init__(self, rows=None, char_mode=True, print_debug=True) -> None:
        self.print_debug = print_debug
        self.all_digits = [k + 1 for k in range(9)]
        if char_mode is False:
            if rows is not None:
                self.rows = rows
            else:
                raise Exception("must pass rows")
        else:
            if rows is None:
                print("default self.rows")
                rows = [
                    "007001200",
                    "009400807",
                    "008005000",
                    "000000000",
                    "100004700",
                    "002090600",
                    "200500060",
                    "000000085",
                    "300006400",
                ]
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
        """
            i: row index
            j: column index
        """
        box_aux_i = int(i/3)
        box_aux_j = int(j/3)
        box = box_aux_i*3 + box_aux_j
        return box

    def get_position_from_box(self, i, j):
        """
            box_index: what box number is
            box_position: within that box
        Ex:
            box 1, position 4 --> i=0, j=1
        """
        box_first_number_i = int(i/3)*3
        box_first_number_j = (i%3)*3
        sum_i_from_j = int(j/3)
        sum_j_from_j = j%3
        return box_first_number_i + sum_i_from_j, box_first_number_j + sum_j_from_j

    def get_possible_digits_from_position(self, i, j):
        box_numbers = self.boxes[self.get_box_from_position(i, j)]
        row_numbers = self.rows[i]
        column_numbers = self.columns[j]
        impossible_digits = list(set(box_numbers + row_numbers + column_numbers))
        possible_digits = [p for p in self.all_digits if p not in impossible_digits]
        return possible_digits

    def check_found_update(self, flag):
        if flag:
            if self.print_debug:
                print("updating")
            self.update_sudoku(based_on="rows")
            self.draw()

    ## METODOS RESOLUCION
    def iterative_solve(self):
        it = 0
        max_it = 40
        found_something = False
        while it < max_it and (found_something is True or it == 0):
            it += 1
            found_something = False
            found_something_single = self.fill_naked_singles()
            self.check_found_update(found_something_single)
            found_something_box = self.fill_by_box()
            self.check_found_update(found_something_box)

            found_something = max([found_something_single, found_something_box])

        if it == max_it:
            if self.print_debug:
                print("WARNING: max iter reached")

    def fill_naked_singles(self):
        """Easies resolution method:
            fills cells that only can have 1 digit
        """
        found_something = False
        for i in range(9):
            for j in range(9):
                if self.rows[i][j] == 0:
                    possible_numbers = self.get_possible_digits_from_position(i, j)
                    if len(possible_numbers) == 1:
                        only_possible_number = possible_numbers[0]
                        if self.print_debug:
                            print(f"i = {i}, j = {j}, only possible number: {only_possible_number}")
                        self.rows[i][j] = only_possible_number
                        found_something = True
        return found_something

    def fill_by_box(self):
        """Looking at each box, if a digit
        can only go to one place
        """
        found_something = False
        for i in range(9):
            box = self.boxes[i]
            missing_digits = [d for d in self.all_digits if d not in box]
            possible_box_digits = [[] for i in range(len(box))]
            for j, c in enumerate(box):
                if c == 0:
                    pos_i, pos_j = self.get_position_from_box(i, j)
                    possible_box_digits[j] = self.get_possible_digits_from_position(pos_i, pos_j)
            for m_d in missing_digits:
                possible_cells = [(c, k) for k, c in enumerate(possible_box_digits) if m_d in c]
                # TODO: buscar parejas, trios...
                if len(possible_cells) == 1:
                    box_place = possible_cells[0][1]
                    if self.print_debug:
                        print(f"in box {i}, digit {m_d} can only be in position {box_place}")
                    # TODO: updated basen on boxes??
                    pos_i, pos_j = self.get_position_from_box(i, box_place)
                    self.rows[pos_i][pos_j] = m_d
                    found_something = True
        return found_something

s = Sudoku()
s.draw()
# s.fill_naked_singles()
# s.fill_by_box()
# s.draw()
s.iterative_solve()
# s.list_to_char()

# s.get_position_from_box(2, 2)

# for i in range(9):
#     for j in range(9):
#         # print(s.get_possible_numbers_from_position(i, j))
#         # print(f"i = {i}, j = {j}, box = {s.get_box_from_position(i, j)}")
#         print(f"i = {i}, j = {j}, possible_numbers = {s.get_possible_numbers_from_position(i, j)}")

