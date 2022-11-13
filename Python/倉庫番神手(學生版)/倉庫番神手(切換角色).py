# Star Pusher (a Sokoban clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, copy, os, pygame
from pygame.locals import *

FPS = 30 		
WINWIDTH = 800 	# 遊戲視窗寬度
WINHEIGHT = 600 # 遊戲視窗長度
HALF_WINWIDTH = int(WINWIDTH / 2)	
HALF_WINHEIGHT = int(WINHEIGHT / 2)	


TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

CAM_MOVE_SPEED = 5 


OUTSIDE_DECORATION_PCT = 20

BRIGHTBLUE = (  0, 170, 255) 
WHITE      = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main(): # OK
	global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

	# 初始變數
	pygame.init()
	FPSCLOCK = pygame.time.Clock()

	# 設定視窗大小
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

	pygame.display.set_caption('Star Pusher')				# 設定視窗名稱
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)	# 設定文字字體與大小
	
	IMAGESDICT = {'uncovered goal': pygame.image.load('RedSelector.png'),
				  'covered goal': pygame.image.load('Selector.png'),
				  'star': pygame.image.load('Star.png'),
				  'corner': pygame.image.load('Wall_Block_Tall.png'),
				  'wall': pygame.image.load('Wood_Block_Tall.png'),
				  'inside floor': pygame.image.load('Plain_Block.png'),
				  'outside floor': pygame.image.load('Grass_Block.png'),
				  'title': pygame.image.load('star_title.png'),
				  'solved': pygame.image.load('star_solved.png'),
				  'princess': pygame.image.load('princess.png'),
				  'boy': pygame.image.load('boy.png'),
				  'catgirl': pygame.image.load('catgirl.png'),
				  'horngirl': pygame.image.load('horngirl.png'),
				  'pinkgirl': pygame.image.load('pinkgirl.png'),
				  'rock': pygame.image.load('Rock.png'),
				  'short tree': pygame.image.load('Tree_Short.png'),
				  'tall tree': pygame.image.load('Tree_Tall.png'),
				  'ugly tree': pygame.image.load('Tree_Ugly.png')
                   }

	# 關卡文件中的文字，對應到代表的圖檔
	TILEMAPPING = {'x': IMAGESDICT['corner'],
				   '#': IMAGESDICT['wall'],
				   'o': IMAGESDICT['inside floor'],
				   ' ': IMAGESDICT['outside floor']}
	OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
						  '2': IMAGESDICT['short tree'],
						  '3': IMAGESDICT['tall tree'],
						  '4': IMAGESDICT['ugly tree']}

	
	currentImage = 0   

	PLAYERIMAGES = [IMAGESDICT['princess']    #任務三:角色list
                    ]

	startScreen() # 顯示開始遊玩的畫面

	levels = readLevelsFile('starPusherLevels.txt') # 讀入關卡文件
	currentLevelIndex = 0                           # 設定關卡

	# 主要遊戲迴圈，依據reslut的結果，判斷要上一關或是下一關
	while True:  
		result = runLevel(levels, currentLevelIndex) 

		if result in ('solved', 'next'): 
			currentLevelIndex += 1

			if currentLevelIndex >= len(levels):     #任務五：切換上一關跟下一關
				currentLevelIndex = 0 

		elif result == 'back': 
			currentLevelIndex -= 1 

			if currentLevelIndex < 0:           
				currentLevelIndex = len(levels)-1

		elif result == 'reset':    
			pass 


