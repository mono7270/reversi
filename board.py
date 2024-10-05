class Board:
    def __init__(self):
        self.black = 1
        self.white = -1
        self.space = 0
        self.wall = 3

        self.black_count = 0
        self.white_count = 0

        self.b_status = [[self.space for _ in range(10)] for _ in range(10)]

        for i in range(10):
            self.b_status[0][i] = self.wall
            self.b_status[9][i] = self.wall
            self.b_status[i][0] = self.wall
            self.b_status[i][9] = self.wall

        self.b_size = 640
        self.c_size = self.b_size / 8
        self.s_size = self.c_size * 0.8

    def drawBoard(self, b_picture):
        b_picture.create_rectangle(
            0, 0, self.b_size, self.b_size, fill="green", outline="black"
        )

        for i in range(8):
            b_picture.create_line(
                i * self.c_size, 0, i * self.c_size, self.b_size, fill="black"
            )
            b_picture.create_line(
                0, i * self.c_size, self.b_size, i * self.c_size, fill="black"
            )

    def resetStones(self):
        for i in range(8):
            for j in range(8):
                self.b_status[i + 1][j + 1] = self.space

        self.b_status[4][5] = self.black
        self.b_status[5][4] = self.black
        self.b_status[4][4] = self.white
        self.b_status[5][5] = self.white

    def drawStones(self, b_picture):
        self.black_count = 0
        self.white_count = 0

        b_picture.delete("stone")

        for i in range(8):
            for j in range(8):
                if self.b_status[i + 1][j + 1] == self.black:
                    b_picture.create_oval(
                        j * self.c_size + 5,
                        i * self.c_size + 5,
                        j * self.c_size + self.c_size - 5,
                        i * self.c_size + self.c_size - 5,
                        fill="black",
                        outline="black",
                        tag="stone",
                    )
                    self.black_count += 1
                elif self.b_status[i + 1][j + 1] == self.white:
                    b_picture.create_oval(
                        j * self.c_size + 5,
                        i * self.c_size + 5,
                        j * self.c_size + self.c_size - 5,
                        i * self.c_size + self.c_size - 5,
                        fill="white",
                        outline="black",
                        tag="stone",
                    )
                    self.white_count += 1
