class Grid():
    def __init__(self, width=0, height=0, initial=[]):
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                default = {}
                for key, val in initial:
                    default[key] = val
                row.append(default)
            self.grid.append(row)
            

    def save(url):
        print("This doesn't do anything yet!")

    def load(url):
        return None

class Gameboard(Grid):
    def __init__(self):
        Grid.__init__(self, 8, 8, [("token","empty")])
        for x in range(8):
            for y in range(8):
                if(y < 2):
                    if((x+y)%2 == 1):
                        self.setToken(x, y, "black")
                if(y > 5):
                    if((x+y)%2 == 1):
                        self.setToken(x, y, "white")

    def setToken(self, x, y, color):
        self.grid[x][y]["token"] = color
        #self.grid[1][1]["token"] = color

    def getToken(self, x, y):
        return self.grid[x][y]["token"]

    def validMoves(self, x, y):
        moves = []
        token = self.getToken(x, y)
        king = "K" in token
        token = token.split()[0]
        
        if(token == "empty"):
            return moves
        if(x < 7 and y < 7 and
           self.getToken(x+1, y+1) == "empty" and
           (token == "black" or king)):
            moves.append((x+1,y+1))     
        if(x > 0 and y < 7 and
           self.getToken(x-1, y+1) == "empty" and
           (token == "black" or king)):
            moves.append((x-1,y+1))
        if(x < 7 and y > 0 and
           self.getToken(x+1, y-1) == "empty" and
           (token == "white" or king)):
            moves.append((x+1,y-1))
        if(x > 0 and y > 0 and
           self.getToken(x-1, y-1) == "empty" and
           (token == "white" or king)):
            moves.append((x-1,y-1))

        return moves

    def move(self, x0, y0, x1, y1):
        if(not (x1,y1) in self.validMoves(x0,y0)):
            return [], False
        
        token = self.getToken(x0, y0)
        
        jumps = self.jumps(x1, y1, token)
        self.setToken(x0,y0, "empty")
        self.setToken(x1,y1, token)

        if(y1 == 7 and "black" in token):
            self.setToken(x1,y1, token + " K")

        if(y1 == 0 and "white" in token):
            self.setToken(x1,y1, token + " K")
        
        return jumps, True

    def jumps(self, x, y, token):
        king = "K" in token
        token = token.split()[0]
        jumps = []

        if(x < 6 and y < 6 and
           self.getToken(x+1, y+1) == "black" and
           self.getToken(x+2, y+2) == "empty" and
           (token == "white" or king)):
            jumps.append((x+1,y+1))

        if(x > 1 and y < 6 and
           self.getToken(x-1, y+1) == "black" and
           self.getToken(x-2, y+2) == "empty" and
           (token == "white" or king)):
            jumps.append((x-1,y+1))

        if(x < 6 and y > 2 and
           self.getToken(x+1, y-1) == "white" and
           self.getToken(x+2, y-2) == "empty" and
           (token == "black" or king)):
            jumps.append((x+1,y-1))

        if(x > 2 and y > 2 and
           self.getToken(x-1, y-1) == "white" and
           self.getToken(x-2, y-2) == "empty" and
           (token == "black" or king)):
            jumps.append((x-1,y-1))
        
        return jumps

    def jump(self, x0, y0, x1, y1, xj, yj):
        token = self.getToken(x, y)
        jumps = self.jumps(x0, y0, token)
        king = "K" in token
        token = token.split()[0]
        if((x1,y1) not in jumps):
            return [], False

        self.setToken(x0,y0, "empty")
        self.setToken(xj,yj, "empty")
        self.setToken(x1,y1, token)

        if(y1 == 7 and "black" in token):
            self.setToken(x1,y1, token + " K")

        if(y1 == 0 and "white" in token):
            self.setToken(x1,y1, token + " K")
        
        return getJumps(x1, y1, token), True
    