def runLevel(levels, levelNum): 
	global currentImage

	levelObj = levels[levelNum] 

	mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player']) 

	gameStateObj = copy.deepcopy(levelObj['startState']) 

	mapNeedsRedraw = True # true代表需要重畫地圖

	# 設定關卡文字內容、字體以及顯示位置
	levelSurf = BASICFONT.render('Level %s of %s' % (levelNum + 1, len(levels)), 1, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.bottomleft = (20, WINHEIGHT - 35)


	mapWidth = len(mapObj) * TILEWIDTH								
	mapHeight = (len(mapObj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT 
	MAX_CAM_X_PAN = abs(HALF_WINHEIGHT - int(mapHeight / 2)) + TILEWIDTH	
	MAX_CAM_Y_PAN = abs(HALF_WINWIDTH - int(mapWidth / 2)) + TILEHEIGHT 	

	levelIsComplete = False
	
	
	cameraOffsetX = 0
	cameraOffsetY = 0


	cameraUp = False
	cameraDown = False
	cameraLeft = False
	cameraRight = False

	while True: 
		
		playerMoveTo = None   
		keyPressed = False     


		for event in pygame.event.get(): # 按鈕事件監聽迴圈
			if event.type == pygame.QUIT:
				terminate() # 關閉遊戲

			elif event.type == pygame.KEYDOWN:     
				
				keyPressed = True
				if event.key == pygame.K_LEFT:   
					playerMoveTo = LEFT
				elif event.key == pygame.K_RIGHT: 
					playerMoveTo = RIGHT
				elif event.key == pygame.K_UP:     
					playerMoveTo = UP
				elif event.key == pygame.K_DOWN:   
					playerMoveTo = DOWN

				# 相機移動
				elif event.key == pygame.K_a:
					cameraLeft = True
				elif event.key == pygame.K_d:
					cameraRight = True
				elif event.key == pygame.K_w:
					cameraUp = True
				elif event.key == pygame.K_s:
					cameraDown = True

				elif event.key == pygame.K_n:
					return 'next'
				elif event.key == pygame.K_b:
					return 'back'

				elif event.key == pygame.K_ESCAPE:
					terminate() # 關閉遊戲
                    
				elif event.key == pygame.K_BACKSPACE:
					return 'reset'
                
				elif event.key == :              #任務四：切換人物角色
					
					currentImage 
					if currentImage >= len(): 
						currentImage = 
					mapNeedsRedraw = True

			elif event.type == pygame.KEYUP:
				# 取消相機的移動
				if event.key == pygame.K_a:
					cameraLeft = False
				elif event.key == pygame.K_d:
					cameraRight = False
				elif event.key == pygame.K_w:
					cameraUp = False
				elif event.key == pygame.K_s:
					cameraDown = False

		if playerMoveTo != None and not levelIsComplete:
			# 按下移動鍵，移動角色
			# 在可以推動星星的情況下，推動星星
			moved = makeMove(mapObj, gameStateObj, playerMoveTo)

			if moved: 							 # 若可以移動
				gameStateObj['stepCounter'] += 1 # 則計步器增加1
				mapNeedsRedraw = True

			if isLevelFinished(levelObj, gameStateObj):
				levelIsComplete = True 	# 用來顯示"solved!!"的過關提示
				keyPressed = False		

		DISPLAYSURF.fill(BGCOLOR)

		if mapNeedsRedraw: 
			mapSurf = drawMap(mapObj, gameStateObj, levelObj['goals']) 
			mapNeedsRedraw = False 

		# 根據相機的移動速度，調整相機的位置
		if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
			cameraOffsetY += CAM_MOVE_SPEED
		elif cameraDown and cameraOffsetY > -MAX_CAM_X_PAN:
			cameraOffsetY -= CAM_MOVE_SPEED
		if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
			cameraOffsetX += CAM_MOVE_SPEED
		elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
			cameraOffsetX -= CAM_MOVE_SPEED

		mapSurfRect = mapSurf.get_rect()
		mapSurfRect.center = (HALF_WINWIDTH + cameraOffsetX, HALF_WINHEIGHT + cameraOffsetY)

		
		DISPLAYSURF.blit(mapSurf, mapSurfRect)

		DISPLAYSURF.blit(levelSurf, levelRect) 

		stepSurf = BASICFONT.render('Steps: %s' % (gameStateObj['stepCounter']), 1, TEXTCOLOR) 
		stepRect = stepSurf.get_rect()
		stepRect.bottomleft = (20, WINHEIGHT - 10)
		DISPLAYSURF.blit(stepSurf, stepRect)

		# 如果過關了，繪製過關畫面到螢幕上
		if levelIsComplete: 
			solvedRect = IMAGESDICT['solved'].get_rect()
			solvedRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
			DISPLAYSURF.blit(IMAGESDICT['solved'], solvedRect)

			if keyPressed:
				return 'solved'

		pygame.display.update() 
		FPSCLOCK.tick()


def isWall(mapObj, x, y): # OK
	
	if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]): 
		return False 

	elif mapObj[x][y] in ('#', 'x'):
		return True # 該格為牆壁

	return False


def decorateMap(mapObj, startxy): # OK
	
	startx, starty = startxy 			# 獲得玩家初始位置

	mapObjCopy = copy.deepcopy(mapObj) 	

	
	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):
			if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
				mapObjCopy[x][y] = ' '

	floodFill(mapObjCopy, startx, starty, ' ', 'o')

	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):

			if mapObjCopy[x][y] == '#':	

			
				if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
				   (isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
				   (isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
				   (isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
					mapObjCopy[x][y] = 'x' 

			
			elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
				mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

	return mapObjCopy 


def isBlocked(mapObj, gameStateObj, x, y):
	

	if isWall(mapObj, x, y): 
		return True

	elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]): # x、y超出地圖範圍
		return True 

	elif (x, y) in gameStateObj['stars']: # 被星星卡住
		return True 

	return False# OK


def makeMove(mapObj, gameStateObj, playerMoveTo): 
	

	playerx, playery = gameStateObj['player']	# 獲得角色目前位置

	stars = gameStateObj['stars']	# 獲得星星的位置

	
	if playerMoveTo == UP:
		xOffset = 0
		yOffset = -1
	elif playerMoveTo == RIGHT:
		xOffset = 1
		yOffset = 0
	elif playerMoveTo == DOWN:
		xOffset = 0
		yOffset = 1
	elif playerMoveTo == LEFT:
		xOffset = -1
		yOffset = 0

	if isWall(mapObj, playerx + xOffset, playery + yOffset): 
		return False
	else:
		if (playerx + xOffset, playery + yOffset) in stars:
			# 要移動的座標上有一顆星星，判斷是否可以推動該星星
			if not isBlocked(mapObj, gameStateObj, playerx + (xOffset*2), playery + (yOffset*2)):
				# 移動星星
				ind = stars.index((playerx + xOffset, playery + yOffset))
				stars[ind] = (stars[ind][0] + xOffset, stars[ind][1] + yOffset)
			else: # 無法移動星星，直接回傳false
				return False

		# 移動角色的座標，並回傳True
		gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
		return True


def startScreen(): #OK
	
		
	titleRect = IMAGESDICT['title'].get_rect()	#建置一個開始畫面的rect物件
	topCoord = 50 				
	titleRect.top = topCoord 
	titleRect.centerx = HALF_WINWIDTH
	topCoord += titleRect.height  

	# 建立要顯示在螢幕的文字list
	instructionText = ['Push the stars over the marks.',
					   'Arrow keys to move, WASD for camera control, P to change character.',
					   'Backspace to reset level, Esc to quit.',
					   'N for next level, B to go back a level.']

	# 設定開始畫面的背景顏色
	DISPLAYSURF.fill(BGCOLOR)

	# 將title圖檔畫到surface上
	DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

	# 定位文字的位置以及畫出文字
	for i in range(len(instructionText)):
		instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR) 	
		instRect = instSurf.get_rect()									
		topCoord += 10 													
		instRect.top = topCoord
		instRect.centerx = HALF_WINWIDTH
		topCoord += instRect.height 
		DISPLAYSURF.blit(instSurf, instRect)	

	while True: 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate() # 離開遊戲
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					terminate() # 離開遊戲

				return 

		pygame.display.update() # 將surface的內容顯示在螢幕上
		FPSCLOCK.tick()


