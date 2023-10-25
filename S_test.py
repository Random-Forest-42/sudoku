
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
                    "076380000",
                    "000000200",
                    "004009007",
                    "700005006",
                    "605000103",
                    "300400008",
                    "800100500",
                    "002000000",
                    "000076380",
                ]
                # rows = [
                #     '000201000',
                #     '009000000',
                #     '000304000',
                #     '000000000',
                #     '000000000',
                #     '000900000',
                #     '000000090',
                #     '000000000',
                #     '000006000',
                # ]
                rows = ['076380015', '083000260', '054609837', '718035006', '645000103', '329461758', '867103500', '032000671', '091076380']
            self.char_to_list(rows)
        self.update_sudoku(based_on="rows")
        self.reset_hidden_pairs()
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

    def reset_hidden_pairs(self):
        self.hidden_box_pairs = [[[] for _ in range(9)] for _ in range(9)]
        self.hidden_column_pairs = [[[] for _ in range(9)] for _ in range(9)]
        self.hidden_row_pairs = [[[] for _ in range(9)] for _ in range(9)]

    def update_sudoku(self, based_on="rows"):
        # TODO: permitir otros. tiene sentido??
        self.reset_hidden_pairs()
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
            box 0, position 3 --> i=1, j=1
        """
        box_first_number_i = int(i/3)*3
        box_first_number_j = (i%3)*3
        sum_i_from_j = int(j/3)
        sum_j_from_j = j%3
        return box_first_number_i + sum_i_from_j, box_first_number_j + sum_j_from_j

    def get_possible_digits_from_position(self, i, j, check_hidden=True):
        own_digit = self.rows[i][j]
        if own_digit != 0:
            possible_digits = []
        else:
            box_digits = self.boxes[self.get_box_from_position(i, j)]
            row_digits = self.rows[i]
            column_digits = self.columns[j]
            impossible_digits = list(set(box_digits + row_digits + column_digits))
            if check_hidden:
                impossible_digits_from_hidden = self.get_impossible_digits_from_position_hidden(i,j)
                impossible_digits = list(set(impossible_digits + impossible_digits_from_hidden))
            possible_digits = [p for p in self.all_digits if p not in impossible_digits]
        return possible_digits

    def get_impossible_digits_from_position_hidden(self, i, j):
        box_index = self.get_box_from_position(i, j)
        hidden_pair_digits = []
        # TODO: la pair depende de si es por fila, columna, caja...
        # hidden_pair_from_given_position = self.hidden_pairs[i][j]
        # for j, b in enumerate(self.boxes[box_index]):
        #     pos_i, pos_j = self.get_position_from_box(box_index, j)
        #     if pos_i != i and pos_j != j:
        #         hidden_pair = self.hidden_pairs[pos_i][pos_j]
        #         if hidden_pair != hidden_pair_from_given_position:
        #             for h_d in hidden_pair:
        #                 hidden_pair_digits.append(h_d)
        # if i == 7 and j == 3:
        #     print(f"hidden_pair_digits: {hidden_pair_digits}")
        return hidden_pair_digits

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
            found_something_row = self.fill_by_row()
            self.check_found_update(found_something_row)
            found_something_column = self.fill_by_columns()
            self.check_found_update(found_something_column)

            found_something = max([
                found_something_single,
                found_something_box,
                found_something_row,
                found_something_column,
            ])

            if not found_something:
                self.detect_box_hidden_pairs()

                found_something = False
                found_something_single = self.fill_naked_singles()
                self.check_found_update(found_something_single)
                found_something_box = self.fill_by_box()
                self.check_found_update(found_something_box)
                found_something_row = self.fill_by_row()
                self.check_found_update(found_something_row)
                found_something_column = self.fill_by_columns()
                self.check_found_update(found_something_column)

                found_something = max([
                    found_something_single,
                    found_something_box,
                    found_something_row,
                    found_something_column,
                ])

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

    def fill_by_row(self):
        """Looking at each row, if a digit
        can only go to one place
        """
        found_something = False
        for i in range(9):
            row = self.rows[i]
            missing_digits = [d for d in self.all_digits if d not in row]
            possible_row_digits = [[] for i in range(len(row))]
            for j, c in enumerate(row):
                if c == 0:
                    pos_i, pos_j = i, j
                    possible_row_digits[j] = self.get_possible_digits_from_position(pos_i, pos_j)
            for m_d in missing_digits:
                possible_cells = [(c, k) for k, c in enumerate(possible_row_digits) if m_d in c]
                # TODO: buscar parejas, trios...
                if len(possible_cells) == 1:
                    columns_index = possible_cells[0][1]
                    if self.print_debug:
                        print(f"in row {i}, digit {m_d} can only be in column {columns_index}")
                    # TODO: updated basen on boxes??
                    self.rows[i][columns_index] = m_d
                    found_something = True
        return found_something

    def fill_by_columns(self):
        """Looking at each column, if a digit
        can only go to one place
        """
        found_something = False
        for i in range(9):
            column = self.columns[i]
            missing_digits = [d for d in self.all_digits if d not in column]
            possible_row_digits = [[] for i in range(len(column))]
            for j, c in enumerate(column):
                if c == 0:
                    pos_i, pos_j = j, i
                    possible_row_digits[j] = self.get_possible_digits_from_position(pos_i, pos_j)
            for m_d in missing_digits:
                possible_cells = [(c, k) for k, c in enumerate(possible_row_digits) if m_d in c]
                # TODO: buscar parejas, trios...
                if len(possible_cells) == 1:
                    row_index = possible_cells[0][1]
                    if self.print_debug:
                        print(f"in column {i}, digit {m_d} can only be in row {row_index}")
                    # TODO: updated basen on boxes??
                    self.rows[row_index][i] = m_d
                    found_something = True
        return found_something

    def detect_box_hidden_pairs(self):
        """Looking at each box, see if there are pairs
            TODO: only plain
        """
        self.reset_hidden_pairs()
        for k in range(3):
            # TODO: super cutre copia pega codigo
            for i in range(9):
                box = self.boxes[i]
                missing_digits = [d for d in self.all_digits if d not in box]
                possible_box_digits = [[] for i in range(len(box))]
                for j, c in enumerate(box):
                    if c == 0:
                        pos_i, pos_j = self.get_position_from_box(i, j)
                        possible_box_digits[j] = self.get_possible_digits_from_position(pos_i, pos_j)

                possible_box_digits_not_solved = [pbx for pbx in possible_box_digits if pbx != []]
                set_possible_box_digits_not_solved = set(tuple(p) for p in possible_box_digits_not_solved)
                aux_d = {str(list(k)):0 for k in set_possible_box_digits_not_solved}
                for j, pbd in enumerate(possible_box_digits_not_solved):
                    aux_d[str(pbd)] += 1
                for j, pbd in enumerate(possible_box_digits):
                    if pbd != [] and aux_d.get(str(pbd)) is not None:
                        if aux_d[str(pbd)] > 1:
                            pos_i, pos_j = self.get_position_from_box(i, j)
                            print(f"found pair (B) in {pos_i},{pos_j}: {pbd}")
                            self.hidden_box_pairs[pos_i][pos_j] = pbd
            # by column
            for i in range(9):
                column = self.columns[i]
                missing_digits = [d for d in self.all_digits if d not in column]
                possible_row_digits = [[] for i in range(len(column))]
                for j, c in enumerate(column):
                    if c == 0:
                        pos_i, pos_j = j, i
                        possible_row_digits[j] = self.get_possible_digits_from_position(pos_i, pos_j)

                possible_col_digits_not_solved = [pbx for pbx in possible_row_digits if pbx != []]
                set_possible_col_digits_not_solved = set(tuple(p) for p in possible_col_digits_not_solved)
                aux_d = {str(list(k)):0 for k in set_possible_col_digits_not_solved}
                for j, pbd in enumerate(possible_col_digits_not_solved):
                    aux_d[str(pbd)] += 1
                for j, pbd in enumerate(possible_row_digits):
                    if pbd != [] and aux_d.get(str(pbd)) is not None:
                        if aux_d[str(pbd)] > 1:
                            pos_i, pos_j = j, i
                            print(f"found pair (C) in {pos_i},{pos_j}: {pbd}")
                            self.hidden_column_pairs[pos_i][pos_j] = pbd

s = Sudoku()
s.draw()
# s.fill_naked_singles()
# s.fill_by_box()
# s.draw()
s.iterative_solve()
s.list_to_char()
s.rows
s.columns
s.boxes
# s.get_position_from_box(2, 2)

# if not s.check_finished():
#     for i in range(9):
#         for j in range(9):
#             # print(s.get_possible_numbers_from_position(i, j))
#             # print(f"i = {i}, j = {j}, box = {s.get_box_from_position(i, j)}")
#             print(f"i = {i}, j = {j}, possible_numbers = {s.get_possible_digits_from_position(i, j)}")
#             # new_i, new_j = s.get_position_from_box(i,j)
#             # print(f"caja = {i}, posicion = {j}, corresponde a fila {new_i}, columna = {new_j}")
# for i in range(9):
# s.detect_box_hidden_pairs()
# s.hidden_pairs


# for i in range(9):
#     for j in range(9):
#         new_i, new_j = s.get_position_from_box(i,j)
#         print(f"caja = {i}, posicion = {j}, corresponde a fila {new_i}, columna = {new_j}")
