import random


class Game:
    def __init__(self, sc, el):
        self.player_stone = sc
        self.enemy_stone = sc * -1

        self.enemy_level = el

        self.current_turn = 1
        self.turn_count = 0

        self.column = 0
        self.row = 0

        self.valid_squares = []
        self.valid_count = 0
        self.pass_count = 0

        self.evaluation = [
            [40, -12, 0, -1, -1, 0, -12, 40],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [0, -3, 0, -1, -1, 0, -3, 0],
            [-1, -3, -1, -1, -1, -1, -3, -1],
            [-1, -3, -1, -1, -1, -1, -3, -1],
            [0, -3, 0, -1, -1, 0, -3, 0],
            [-12, -15, -3, -3, -3, -3, -15, -12],
            [40, -12, 0, -1, -1, 0, -12, 40],
        ]

    def checkSquares(self, b):
        """
        石を打てるマスが有るか判定
        """
        self.valid_squares.clear()
        self.valid_count = 0

        for i in range(1, 9):
            for j in range(1, 9):
                if b.b_status[i][j] == self.current_turn:
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            if b.b_status[i + k][j + l] == self.current_turn * -1:
                                m = k
                                n = l

                                match m:
                                    case -1:
                                        match n:
                                            case -1:
                                                while True:
                                                    m -= 1
                                                    n -= 1
                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                            case 0:
                                                while True:
                                                    m -= 1
                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                            case 1:
                                                while True:
                                                    m -= 1
                                                    n += 1

                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                    case 0:
                                        match n:
                                            case -1:
                                                while True:
                                                    n -= 1

                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                            case 0:
                                                pass
                                            case 1:
                                                while True:
                                                    n += 1

                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                    case 1:
                                        match n:
                                            case -1:
                                                while True:
                                                    m += 1
                                                    n -= 1

                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                            case 0:
                                                while True:
                                                    m += 1
                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
                                            case 1:
                                                while True:
                                                    m += 1
                                                    n += 1

                                                    if (
                                                        b.b_status[i + m][j + n] == b.wall
                                                        or b.b_status[i + m][j + n] == self.current_turn
                                                    ):
                                                        break
                                                    elif b.b_status[i + m][j + n] == b.space:
                                                        self.valid_squares.append([i + m, j + n])
                                                        self.valid_count += 1

                                                        break
        if self.valid_count:
            self.pass_count = 0

            return True

        return False

    def checkMove(self, x, y, b):
        """
        プレイヤーがクリックしたマスに石を打てるか判定
        """
        column = int(y / b.c_size) + 1
        row = int(x / b.c_size) + 1

        for i in range(self.valid_count):
            if self.valid_squares[i][0] == column and self.valid_squares[i][1] == row:
                self.column = column
                self.row = row

                return True

    def reverseStones(self, b):
        """
        石を反転させる処理
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                if b.b_status[self.column + i][self.row + j] == self.current_turn * -1:
                    k = i
                    l = j

                    match k:
                        case -1:
                            match l:
                                case -1:
                                    while True:
                                        k -= 1
                                        l -= 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            k += 1
                                            l += 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1

                                                k += 1
                                                l += 1

                                            break
                                case 0:
                                    while True:
                                        k -= 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            k += 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1

                                                k += 1

                                            break
                                case 1:
                                    while True:
                                        k -= 1
                                        l += 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            k += 1
                                            l -= 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1

                                                k += 1
                                                l -= 1

                                            break
                        case 0:
                            match l:
                                case -1:
                                    while True:
                                        l -= 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            l += 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1
                                                l += 1
                                            break
                                case 0:
                                    pass
                                case 1:
                                    while True:
                                        l += 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            l -= 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1

                                                l -= 1

                                            break
                        case 1:
                            match l:
                                case -1:
                                    while True:
                                        k += 1
                                        l -= 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            k -= 1
                                            l += 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1

                                                k -= 1
                                                l += 1

                                            break
                                case 0:
                                    while True:
                                        k += 1
                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            k -= 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1
                                                k -= 1

                                            break
                                case 1:
                                    while True:
                                        k += 1
                                        l += 1

                                        if (
                                            b.b_status[self.column + k][self.row + l] == b.space
                                            or b.b_status[self.column + k][self.row + l] == b.wall
                                        ):
                                            break
                                        elif b.b_status[self.column + k][self.row + l] == self.current_turn:
                                            b.b_status[self.column][self.row] = self.current_turn

                                            k -= 1
                                            l -= 1

                                            while (
                                                b.b_status[self.column][self.row]
                                                != b.b_status[self.column + k][self.row + l]
                                            ):
                                                b.b_status[self.column + k][self.row + l] *= -1
                                                k -= 1
                                                l -= 1
                                            break

    def level1Move(self):
        """
        レベル1の思考ロジック
        有効マスの中からランダムに選択
        """
        random_square = random.randint(0, self.valid_count - 1)
        self.column = self.valid_squares[random_square][0]
        self.row = self.valid_squares[random_square][1]

    def level2Move(self):
        """
        レベル2の思考ロジック
        最も評価値の高い有効マスを選択
        """
        most_valuable = -100

        for i in range(self.valid_count):
            if self.evaluation[self.valid_squares[i][0] - 1][self.valid_squares[i][1] - 1] > most_valuable:
                most_valuable = self.evaluation[self.valid_squares[i][0] - 1][self.valid_squares[i][1] - 1]
                self.column = self.valid_squares[i][0]
                self.row = self.valid_squares[i][1]

    def judge(self, black_count, white_count, black, white, give_up):
        """
        どちらが勝ったのか判定
        """
        if give_up:
            return 1
        else:
            if black_count > white_count:
                if black == self.player_stone:
                    return 0
                else:
                    return 1
            elif white_count > black_count:
                if white == self.player_stone:
                    return 0
                else:
                    return 1
            else:
                return 2
