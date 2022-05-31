import copy
import json
import pygame
from random import randint

screen_size = (700, 600)
screen = pygame.display.set_mode(screen_size)


class tetrominoes:
    def __init__(self):
        foo = open("tetrominoes.json", "r")
        file = json.load(foo)
        foo.close()
        self.index = file["index"]
        self.pieces = file["pieces"]
        self.colors = file["colors"]

    def get_piece(self, piece, rotation):
        piece_list = self.pieces[self.index[piece]]
        piece_shape = piece_list[rotation % 4]
        temp = copy.deepcopy(piece_shape)
        for x in range(4):
            for y in range(4):
                if piece_shape[x][y]:
                    temp[x][y] = self.index[piece]
        return temp

    def get_colors(self):
        return self.colors

    def get_total_pieces(self):
        return len(self.index)


class game_board:
    def __init__(self, x, y):
        self.size = (x, y)
        self.grid = self.make_grid(self.size)

    def make_grid(self, size):
        grid = []
        for i in range(size[0]):
            row = []
            for j in range(size[1]):
                row.append(0)
            grid.append(row)
        return grid

    def is_valid_pos(self, piece_shape, pos):

        temp = copy.deepcopy(self.grid)

        for i in range(4):
            for j in range(4):
                if not piece_shape[i][j]:
                    continue
                x = i + pos[0]
                y = j + pos[1]
                if x < 0 or x >= self.size[0]:
                    return False
                if y >= self.size[1]:
                    return False
                if y < 0:
                    continue
                if temp[x][y]:
                    return False
        return True

    def to_draw_grid(self, piece_shape, pos):

        temp = copy.deepcopy(self.grid)

        for i in range(4):
            for j in range(4):
                if not piece_shape[i][j]:
                    continue
                x = i + pos[0]
                y = j + pos[1]
                if y < 0:
                    continue
                temp[x][y] = piece_shape[i][j]
        return temp

    def place_in_board(self, piece_shape, pos):
        temp = copy.deepcopy(self.grid)

        for i in range(4):
            for j in range(4):
                if not piece_shape[i][j]:
                    continue
                x = i + pos[0]
                y = j + pos[1]
                if y < 0:
                    return "game over"
                temp[x][y] = piece_shape[i][j]
        self.grid = temp

    def get_current_grid(self):
        return self.grid


class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.tetrominoes = tetrominoes()
        self.init()

    def init(self):
        self.game_board = game_board(*self.board_size)
        self.current_piece = randint(0, self.tetrominoes.get_total_pieces()-1)
        self.next_pieces, self.packet = self.make_next_piece([], [])
        self.pieces_pos = [4, -1]
        self.rotation = 0

    def make_next_piece(self, packet_in: list, next_pieces_in: list):
        next_pieces = copy.deepcopy(next_pieces_in)
        packet = copy.deepcopy(packet_in)
        while len(next_pieces) <= 6:
            if len(packet) == 0:
                packet = list(range(self.tetrominoes.get_total_pieces()))
            next_pieces.append(packet[randint(0, len(packet) - 1)])
            packet.remove(next_pieces[-1])
        if len(packet) == 0:
            packet = list(range(self.tetrominoes.get_total_pieces()))
        return next_pieces, packet

    def move_piece(self, inputs: dict):
        touching = 0
        rotation = self.rotation + inputs["rotation"]
        rotation %= 4
        if inputs["drop"]:
            x = self.pieces_pos[0]
            y = self.pieces_pos[1]
            while not touching:
                if self.game_board.is_valid_pos(self.tetrominoes.get_piece(self.current_piece, self.rotation), (x, y)):
                    y += 1
                else:
                    self.game_board.place_in_board(self.tetrominoes.get_piece(self.current_piece, rotation),
                                                   (x, y - 1))
                    touching = 1
                    self.current_piece = self.next_pieces[0]
                    self.next_pieces.pop(0)
                    self.next_pieces, self.packet = self.make_next_piece(self.packet, self.next_pieces)
                    self.pieces_pos = [4,-1]
                    self.clear_line()
        else:
            x = self.pieces_pos[0] + (inputs["right"] - inputs["left"])
            y = self.pieces_pos[1] + inputs["down"]
            if self.game_board.is_valid_pos(self.tetrominoes.get_piece(self.current_piece, rotation), (x, y)):
                self.pieces_pos = [x, y]
                self.rotation = rotation
            else:
                if y != self.pieces_pos[1]:
                    self.game_board.place_in_board(self.tetrominoes.get_piece(self.current_piece, self.rotation), \
                                                   self.pieces_pos)
                    self.current_piece = self.next_pieces[0]
                    self.next_pieces.pop(0)
                    self.next_pieces, self.packet = self.make_next_piece(self.packet, self.next_pieces)
                    self.pieces_pos = [4,-1]
                    self.clear_line()
                    if y <= 0:
                        self.init()
                        print("game_over")

    def get_draw_grid(self):
        grid = self.game_board.to_draw_grid(self.tetrominoes.get_piece(self.current_piece, self.rotation), self.pieces_pos)
        colors = self.tetrominoes.get_colors()
        return grid, self.board_size, colors

    def clear_line(self):
        to_remove = []
        grid = copy.deepcopy(self.game_board.grid)
        for y in range(self.board_size[1]):
            is_commplete_line = 1
            for x in range(self.board_size[0]):
                if not grid[x][y]:
                    is_commplete_line = 0
                    break
            if is_commplete_line:
                to_remove.append(y)
        if to_remove:
            for x in range(len(to_remove)):
                for i in range(self.board_size[0]):
                    grid[i].pop(to_remove[x])
                    grid[i].insert(0, 0)

        self.game_board.grid = grid




