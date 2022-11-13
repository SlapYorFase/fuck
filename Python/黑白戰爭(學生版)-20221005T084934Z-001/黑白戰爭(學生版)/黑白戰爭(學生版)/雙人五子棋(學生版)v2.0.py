import pygame
print(pygame.ver)


EMPTY = 0
BLACK = 1
WHITE = 2


black_color = [0, 0, 0]
white_color = [255, 255, 255]


class RenjuBoard(object):

    def __init__(self):
        
        self._board = [[]] * 15
        self.reset()
    
    def reset(self):    #重製棋盤
        for row in range(len(self._board)):
            self._board[row] = [EMPTY] * 15
   
    def move(self, row, col, is_black):
        if self._board[row][col] == EMPTY:
            self._board[row][col] = BLACK if is_black else WHITE
            return True
        return False
    
    def draw(self, screen): #課程任務一：利用for迴圈來畫棋盤線
        for h in range(1,16):
            pygame.draw.line(screen, black_color,
                             [40,h*40],[600,h*40] , 1)
            pygame.draw.line(screen, black_color,
                             [h*40,40],[h*40,600] , 1)
       
        pygame.draw.rect(screen, black_color, [36, 36, 568, 568], 3)

        #課程任務一：根據天元座標，畫出星位座標  
        pygame.draw.circle(screen, black_color, [320, 320], 5, 0)
        pygame.draw.circle(screen, black_color, [160, 160], 5,0)
        pygame.draw.circle(screen, black_color, [480,160 ], 5,0)
        pygame.draw.circle(screen, black_color, [160,480 ], 5,0)
        pygame.draw.circle(screen, black_color, [480, 480], 5,0)
        
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                
                if self._board[row][col] != EMPTY:
                    ccolor = black_color \
                        if self._board[row][col] == BLACK else white_color
                    
                    pos = [40 * (col + 1), 40 * (row + 1)]
                   
                    pygame.draw.circle(screen, ccolor, pos, 18, 0)

def is_win(board):
    for n in range(15):    # 判斷垂直方向勝利
        
        flag = 0     # flag是一个標籤，表示是否有連續以上五個相同颜色的棋子
      
        for b in board._board:
            if    b[n]== 1:
                flag += 1
                if flag == 5:
                    print('黑棋勝')
                    return False
            else:
            
                flag = 0    

        flag = 0
        for b in board._board:
            if b[n] == 2:
                flag += 1
                if flag == 5:
                    print('白棋勝')
                    return False
            else:
                flag = 0

        flag = 0         # 判斷水平方向勝利
        for b in board._board[n]:
            if b == 1:
                flag += 1
                if flag == 5:
                    print('黑棋勝')
                    return False
            else:
                flag = 0

        flag = 0
        for b in board._board[n]:     
            if b == 2:
                flag += 1
                if flag == 5:
                    print('白棋勝')
                    return False
            else:
                flag = 0

        for x in range(4,25):        # 判斷正斜方向勝利
            flag = 0
            for i,b in enumerate(board._board):
                if 14 >= x - i >= 0 and b[x - i] == 1:
                    flag += 1
                    if flag == 5:
                        print('黑棋勝')
                        return False
                else:
                    flag = 0

        for x in range(4,25):
            flag = 0
            for i,b in enumerate(board._board):
                if 14 >= x - i >= 0 and b[x - i] == 2:
                    flag += 1
                    if flag == 5:
                        print('白棋勝')
                        return False
                else:
                    flag = 0

        for x in range( 10,-11, -1):   #判斷反斜方向勝利
            flag = 0
            for i,b in enumerate(board._board):
                if 0 <= x + i <= 14 and b[x + i] == 1:
                    flag += 1
                    if flag == 5:
                        print('黑棋勝')
                        return False
                else:
                    flag = 0

        for x in range(10,-11 , -1):
            flag = 0
            for i,b in enumerate(board._board):
                if 0 <= x + i <= 14 and b[x + i] == 2:
                    flag += 1
                    if flag == 5:
                        print('白棋勝')
                        return False
                else:
                    flag = 0

    return True


def main():
    # 創建棋盤對象
    board = RenjuBoard()
    # 用於判斷是下黑棋還是白棋
    is_black = False
    # pygame初始化函数，固定寫法
    pygame.init()
    pygame.display.set_caption('黑白戰爭') # 改標題
    # pygame.display.set_mode()表示建立個窗口，左上角为座標原點，往右为x正向，往下为y軸正向
    screen = pygame.display.set_mode((640,640))
    # 给視窗填充颜色，颜色用三原色数字列表
    screen.fill([125,95,24])
    board.draw(screen)  
    pygame.display.flip()  # 刷新視窗

    running = True
   
    while running:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYUP:
                pass
            
            elif event.type == pygame.MOUSEBUTTONDOWN and \
                    event.button == 1:
                x, y = event.pos  
                
                row = round((y - 40) / 40)     
                col = round((x - 40) / 40)
                if board.move(row, col, is_black):
                    is_black = not is_black
                    screen.fill([125, 95, 24])
                    board.draw(screen)
                    pygame.display.flip()
                    
                    if not is_win(board):
                   
                        running = False

    pygame.quit()


if __name__ == '__main__':
    main()
