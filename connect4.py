import copy
import timeit
import numpy as np
import random
import pygame
import sys
import math
#from Visualize_Tree import *

# Global Variables ***********************************************************
#Colors for the GUI
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#Game Dimensions (width ≥ 7, length ≥ 6)
ROW_COUNT = 6
COLUMN_COUNT = 7

#Dimensions For the GUI
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+2) * SQUARESIZE
size = (width, height)

#Connect-4
WINDOW_LENGTH = 4

#Player vs AI
PLAYER = 0
PLAYER2 = 1
AI = 1

#Pieces and Empty Spaces
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
# *********************************************************************************

# The Logic to implement the Game *************************************************
#Create the board (Initially, it's all empty)
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

#Drop the piece
def drop_piece(board, row, col, piece):
	board[row][col] = piece

#Check if valid move (valid if there's an empty space in the column)
def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def is_within_bounds(col,row):
	return (col<COLUMN_COUNT and row<ROW_COUNT)

#Gets the next empty row in the selected column
def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

#Print the board to the console
def print_board(board):
	print(np.flip(board, 0))

#Check if move will make a sequence of 4
def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

#Count number of wins
def count_wins_old(board, piece):

	board=np.flip(board, 0)
	wins=0
	count=0

	# Check horizontal locations for win
	for r in range(ROW_COUNT):
		count=0 #for every row
		for c in range(COLUMN_COUNT):
			if(board[r][c]==piece):
				count+=1
			else:
				if(count>=WINDOW_LENGTH):
					wins+=1
				count=0
		if(count>=2*WINDOW_LENGTH-1): #Vertical: maximum = 7 -> can make 2 sequences
			wins+=2
		elif(count>=WINDOW_LENGTH):
			wins+=1

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		count=0 #for every column
		for r in range(ROW_COUNT):
			if(board[r][c]==piece):
				count+=1
			else:
				if(count>=WINDOW_LENGTH): #Vertical: maximum = 6 -> only one sequence is possible
					wins+=1
				count=0
		if(count>=WINDOW_LENGTH): #Vertical: maximum = 6 -> only one sequence is possible
			wins+=1

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3): # 4 times (last 3 columns not possible to make a positive slope diagonal of length = 4)
		col=c
		count=0

		#Main Loop
		for r in reversed(range(ROW_COUNT)): #5,4,3,2,1,0
			if not is_within_bounds(col,r):
				break
			if(board[r][col]==piece):
				count+=1
			else:
				if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
					wins+=1
				count=0
			col+=1
		if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
			wins+=1

		#handle 2 remaining cases
		if(c ==0):
			for i in range(1,3):
				count=0
				col=c
				for r in reversed(range(ROW_COUNT-i)):
					if(board[r][col]==piece):
						count+=1
					else:
						if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
							wins+=1
						count=0
					col+=1
				if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
					wins+=1

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3): # 4 times (last 3 columns not possible to make a positive slope diagonal of length = 4)
		col=c
		count=0

		#Main Loop
		for r in range(ROW_COUNT): #0,1,2,3,4,5
			if not is_within_bounds(col,r):
				break
			if(board[r][col]==piece):
				count+=1
			else:
				if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
					wins+=1
				count=0
			col+=1
		if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
			wins+=1

		#handle 2 remaining cases
		if(c ==0):
			for i in range(1,3):
				count=0
				col=c
				for r in range(i,ROW_COUNT):
					if(board[r][col]==piece):
						count+=1
					else:
						if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
							wins+=1
						count=0
					col+=1
				if(count>=WINDOW_LENGTH): #positively sloped diagonal: maximum = 6 -> only one sequence is possible
					wins+=1

	#return total number of wins
	return wins

#Get total number of new wins, depending on count
def getNewWins(count):
	if(count>=WINDOW_LENGTH):
		r = count%WINDOW_LENGTH
		extrawins=r+1
	else:
		extrawins=0
	return extrawins

