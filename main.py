import pygame
from random import sample

pygame.init()
pygame.font.init()

length = 500
screen = pygame.display.set_mode((length, length))
pygame.display.set_caption('Sudoku')
font1 = pygame.font.SysFont("comicsans", length//10)
running = False

difficulty = ""

width = length/9
k = 50
val = 0

def shuffle(s): return sample(s,len(s)) 

def cord(pos):
	global x, y
	x = pos[0]//width
	y = pos[1]//width
	   
# starting position for the highlited box
cord((50,50))

### game loop
while True:
	a = 0
	screen.fill((200,200,200))

	if running == False:
		### create the gui
		# create the title
		title = font1.render("Sudoku", True, (0,0,0))
		title_rect = title.get_rect(center = (length/2, 50))
		screen.blit(title, title_rect)

		# easy
		easy_rect = pygame.draw.rect(screen, (0,0,0), (length/2-50, 100, 100, 50))
		easy = font1.render("Easy", True, (200,200,200))
		easy_rect = easy.get_rect(center = (length/2, 125))
		screen.blit(easy, easy_rect)

		# medium
		med_rect = pygame.draw.rect(screen, (0,0,0), (length/2-50, 175, 100, 50))
		med = font1.render("Med", True, (200,200,200))
		med_rect = med.get_rect(center = (length/2, 200))
		screen.blit(med, med_rect)
		
		# hard
		hard_rect = pygame.draw.rect(screen, (0,0,0), (length/2-50, 250, 100, 50))
		hard = font1.render("Hard", True, (200,200,200))
		hard_rect = hard.get_rect(center = (length/2, 275))
		screen.blit(hard, hard_rect)

		# impossible
		impos = pygame.draw.rect(screen, (0,0,0), (length/2-100, 325, 200, 50))
		impos = font1.render("Impossible", True, (200,200,200))
		impos_rect = impos.get_rect(center = (length/2, 350))
		screen.blit(impos, impos_rect)

		
		if difficulty != '':
			running = True
			### create the board
			base  = 3
			side  = base*base
			
			# randomize rows, columns and numbers (of valid base pattern)
				
			rBase = range(base) 
			rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
			cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
			nums  = shuffle(range(1,base*base+1))
			
			
			# produce board using randomized baseline pattern
			board = [[nums[(base*(r%base)+r//base+c)%side] for c in cols] for r in rows]
			
			squares = side*side
			
			# minimum amount of squares filled in for a sudoku is 17 squares
			if difficulty == "easy":
				empties = 30
			elif difficulty == "medium":
				empties = 40
			elif difficulty == "hard":
				empties = 50
			elif difficulty == "impossible":
				empties = 64
			for p in sample(range(squares),empties):
				board[p//side][p%side] = 0
			
			numSize = len(str(side))
			
			a = [[nums[(base*(r%base)+r//base+c)%side] for c in cols] for r in rows]
			
			
			# answers and answered
			answers = []
			answered = [[0 for i in range(9)] for j in range(9)]
	
			for i in range(9):
				answers.append([])
				for j in range(9):
					if board[i][j] == 0:
						answers[i].append(a[i][j])
					else:
						answers[i].append(0)
			pygame.display.set_caption("Sudoku: " + difficulty + ". Press 'r' to restart")
			print("Board:")
			for line in board: print(line)
			
			# print("answers:")
			# for i in answers:print(i)
		
	else: # the sudoku game
		### draw the values on the dark gray squares
		for i in range(9):
			for j in range(9):
				# dark gray squares
				# check if board value is not empty
				if board[i][j] != 0:
					pygame.draw.rect(screen, (140, 140, 140), (j*width, i*width, width+1, width+1)) 
	
					# values			
					screen.blit(font1.render(str(board[i][j]),True, (0,0,0)), (j*width+width/3,i*width+width/4))
	
				# check if board value is empty
				elif board[i][j] == 0:
					# blit user values
					if answered[i][j] != 0:
						screen.blit(font1.render(str(answered[i][j]),True, (0,0,0)), (j*width+width/3,i*width+width/4))


		### draw lines to separate the boxes
		for l in range(10):
			thick = 5 if l % 3 == 0 else 1
			
			pygame.draw.line(screen, (0, 0, 0), (0, l * width), (length, l * width), thick)
			pygame.draw.line(screen, (0, 0, 0), (l * width, 0), (l * width, length), thick)
	
		### highlight the box 
		for k in range(2):
			pygame.draw.line(screen, (0, 0, 0), (x * width-3, (y + k)*width), (x * width + width + 3, (y + k)*width), 7)
			
			pygame.draw.line(screen, (0, 0, 0), ( (x + k)* width, y * width ), ((x + k) * width, y * width + width), 7) 
	
		### check for win
		if answers == answered:
			break
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			break
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = event.pos
			if easy_rect.collidepoint(pos):
				difficulty = 'easy'
				
			elif med_rect.collidepoint(pos):
				difficulty = 'medium'
				
			elif hard_rect.collidepoint(pos):
				difficulty = 'hard'
				
			elif impos_rect.collidepoint(pos):
				difficulty = 'impossible'
				
			cord(pos)
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				break
			if running == True:
				# move the highlighted box
				if event.key == pygame.K_w or event.key == pygame.K_UP:
					y -= 1
				elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
					y += 1
				elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
					x -= 1
				elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
					x += 1
				
				# change the values on the squares
				elif event.key == pygame.K_1:
					val = 1
					a = 1
					
				elif event.key == pygame.K_2:
					val = 2
					a = 1
					
				elif event.key == pygame.K_3:
					val = 3
					a = 1
					
				elif event.key == pygame.K_4:
					val = 4
					a = 1
					
				elif event.key == pygame.K_5:
					val = 5
					a = 1
					
				elif event.key == pygame.K_6:
					val = 6
					a = 1
					
				elif event.key == pygame.K_7:
					val = 7
					a = 1
					
				elif event.key == pygame.K_8:
					val = 8
					a = 1
					
				elif event.key == pygame.K_9:
					val = 9
					a = 1
				elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
					val = 0
					a = 1
				elif event.key == pygame.K_r:
					running = False
					difficulty = ''
	if a == 1 and board[int(y)][int(x)] == 0: answered[int(y)][int(x)] = val
	
	pygame.display.flip()
	
pygame.quit()
	