def draw(screen_size, board, board_size, colors):
    temp = min(screen_size[0] // board_size[0], screen_size[1] // board_size[1])
    cell_size = (temp, temp)
    screen = pygame.Surface((temp * board_size[0] + 1,temp * board_size[1]))
    screen.fill((100, 100, 100))
    for x in range(board_size[0]):
        for y in range(board_size[1]):
            if board[x][y]:
                rect = pygame.Rect((cell_size[0] * x, cell_size[1] * y), cell_size)
                pygame.draw.rect(screen, colors[board[x][y]], rect)

    for x in range(board_size[0] + 1):
        pygame.draw.line(screen, (0, 0, 0), (cell_size[0] * x, 0), (cell_size[0] * x, cell_size[1] * board_size[1]))
    for y in range(board_size[1] + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, cell_size[1] * y), (cell_size[0] * board_size[0], cell_size[1] * y))
    return screen


def event_handel():
    global das_mode, das_timer
    das_timer -= 1
    if das_timer < 0:
        das_timer = 0
    event = pygame.event.get()
    keys = pygame.key.get_pressed()
    inputs = {"left": 0, "right": 0, "down": 0, "drop": 0, "rotation": 0}
    for e in event:
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP or e.key == pygame.K_w:
                inputs["drop"] = 1
            if e.key == pygame.K_q or e.key == pygame.K_KP0:
                inputs["rotation"] -= 1
            if e.key == pygame.K_e or e.key == pygame.K_KP_PERIOD:
                inputs["rotation"] += 1
        if e.type == pygame.KEYUP:
            das_timer = 0
            das_mode = 0

    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and das_timer == 0:
        inputs["down"] = 1
        if das_mode == 0:
            das_timer = 30
            das_mode = 1
        else:
            das_timer = 6

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and das_timer == 0:
        inputs["left"] = 1
        if das_mode == 0:
            das_timer = 30
            das_mode = 1
        else:
            das_timer = 6

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and das_timer == 0:
        inputs["right"] = 1
        if das_mode == 0:
            das_timer = 30
            das_mode = 1
        else:
            das_timer = 6

    return inputs


def draw_left_ui(side_size, hold, colors):
    side = pygame.Surface(side_size)
    side.fill((50,50,50))
    buffer = side_size[0]//10
    cell_size = side_size[0]//5
    outline_rect = pygame.Rect((buffer, buffer), (cell_size*4+buffer//2, cell_size*4+buffer//2))
    outline_rect.center = (cell_size*5//2, cell_size*5//2)
    pygame.draw.rect(side,(200, 200, 200), outline_rect, buffer//2)
    return side

def calculate_all_sizes(screen_size, board_size):
    cell_size = min(screen_size[0] // board_size[0], screen_size[1] // board_size[1])
    side_size = (cell_size * 5, cell_size * board_size[1])
    game_size = (cell_size * board_size[0], cell_size * board_size[1])
    side_buffer = (screen_size[0] - (game_size[0] + (side_size[0]*2)))//2, screen_size[1]
    return side_size, game_size, side_buffer

# game_board = game_board(10,20)
# tetrominoes = tetrominoes()
# index = 0
# rotation = 0

game = Game((10, 20))
side_size, game_size, side_buffer = calculate_all_sizes(screen_size, (10, 20))
das_mode = 0  # 0 = wait mode, 1 = quick tap
das_timer = 0
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))
    # rotation += 1
    # if rotation > 3:
    # 	rotation = 0
    # 	index += 1
    # 	index %= tetrominoes.get_total_pieces()
    # piece_shape = tetrominoes.get_piece(index, rotation)
    # if game_board.is_valid_pos(piece_shape, (5,10)):
    # 	draw_grid = game_board.to_draw_grid(piece_shape, (5,10))
    # else:
    # 	draw_grid = game_board.get_current_grid()
    # draw(screen, screen_size, draw_grid, game_board.size, tetrominoes.get_colors())
    inputs = event_handel()
    game.move_piece(inputs)
    left_ui = draw_left_ui(side_size, [0], 0)
    game_screen = draw(game_size, *game.get_draw_grid())
    screen.blit(left_ui, (side_buffer[0], 0))
    screen.blit(game_screen, (side_size[0]+side_buffer[0], 0))
    pygame.display.flip()
