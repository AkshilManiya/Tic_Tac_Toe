import tkinter
from tkinter import messagebox
import random

def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] == 'X' or b[i][0] == b[i][1] == b[i][2] == 'O':
            return True
        if b[0][i] == b[1][i] == b[2][i] == 'X' or b[0][i] == b[1][i] == b[2][i] == 'O':
            return True
    if   b[0][0] == b[1][1] == b[2][2] == 'X' or b[0][0] == b[1][1] == b[2][2] == 'O':
        return True
    if b[0][2] == b[1][1] == b[2][0] == 'X' or b[0][2] == b[1][1] == b[2][0] == 'O':
        return True
    return False
        
class computer_Player:
    move = [[0,1,2], [1,2,0], [2,0,1],
            [3,4,5], [4,5,3], [5,3,4],
            [6,7,8], [7,8,6], [8,6,7],
            [0,3,6], [3,6,0], [6,0,3],
            [1,4,7], [4,7,1], [7,1,4],
            [2,5,8], [5,8,2], [8,2,5],
            [0,4,8], [4,8,0], [8,0,4],
            [2,4,6], [4,6,2], [6,2,4]]
    num = {0:[0,0],1:[0,1],2:[0,2],
           3:[1,0],4:[1,1],5:[1,2],
           6:[2,0],7:[2,1],8:[2,2]}
        
    def place(self, board):
        self.board = board
        self.box = [self.board[0][0],self.board[0][1],self.board[0][2],
                    self.board[1][0],self.board[1][1],self.board[1][2],
                    self.board[2][0],self.board[2][1],self.board[2][2]]
        d = self.defence()
        if d != None:
            self.board[self.num[d][0]][self.num[d][1]] = 'X'
            de = check_winner(self.board)
            self.board[self.num[d][0]][self.num[d][1]] = ' '
        else:
            de = False
            
        a = self.attack()
        if a != None:
            self.board[self.num[a][0]][self.num[a][1]] = 'O'
            ac = check_winner(self.board)
            self.board[self.num[a][0]][self.num[a][1]] = ' '
        else:
            ac = False
            
        if ac == de == True:
            return self.num[d][0], self.num[d][1]
        elif ac == True and de == False:
            return self.num[a][0], self.num[a][1]
        elif ac == False and de == True:
            return self.num[d][0], self.num[d][1]
        else:
            el = random.choice(self.blanks_count())
            return self.num[el][0], self.num[el][1]
        
    def blanks_count(self):
        blanks = []
        z = 0
        for i in self.box:
            if i == ' ':
                blanks.append(z)
            z+=1
        return blanks
    
    def defence(self):
        for i in self.move:
            if self.box[i[0]]==self.box[i[1]]=='X':
                a = i[2]
                if a in self.blanks_count():
                    break
            else:
                a = None
        return a
    
    def attack(self):
        for i in self.move:
            if self.box[i[0]]==self.box[i[1]]=='O':
                a = i[2]
                if a in self.blanks_count():
                    break
            else:
                a = None
        return a
        
class Play_Frame(tkinter.Frame):
    move = 'O'
    mode = 0
    turns = 0
    def __init__(self, mode):
        super().__init__()
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.mode = mode
        if self.mode==1:
            self.a = computer_Player()
        for i in range(3):
            for j in range(3):
                btn = tkinter.Button(self, height=5, width=10, command=lambda x=i, y=j: self.Btn_click(x, y), font=('Helvetica', 10))
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="snwe")
                
    def Btn_click(self, r, c):
        self.move = 'X' if self.move == 'O' else 'O'
        self.board[r][c]=self.move
        self.disable_btn(r, c)
        self.turns+=1
        self.finish = self.ch()
        if self.mode == 1 and self.finish == False:
            self.computer_player()
            
    def computer_player(self):
        x, y = self.a.place(self.board)
        self.move = 'X' if self.move == 'O' else 'O'
        self.board[x][y]=self.move
        self.disable_btn(x, y)
        self.turns+=1
        self.ch()
                
    def ch(self):
        if check_winner(self.board):
            if self.move == 'X':
                messagebox.showinfo("success", "Player 1 is Winner")
                self.clear()
                return True
            else:
                if self.mode==1:
                    messagebox.showinfo("success", "computer player is Winner")    
                else:
                    messagebox.showinfo("success", "Player 2 is Winner")
                self.clear()
                return True
        elif self.turns >= 9:
            messagebox.showinfo("Fail","match is drow ")
            self.clear()
            return True
        else:
            return False
        
    def disable_btn(self, x, y):
        button = self.grid_slaves(row=x, column=y)[0]
        button.configure(text=f"{self.move}")
        button.configure(state=tkinter.DISABLED)
        
    def clear(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.move = 'O'
        self.turns = 0
        for i in range(3):
            for j in range(3):
                button = self.grid_slaves(row=i, column=j)[0]
                try:
                    button.configure(text=" ")
                    button.configure(state="active")
                except Exception as a:
                    pass


class Main_Frame(tkinter.Tk):
    mode = 0
    def __init__(self):
        super().__init__()
        self.title("tic_tac_toe")
        self.geometry("400x400")
        self.resizable(False, False)
        
        self.upper_frame = tkinter.Frame(self)
        self.upper_frame.pack(anchor="nw")
        
        back = tkinter.Button(self.upper_frame, command=self.Back, text="Back", width=5)
        back.pack(anchor="nw", expand=True, padx=3, pady=3)
        
        self.base = tkinter.Frame(self)
        self.base.pack(anchor="center" ,expand=True)
        
        computer = tkinter.Button(self.base, height=5, width=20, text="Play with computer", command= lambda : self.create_Bord(1))
        computer.pack(anchor="center", pady=15, padx=5)
        player2 = tkinter.Button(self.base, height=5, width=20, text="2 player", command= lambda : self.create_Bord(2))
        player2.pack(anchor="center", pady=15, padx=5)

    def create_Bord(self, mode):
        self.mode = mode
        
        if self.mode == 1:
            self.base.pack_forget()
            self.a = Play_Frame(1)
            self.a.pack(expand=True)
        elif self.mode == 2:
            self.base.pack_forget()
            self.b = Play_Frame(0)
            self.b.pack(expand=True)
        
    def Back(self):
        try:
            self.a.destroy()
            self.base.pack(anchor="center" ,expand=True)
        except Exception as e:
            pass
        try:
            self.b.destroy()
            self.base.pack(anchor="center" ,expand=True)
        except Exception as e:
            pass
        

if __name__ == "__main__":
    Main_Frame().mainloop()
    
    