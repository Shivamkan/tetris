import copy
import json
import pygame
from random import randint

screen_size = (300,600)
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
		piece_shape = piece_list[rotation%4]
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
				if y > self.size[1]:
					return False
				if temp[x][y]:
					return False
				if y < 0:
					continue
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

	def get_current_grid(self):
		return self.grid

class Game:
	def __init__(self):
		self.tetrominoes = tetrominoes()
		self.game_board = game_board()
		self.current_piece = randint(0,self.tetrominoes.get_total_pieces())
		self.next_pieces, self.packet = self.make_next_piece([],[])
		self.pieces_pos = [4,-2]
		self.rotation = 0

	def make_next_piece(self, packet_in:list, next_pieces_in:list):
		next_pieces = copy.deepcopy(next_pieces_in)
		packet = copy.deepcopy(packet_in)
		while len(next_pieces)<=6:
			if len(packet) == 0:
				packet = copy.deepcopy(self.tetrominoes.index)
			next_pieces.append(packet[randint(0, len(packet)-1)])
			packet.remove(next_pieces[-1])
		if len(packet) == 0:
			packet = copy.deepcopy(self.tetrominoes.index)
		return next_pieces, packet



def draw(screen, screen_size, board, board_size, colors):
	cell_size = (screen_size[0] // board_size[0], screen_size[1] // board_size[1])
	for x in range(board_size[0]):
		for y in range(board_size[1]):
			if board[x][y]:
				rect = pygame.Rect((cell_size[0] * x, cell_size[1] * y), cell_size)
				pygame.draw.rect(screen, colors[board[x][y]], rect)

	for x in range(board_size[0]+1):
		pygame.draw.line(screen, (0,0,0), (cell_size[0]*x, 0), (cell_size[0]*x, cell_size[1]*board_size[1]))
	for y in range(board_size[1]+1):
		pygame.draw.line(screen, (0,0,0), (0, cell_size[1]*y), (cell_size[0]*board_size[0], cell_size[1]*y))

def event_handel():
	event = pygame.event.get()
	for e in event:
		if e.type == pygame.QUIT:
			pygame.quit()
			quit()

game_board = game_board(10,20)
tetrominoes = tetrominoes()

index = 0
rotation = 0



clock = pygame.time.Clock()
while True:
	clock.tick(60)
	screen.fill((100, 100, 100))
	# rotation += 1
	# if rotation > 3:
	# 	rotation = 0
	# 	index += 1
	# 	index %= tetrominoes.get_total_pieces()
	piece_shape = tetrominoes.get_piece(index, rotation)
	if game_board.is_valid_pos(piece_shape, (5,10)):
		draw_grid = game_board.to_draw_grid(piece_shape, (5,10))
	else:
		draw_grid = game_board.get_current_grid()
	draw(screen, screen_size, draw_grid, game_board.size, tetrominoes.get_colors())
	event_handel()
	pygame.display.flip()