def readLevelsFile(filename): # OK
	assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
	mapFile = open(filename, 'r')               # 開啟檔案
	content = mapFile.readlines() + ['\r\n']    # 讀入檔案
	mapFile.close()                             # 關閉檔案

	levels = []         # 存放每個關卡物件的list
	levelNum = 0        
	mapTextLines = []   # 用來暫存每關的文字
	mapObj = []			# 根據mapTextLines製作的物件(暫存)

	
	for lineNum in range(len(content)):

		line = content[lineNum].rstrip('\r\n')	

		if ';' in line:						
			line = line[:line.find(';')]	

		if line != '':					
			mapTextLines.append(line)	


		elif line == '' and len(mapTextLines) > 0:	

			
			maxWidth = -1
			for i in range(len(mapTextLines)):
				if len(mapTextLines[i]) > maxWidth:
					maxWidth = len(mapTextLines[i])

			for i in range(len(mapTextLines)):
				mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

			for x in range(len(mapTextLines[0])):	
				mapObj.append([])

			for y in range(len(mapTextLines)):		
				for x in range(maxWidth):
					mapObj[x].append(mapTextLines[y][x])

			startx = None # 紀錄玩家初始位置
			starty = None
			goals = [] 
			stars = [] 

			for x in range(maxWidth):
				for y in range(len(mapObj[x])):
					
					if mapObj[x][y] in ('@', '+'): 
						startx = x
						starty = y

					if mapObj[x][y] in ('.', '+', '*'):
						goals.append((x, y))

					if mapObj[x][y] in ('$', '*'):
						# '$' is star
						stars.append((x, y))

			# 檢查玩家的初始位置、星星與目標的位置是否有錯，以及錯誤訊息
			assert startx != None and starty != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (levelNum+1, lineNum, filename)
			assert len(goals) > 0, 'Level %s (around line %s) in %s must have at least one goal.' % (levelNum+1, lineNum, filename)
			assert len(stars) >= len(goals), 'Level %s (around line %s) in %s is impossible to solve. It has %s goals but only %s stars.' % (levelNum+1, lineNum, filename, len(goals), len(stars))

			gameStateObj = {'player': (startx, starty),
							'stepCounter': 0,
							'stars': stars}
			levelObj = {'width': maxWidth,
						'height': len(mapObj),
						'mapObj': mapObj,
						'goals': goals,
						'startState': gameStateObj}

			levels.append(levelObj)	

			mapTextLines = []
			mapObj = []
			gameStateObj = {}
			levelNum += 1

	return levels # 回傳處理完的level物件