#Count number of wins
def count_wins(board, piece):

	board=np.flip(board, 0)
	wins=0
	count=0

	# Check horizontal locations for win
	for r in range(ROW_COUNT):
		count=0 #for every row
		for c in range(COLUMN_COUNT):
			if(board[r][c]==piece):
				count+=1
			else:
				wins+=getNewWins(count)
				count=0
		wins+=getNewWins(count)


	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		count=0 #for every column
		for r in range(ROW_COUNT):
			if(board[r][c]==piece):
				count+=1
			else:
				wins+=getNewWins(count)
				count=0
		wins+=getNewWins(count)

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3): # 4 times (last 3 columns not possible to make a positive slope diagonal of length = 4)
		col=c
		count=0

		#Main Loop
		for r in reversed(range(ROW_COUNT)): #5,4,3,2,1,0
			if not is_within_bounds(col,r):
				break
			if(board[r][col]==piece):
				count+=1
			else:
				wins+=getNewWins(count)
				count=0
			col+=1
		wins+=getNewWins(count)

		#handle 2 remaining cases
		if(c ==0):
			for i in range(1,3):
				count=0
				col=c
				for r in reversed(range(ROW_COUNT-i)):
					if(board[r][col]==piece):
						count+=1
					else:
						wins+=getNewWins(count)
						count=0
					col+=1
				wins+=getNewWins(count)

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3): # 4 times (last 3 columns not possible to make a positive slope diagonal of length = 4)
		col=c
		count=0

		#Main Loop
		for r in range(ROW_COUNT): #0,1,2,3,4,5
			if not is_within_bounds(col,r):
				break
			if(board[r][col]==piece):
				count+=1
			else:
				wins+=getNewWins(count)
				count=0
			col+=1
		wins+=getNewWins(count)

		#handle 2 remaining cases
		if(c ==0):
			for i in range(1,3):
				count=0
				col=c
				for r in range(i,ROW_COUNT):
					if(board[r][col]==piece):
						count+=1
					else:
						wins+=getNewWins(count)
						count=0
					col+=1
				wins+=getNewWins(count)

	#return total number of wins
	return wins
# *********************************************************************************

# AI ******************************************************************************

# Old Heuristic Function **********************************************************
#Assistant function for the Heuristic Function
def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 1000
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 3

	if window.count(opp_piece) == 4:
		score -= 800
	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 6
	elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
		score -= 1

	return score

#Heuristic Function
def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score positive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	## Score negative sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score
# ********************************************************************************

# NEW Heuristic Function *********************************************************
def isEmpty(board,row,col):
	return (board[row][col]==0)

def Piece(board,row,col,piece):
	return (board[row][col]==piece)

def isValid(row,col):
	return col<COLUMN_COUNT and row<ROW_COUNT

def getScoreOfColumn(col):
	if(col==0): return 4
	elif(col==1): return 7
	elif(col==2): return 12
	elif(col==3): return 20
	elif(col==4): return 12
	elif(col==5): return 7
	elif(col==6): return 4

def scoreOfSingleElements(board,piece):
	score=0
	for r in range(ROW_COUNT):
		for c in range(COLUMN_COUNT):
			check=True
			if(board[r][c]==piece):
				if isValid(r+1,c): #up
					if Piece(board,r+1,c,piece):
						check=False
				if isValid(r-1,c): #down
					if Piece(board,r-1,c,piece):
						check=False
				if isValid(r,c-1): #left
					if Piece(board,r,c-1,piece):
						check=False
				if isValid(r,c+1): #right
					if Piece(board,r,c+1,piece):
						check=False
				#Diagonal Movements
				if isValid(r+1,c+1): #up-right
					if Piece(board,r+1,c+1,piece):
						check=False
				if isValid(r-1,c+1): #down-right
					if Piece(board,r-1,c+1,piece):
						check=False
				if isValid(r+1,c-1): #up-left
					if Piece(board,r+1,c-1,piece):
						check=False
				if isValid(r-1,c-1): #down-left
					if Piece(board,r-1,c-1,piece):
						check=False
			if(check): score+=getScoreOfColumn(c)
	return score
				

