import pygame
import json
import copy

screen_size = (300,600)
screen = pygame.display.set_mode(screen_size)

file = open("tetrominoes.json", "r")
file = json.load(file)
index = file["index"]
pieces = file["pieces"]
colors = file["colors"]
for x in range(len(index)):
	print(pieces[index[x]])

def event_handel():
	event = pygame.event.get()
	for e in event:
		if e.type == pygame.QUIT:
			pygame.quit()
			quit()


clock = pygame.time.Clock()
while True:
	clock.tick(0.5)
	screen.fill((100, 100, 100))
	event_handel()
	pygame.display.flip()