def floodFill(mapObj, x, y, oldCharacter, newCharacter): 

	if mapObj[x][y] == oldCharacter:
		mapObj[x][y] = newCharacter

	if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
		floodFill(mapObj, x+1, y, oldCharacter, newCharacter) 
	if x > 0 and mapObj[x-1][y] == oldCharacter:
		floodFill(mapObj, x-1, y, oldCharacter, newCharacter) 
	if y < len(mapObj[x]) - 1 and mapObj[x][y+1] == oldCharacter:
		floodFill(mapObj, x, y+1, oldCharacter, newCharacter) 
	if y > 0 and mapObj[x][y-1] == oldCharacter:
		floodFill(mapObj, x, y-1, oldCharacter, newCharacter) 


def drawMap(mapObj, gameStateObj, goals): 
	
	# 先計算地圖的寬度及高度
	mapSurfWidth = len(mapObj) * TILEWIDTH
	mapSurfHeight = (len(mapObj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
	mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight)) 
	mapSurf.fill(BGCOLOR)

	
	for x in range(len(mapObj)):
		for y in range(len(mapObj[x])):

			spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT)) # 創建一個方塊
			if mapObj[x][y] in TILEMAPPING: 
				baseTile = TILEMAPPING[mapObj[x][y]]
			elif mapObj[x][y] in OUTSIDEDECOMAPPING: 
				baseTile = TILEMAPPING[' ']

			# 先繪製出牆壁的部分
			mapSurf.blit(baseTile, spaceRect)

			if mapObj[x][y] in OUTSIDEDECOMAPPING:
				# 畫出裝飾物
				mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)

			elif (x, y) in gameStateObj['stars']:
				if (x, y) in goals: 
					mapSurf.blit(IMAGESDICT['covered goal'], spaceRect) 

				mapSurf.blit(IMAGESDICT['star'], spaceRect)

			elif (x, y) in goals: 
				mapSurf.blit(IMAGESDICT['uncovered goal'], spaceRect) 

			if (x, y) == gameStateObj['player']: 
				mapSurf.blit(PLAYERIMAGES[currentImage], spaceRect)

	return mapSurf 


def isLevelFinished(levelObj, gameStateObj): 
	
	for goal in levelObj['goals']:
		if goal not in gameStateObj['stars']:
			return False 
	return True

def terminate(): 

	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()