def getBlocksScore():
	#3 in a row then block
	#4 in a row then block
	#5 in a row then block
	pass


def getCount_window(window, piece):
	count_2 = 0
	count_3 = 0
	count_4 = 0
	blocks = 0

	#Get the opponent's peice
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	#Count the piece in the window
	count_piece = window.count(piece)

	if count_piece == 4: #4 in a row
		count_4 += 1
	elif count_piece == 3 and window.count(EMPTY) == 1: #3 in a row
		count_3 += 1
	elif count_piece == 2 and window.count(EMPTY) == 2: #2 in a row
		count_2 += 1
	elif count_piece == 1 and window.count(opp_piece) ==3: #number of blocks
		blocks+=1

	return count_2, count_3, count_4,blocks

def getCounts(board,piece): #number of 4s, 3s and 2s
	count2=0
	count3=0
	count4=0
	blocks=0

    ## Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			new2,new3,new4,newblocks = getCount_window(window, piece)
			if(new3>0):
				pass
			count2+=new2
			count3+=new3
			count4+=new4
			blocks+=newblocks

	## Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			new2,new3,new4,newblocks = getCount_window(window, piece)
			count2+=new2
			count3+=new3
			count4+=new4
			blocks+=newblocks

	## Positive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			new2,new3,new4,newblocks = getCount_window(window, piece)
			count2+=new2
			count3+=new3
			count4+=new4
			blocks+=newblocks

	## Negative sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			new2,new3,new4,newblocks = getCount_window(window, piece)
			count2+=new2
			count3+=new3
			count4+=new4
			blocks+=newblocks

	return count2,count3,count4,blocks

## POINTS (WEIGHT of each feature)
# 1 connect-4 = 1000 points
# 1 connect-3 = 100 points
# 1 connect-2 = 10 points

POINTS_4 = 10000
POINTS_3 = 100
POINTS_2 = 10
POINTS_B = POINTS_4 

#Heuristic Function
def eval(board, piece):

	#Get the opponent's peice
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	#Heuristic value (initially = 0)
	hv = 0

	#feature 1: connect-4s that exist
	#feature 2: connect-3s that exist
	#feature 3: connect-2s that exist
	connected_2,connected_3,connected_4, blocks = getCounts(board,piece)

	#feature 4: connect-4s of opponent
	#feature 5: connect-3s of opponent
	#feature 6: connect-2s of opponent
	connected_2_opp,connected_3_opp, connected_4_opp,blocks_opp = getCounts(board, opp_piece)

	#feature 7: score of single element (not adjacent to anything similar)
	hv+=scoreOfSingleElements(board,piece)

	#feature 8: try to block -> if going to block more than 3 in a row, should get a higher priority
	hv+=(blocks)*POINTS_B

	#Calculate heuristic value
	hv+= POINTS_4*(connected_4 - connected_4_opp)
	hv+= POINTS_3*(connected_3 - connected_3_opp)
	hv+= POINTS_2*(connected_2 - connected_2_opp)

	return hv

#Get the terminal node
def is_terminal_node(board):
	return len(get_valid_locations(board)) == 0

# Minimax tree **************************************************************************************************
class Node:
	def __init__(self, parent,depth):
		self.score = None  #undefined at first
		self.parent = parent
		self.children= []
		self.depth = depth

	def addChild(self,node):
		self.children.append(node)

	def setParent(self,parent):
		self.parent=parent

	def setScore(self,score):
		self.score=score

class Minimax_Tree:

	def __init__(self,depth):
		self.root = Node(None,0)
		self.depth=depth

	def printTree(self):
		node=self.root
		queue=[]
		queue.append(node)
		current_depth=-1
		max_depth = self.depth
		text=[]
		text.append(str(node.score))
		nodes_expanded=0

		#Loop on all nodes
		while(queue):

			node=queue.pop(0)

			if(node):

				nodes_expanded+=1

				#If depth changed, print level and whether it's a min or max
				if(current_depth < node.depth):
					if(nodes_expanded!=1):
						print('\n')
					current_depth=node.depth
					print(f'Level {current_depth}',end =" ")
					if(current_depth%2==0):
						print('(MAX):',end =" ")
					else:
						print('(MIN):',end =" ")

				#Print score of node
				print(node.score,end =" ")

				#For child in children append to queue
				for child in node.children:
					queue.append(child)
					text.append(str(child.score))
				x=len(node.children)
				if(x==0):
					max_depth=node.depth
				elif(current_depth!=max_depth):
					for i in range(x,7):
						text.append('None')
						queue.append(None)
			#Not a node (None)
			elif(current_depth!=max_depth ): 
				for i in range(7):
					text.append('None')
					queue.append(None)
		print('')
		
		return text,nodes_expanded

# ***************************************************************************************************************

# Minmax with/without alpha beta pruning ************************************************************************
# pruning: flag to indicate whether to use alpha-beta pruning or not

#Minimizer (Player)
def Minimize(board,depth,alpha, beta, pruning, node):
	#Check if leaf node
	if is_terminal_node(board): #if leaf node
		AI_wins=count_wins(board, AI_PIECE)
		Player_wins=count_wins(board, PLAYER_PIECE)
		if(AI_wins>Player_wins):
			return None, 10000000000
		elif(AI_wins<Player_wins):
			return None, -10000000000
		else: return None, 0 #draw
	#check if maximum depth reached
	if depth==0:
		#return None, score_position(board, AI_PIECE)		#call the heuristic function to give an estimate
		return None, eval(board, AI_PIECE)

	valid_locations = get_valid_locations(board)
	min_score = math.inf
	min_column = random.choice(valid_locations)
	for col in valid_locations:
		child=Node(node,node.depth+1) #create child node
		node.addChild(child) #append child to node's children
		row = get_next_open_row(board, col)
		b_copy = copy.deepcopy(board)
		drop_piece(b_copy, row, col, AI_PIECE)
		new_score = Maximize(b_copy, depth-1, alpha, beta, pruning, child)[1]
		child.setScore(new_score) #set score of child node
		if new_score < min_score:
			min_score = new_score
			min_column = col
		if(pruning): #If with alpha-beta pruning
			beta = min(beta, min_score)
			if alpha >= beta:
				break
	node.setScore(min_score)
	return min_column, min_score

#Maximizer (AI)
def Maximize(board,depth, alpha, beta,pruning, node):
	#Check if leaf node
	if is_terminal_node(board):
		AI_wins=count_wins(board, AI_PIECE)
		Player_wins=count_wins(board, PLAYER_PIECE)
		if(AI_wins>Player_wins):
			return None, 10000000000
		elif(AI_wins<Player_wins):
			return None, -10000000000
		else: return None, 0 #draw
	#check if maximum depth reached
	if depth==0:
		#return None, score_position(board, AI_PIECE)		#call the heuristic function to give an estimate
		return None, eval(board, AI_PIECE)

	#Get all valid columns
	valid_locations = get_valid_locations(board)
	max_score = -math.inf
	max_column = random.choice(valid_locations)
	for col in valid_locations:
		child=Node(node,node.depth+1) #create child node
		node.addChild(child) #append child to node's children
		row = get_next_open_row(board, col)
		b_copy = copy.deepcopy(board)
		drop_piece(b_copy, row, col, AI_PIECE)
		new_score = Minimize(b_copy, depth-1, alpha, beta, pruning, child)[1]
		child.setScore(new_score) #set score of child node
		if new_score > max_score:
			max_score = new_score
			max_column = col
		if(pruning): #If with alpha-beta pruning
			alpha = max(alpha, max_score)
			if alpha >= beta:
				break
	node.setScore(max_score)
	return max_column, max_score

def Minimax(board,depth,alpha, beta,pruning):
	tree = Minimax_Tree(depth)
	column, max = Maximize(board,depth,alpha, beta, pruning, tree.root)
	return tree, column

# ************************************************************************************************************

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations
# *********************************************************************************

# GUI *****************************************************************************
def draw_board(board, screen):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+2*SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+2*SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
# **********************************************************************************


# Connect 4 Game Class**************************************************************
class Connect4:

	def __init__(self):
		self.board = create_board()
		self.game_over = False

		pygame.init()
		pygame.display.set_caption('Connect-4')
		self.screen = pygame.display.set_mode(size)
		draw_board(self.board,self.screen)
		pygame.display.update()

		self.myfont = pygame.font.SysFont("monospace", 75)
		self.myfont2 = pygame.font.SysFont("monospace", 40)
		self.turn = random.randint(PLAYER, AI)

	#Multi-player
	def PlayerVsPlayer(self):

		#Count number of wins for each
		numofwins_player1=0
		numofwins_player2=0

		#Maximum number of plays
		max_plays= ROW_COUNT* COLUMN_COUNT

		#Valid Move Boolean
		valid_move=False

		while not self.game_over:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if 	event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(self.screen, WHITE, (0,0, width, 2*SQUARESIZE))
					label = self.myfont2.render("Player1: "+str(numofwins_player1)+"   Player2: "+str(numofwins_player2), 1, BLACK)
					self.screen.blit(label, (5,5))
					posx = event.pos[0]
					if self.turn == 0:
						pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE+SQUARESIZE/2)), RADIUS)
					else:
						pygame.draw.circle(self.screen, YELLOW, (posx, int(SQUARESIZE+SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(self.screen, WHITE, (0,0, width,2*SQUARESIZE))

					# Ask for Player 1 Input
					if self.turn == PLAYER:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if is_valid_location(self.board, col):
							valid_move=True
							row = get_next_open_row(self.board, col)
							drop_piece(self.board, row, col, 1)

							#if winning_move(self.board, 1):
							#	numofwins_player1+=1
							numofwins_player1=count_wins(self.board, 1)


					# # Ask for Player 2 Input
					else:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if is_valid_location(self.board, col):
							valid_move=True
							row = get_next_open_row(self.board, col)
							drop_piece(self.board, row, col, 2)

							#if winning_move(self.board, 2):
							#	numofwins_player2+=1
							numofwins_player2=count_wins(self.board, 2)

					#Update Board
					label = self.myfont2.render("Player1: "+str(numofwins_player1)+"   Player2: "+str(numofwins_player2), 1, BLACK)
					self.screen.blit(label, (5,5))
					draw_board(self.board,self.screen)

					#If move was valid
					if(valid_move):

						#Change Turn
						self.turn += 1
						self.turn = self.turn % 2

						#Decrement remaining number of possible moves
						max_plays-=1
						if(max_plays==0):
							self.game_over=True

					
					#Reset it to false
					valid_move=False


		#Check who wins
		if(numofwins_player1>numofwins_player2):
			label = self.myfont.render("Player 1 wins!!", 1, RED)
			self.screen.blit(label, (40,10))
		elif(numofwins_player1 < numofwins_player2):
			label = self.myfont.render("Player 2 wins!!", 1, YELLOW)
			self.screen.blit(label, (40,10))
		else:
			label = self.myfont.render("DRAW !!", 1, BLUE)
			self.screen.blit(label, (40,10))

		#Update Board
		draw_board(self.board,self.screen)

		#Check Mouse Events
		while(1):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


	#Play Against the Computer (AI)
	def PlayerVsComputer(self, depth, pruning):

		#Count number of wins for each
		numofwins_player=0
		numofwins_AI=0
		move_num_AI=1

		#Maximum number of plays
		max_plays= ROW_COUNT* COLUMN_COUNT

		while not self.game_over:

			#Check Mouse Events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(self.screen, WHITE, (0,0, width, 2*SQUARESIZE))
					label = self.myfont2.render("Player: "+str(numofwins_player)+"         AI: "+str(numofwins_AI), 1, BLACK)
					self.screen.blit(label, (5,5))
					posx = event.pos[0]
					if self.turn == PLAYER:
						pygame.draw.circle(self.screen, RED, (posx, int(SQUARESIZE+SQUARESIZE/2)), RADIUS)

				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(self.screen, WHITE, (0,0, width, 2*SQUARESIZE))

					# Player's 1 turn
					if self.turn == PLAYER:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if is_valid_location(self.board, col):
							row = get_next_open_row(self.board, col)
							drop_piece(self.board, row, col, PLAYER_PIECE)
							draw_board(self.board,self.screen)
							numofwins_player=count_wins(self.board, PLAYER_PIECE)

							self.turn += 1
							self.turn = self.turn % 2
							#Decrement remaining number of possible moves
							max_plays-=1
							if(max_plays==0):
								self.game_over=True


			# AI's turn to play
			if self.turn == AI and not self.game_over:
				label = self.myfont2.render("Player: "+str(numofwins_player)+"         AI: "+str(numofwins_AI), 1, BLACK)
				self.screen.blit(label, (5,5))
				#Update Board
				draw_board(self.board,self.screen)
				alpha = -math.inf
				beta = math.inf

				#Minimax Tree (Calculate time taken and nodes expanded to find a move) + print tree
				print(f"AI's move #{move_num_AI}*****************************************************************")
				move_num_AI+=1
				start = timeit.default_timer()  #start the timer
				tree, col = Minimax(self.board, depth,alpha, beta, pruning) #AI is tha maximizing player
				stop = timeit.default_timer()   #stop the timer
				runningTime=(stop-start)
				text,nodes_expanded = tree.printTree()
#				plot_tree(depth, 7, text)
				if(runningTime>1): #greater than 1s
					print(f'\nRunning Time = {runningTime} s')
				else:
					print(f'\nRunning Time = {runningTime*1000} ms')
				print(f'Nodes Expanded = {nodes_expanded}')
				print('*****************************************************************************')

				if is_valid_location(self.board, col):
					#pygame.time.wait(500)
					row = get_next_open_row(self.board, col)
					drop_piece(self.board, row, col, AI_PIECE)

					numofwins_AI=count_wins(self.board, AI_PIECE)

					draw_board(self.board,self.screen)
					self.turn += 1
					self.turn = self.turn % 2

					#Decrement remaining number of possible moves
					max_plays-=1
					if(max_plays==0):
						self.game_over=True

			label = self.myfont2.render("Player: "+str(numofwins_player)+"         AI: "+str(numofwins_AI), 1, BLACK)
			self.screen.blit(label, (5,5))
			#Update Board
			draw_board(self.board,self.screen)


		#Check who wins
		if(numofwins_player>numofwins_AI):
			label = self.myfont.render("Player 1 wins!!", 1, RED)
			self.screen.blit(label, (20,SQUARESIZE+10))
		elif(numofwins_player < numofwins_AI):
			label = self.myfont.render("Computer wins!!", 1, YELLOW)
			self.screen.blit(label, (20,SQUARESIZE+10))
		else:
			label = self.myfont.render("DRAW !!", 1, BLUE)
			self.screen.blit(label, (20,SQUARESIZE+10))

		#Update Board
		draw_board(self.board,self.screen)

		#Check Mouse Events
		while(1):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

# ***********************************************************************************

# #Defining the main function
# def main():
# 	#maximum depth allowed taken as input from GUI
# 	depth=4
# 	#With/Without Alpha-Beta pruning taken as input from GUI
# 	pruning = True
# 	game = Connect4()
# 	game.PlayerVsComputer(depth,pruning)

# # Using the special variable
# # __name__ to execute the main function
# if __name__=="__main__":
#     main()