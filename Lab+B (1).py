
# coding: utf-8

# In[45]:


#make player class with it holding the piece and colour of choice
#take out parrent node,replace with opp keylist list
#----------------------------------------------------------------------------------------------------------------------
import copy
import random
from copy import deepcopy
class Game:
    
    def __init__(self,rows,columns,player1,player2):
        self.rows=rows
        self.columns= columns
        self.player1=player1
        self.player2=player2
        self.pieces1=self.player1.banner
        self.pieces2=self.player2.banner
        self.board={}
        self.limit=3
        singlerow=["." for i in range(rows)]
        for i in range(columns):
            value=i+65
            if (value<=90):
                col=chr(value)
                self.board[col]=copy.deepcopy(singlerow)
            else:
                break
        self.keylist=self.board.keys()
        self.board=self.initial_state(self.rows,self.keylist)
        self.player1.table(self.board,self)
        self.player2.table(self.board,self)
        #self.play_game(self.player1.Evasive,self.player2.tr,self.board)
    
    def play_game(self,player1h,player2h,board):
        while (True):
            move=self.minimax(None,self.player1,self.player2,player1h,-1,self.limit)
            self.display_state(self.board)
            updated=self.transition(self.player1,move[0],move[1],self.board,self.player2)
            print("Player1 chose",self.player1.banner,move[0],"to go",move[1])
            self.player1=updated[1]
            self.player2=updated[2]
            print(self.player1.banner,self.player1.game_pieces)
            print(self.player2.banner,self.player2.game_pieces)
            if(self.end_game(self.player1,self.player2)):
                print(self.player1.name," Wins")
                self.display_state(self.board)
                return 0
            move2=self.minimax(None,self.player2,self.player1,player2h,-1,self.limit)
            self.display_state(self.board)
            print(self.player2.banner,self.player2.game_pieces)
            print(self.player1.banner,self.player1.game_pieces)
            updated=self.transition(self.player2,move2[0],move2[1],self.board,self.player1)
            print("Player2 chose",self.player2.banner,move2[0],"to go",move2[1])
            self.player2=updated[1]
            self.player1=updated[2]
            if (self.end_game(self.player2,self.player1)):
                print(self.player2.name," Wins")
                self.display_state(self.board)
                return 0

        
            
    
        
                
                
  
    def initial_state(self,rows,columns):
            for num in range(2):
                for col in columns:
                    self.board[col][num]=self.pieces2
                    self.player2.game_pieces.append(col+str(num))
                    self.board[col][(rows-1)-num]=self.pieces1
                    nn=rows-1-num
                    self.player1.game_pieces.append(col+str(nn))
            return self.board
  
    def display_state(self,board):
        spacespercolumn=self.rows
        columns=sorted(self.keylist)
        for i in range((spacespercolumn)):
            currentrow=[]
            for key in columns:
                currentrow.append(board[key][i])
            print(currentrow)
        

    def transition(self,cplayer,piece,newloc,board,oplayer):
        #check if action contained enemy then delete enemy from keylist
        #fixit
        piecel=list(piece)
        piececolumn=board[piece[0]]
        piececolumn[int(piece[1])]="."
        newlocl=list(newloc)
        newcolumn=board[newlocl[0]]
        moveto=newcolumn[int(newlocl[1])]
        if (moveto!="."):
            oplayer.game_pieces.remove(newloc)
        cplayer.game_pieces.append(newloc)
        cplayer.game_pieces.remove(piece)
        newcolumn[int(newlocl[1])]=cplayer.banner
        oplayer.table(board,self)
        cplayer.table(board,self)
        return(board,cplayer,oplayer) #for min max state nodes

            
    
    def end_game(self,currentplayer,opponent):
            if not(opponent.game_pieces):
                return True
            if isinstance(currentplayer,Player1):
                for col in self.keylist:
                    if (self.board[col][0]==currentplayer.banner):
                        return True
                return False
            elif isinstance(currentplayer,Player2):
                    state=currentplayer.board
                    index=self.rows-1
                    for col in self.keylist:
                        if(self.board[col][index]==currentplayer.banner):
                            return True
                    return False
            
    #create a rootnode for eachplayer in gameplay function
    #root=Node(None, self.board, None, None)

    def minimax(self,node,currentplayer,oplayer,heuristic,depth,limit,numofactions=0):
        #root node with node, act_piece has both actions and possible actions
        #if limit reached
        gate=False
        if(depth==limit):
            return (heuristic(oplayer,currentplayer))
        if self.end_game(currentplayer,oplayer):
            return(heuristic(oplayer,currentplayer))
        #If no limit reached
        if (node==None):
            node=Node(self.board, None, None,None,None) 
            gate=True
        act_piece=currentplayer.move_generator(node.state)
        for pi_ac in act_piece:
            for act in pi_ac[1]:
                new_state=copy.deepcopy(node.state)
                ccp=copy.deepcopy(currentplayer)
                opp=copy.deepcopy(oplayer)
                result=self.transition(ccp, pi_ac[0], act,new_state,opp)
                result_state=result[0]
                nextplayerpieces=copy.deepcopy(result[2].game_pieces)
                opponentpices=copy.deepcopy(result[1].game_pieces)
                baby=Node(result_state,pi_ac[0],act,nextplayerpieces,opponentpices)
                node.children.append(baby)
        bestaction=[]
        if (gate):
            numofactions=len(node.children)
            gate=False
        depth+=1 
        nextplayer=copy.deepcopy(result[2])
        opponent=copy.deepcopy(result[1])
        while (node.children):
            next_node=node.children.pop()
            nextplayer.table(node.state,self)
            opponent.table(node.state,self)
            nextplayer.gamepieces(next_node.nextpkeylist)
            opponent.gamepieces(next_node.oplist)
            result=self.minimax(next_node,nextplayer,opponent,heuristic,depth,limit,numofactions)
            bestaction.append(result)
        if(depth==0):
            Best=currentplayer.determinebest(bestaction)
            return (Best[1],Best[2])
        if(depth==1):  
            return(currentplayer.determinebest(bestaction),node.piece,node.action)
           
        else:
            return(currentplayer.determinebest(bestaction))

        #print("These are options for",currentplayer.banner,"\n",bestaction)
        #print("\nChosen action for",depth,"is",currentplayer.determinebest(bestaction))
      
           
            
            
            
            
        
      
        
       
        
        
        
                
        
        

class Player1:
    #max
    #bottom goo

    def __init__(self,banner,name):
        self.banner=banner
        self.game_pieces=[]
        self.board=None
        self.name=name
        self.restofcollums=0
        
    def gamepieces(self,pieces):
        self.game_pieces=pieces
        
    def table(self,board,game):
        if (self.board==None):
            self.board=board
            self.restofcollums=(len(game.keylist)-1)
        else:
            self.board=board
        
    def determinebest(self, actions):
        #bestheur=max(actions,key=lambda move:move[0])
        bestheur=max(actions)
        return bestheur
    
    
   
         
            
        
    def Conqueror(self,player,opponent):
        return(0 - len(opponent.game_pieces) + random.random())
        
        
    def Evasive(self,player,opponent):
        return(len(player.game_pieces) + random.random())

    def actions(self,piece):
        #have to create two player classes
        piece=list(piece)
        piececolumn=self.board[piece[0]]
        vmove=int(piece[1])-1 
        goodactions=[]
        if not (vmove<0):
            #determine front move
            if (piececolumn[vmove]!=self.banner):
                if piececolumn[vmove]==".":
                    goodactions.append(piece[0]+str(vmove))
            #determibne diag move
            origcol=ord(piece[0])
            if ((origcol-1)>=65):
                dcol=chr(origcol-1)
                dcolumn=self.board[dcol]
                if (dcolumn[vmove]!=self.banner):
                    goodactions.append(dcol+str(vmove))
            if ((origcol+1)<=(65+self.restofcollums)):
                dcol=chr(origcol+1)
                dcolumn=self.board[dcol]
                if (dcolumn[vmove]!=self.banner):
                    goodactions.append(dcol+str(vmove))        
        return goodactions


    def move_generator(self,boardstate):
        for piece in self.game_pieces:
            posactions=self.actions(piece)
            yield (piece,posactions)
            
    def tr(self, player,opponent):

        base=((len(player.game_pieces)) + random.random())
        piececolumn=self.board["A"] 
        rowlength=len(piececolumn)-1
        for piece in player.game_pieces:
            piece=list(piece)
            piecescore=-(rowlength-int(piece[1]))
            piecescore=piecescore/2
            if (len(player.game_pieces) > len(opponent.game_pieces)):
                piecescore-=10
        base=base+piecescore
        return base
    


        

            
class Player2:
    #min
    #top gee

    def __init__(self,banner,name):
        self.banner=banner
        self.game_pieces=[]
        self.name=name
        self.board=None
        self.restofcollums=0
        
    def gamepieces(self,pieces):
        self.game_pieces=pieces
    
    def table(self,board,game):
        if (self.board==None):
            self.board=board
            self.restofcollums=(len(game.keylist)-1)
        else:
            self.board=board
        
    def determinebest(self, actions):
        #bestheur=min(actions,key=lambda move:move[0])
        
        bestheur=min(actions)
        return bestheur
    def Conqueror(self,player,opponent):
        return(0 - len(opponent.game_pieces) + random.random())
        
        
    def Evasive(self,player,opponent):
        return(len(player.game_pieces) + random.random())
    
        
    def actions(self,piece):
        #have to create two player classes
        piece=list(piece)
        piececolumn=self.board[piece[0]]
        vmove=int(piece[1])+1 
        goodactions=[]
        rowlength=len(piececolumn)-1
        if not (vmove>rowlength):
            #determine front move
            if (piececolumn[vmove]!=self.banner):
                if piececolumn[vmove]==".":
                    goodactions.append(piece[0]+str(vmove))
            #determibne diag move
            origcol=ord(piece[0])
            if ((origcol-1)>=65):
                dcol=chr(origcol-1)
                dcolumn=self.board[dcol]
                if (dcolumn[vmove]!=self.banner):
                    goodactions.append(dcol+str(vmove))
            if ((origcol+1)<=(65+self.restofcollums)):
                dcol=chr(origcol+1)
                dcolumn=self.board[dcol]
                if (dcolumn[vmove]!=self.banner):
                    goodactions.append(dcol+str(vmove))        
        return goodactions


    def move_generator(self,boardstate):
        for piece in self.game_pieces:
            posactions=self.actions(piece)
            yield (piece,posactions)
            
    def tr(self, player,opponent):

        base=((len(player.game_pieces)) + random.random())
        piececolumn=self.board["A"] 
        rowlength=len(piececolumn)-1
        for piece in player.game_pieces:
            piece=list(piece)
            piecescore=-(rowlength-int(piece[1]))
            piecescore=piecescore/2
            if (len(player.game_pieces) > len(opponent.game_pieces)):
                piecescore-=10
        base=base+piecescore
        return base
    
    def rt(self,player,opponent):
        score=(len(player.game_pieces) + random.random())
        piececolumn=self.board["A"] 
        rowlength=len(piececolumn)-1
        for piece in player.game_pieces:
            piece=list(piece)
            if ((piece[1])==rowlength-1):
                score-=10 
        return score


class Node:
    #nxtpkeylist = next player keylist
    def __init__(self,state, piece, action,nxtpkeylist,oplist):
        self.action = action#action it takes to move to location 
        self.state=state
        self.piece = piece
        self.children=[]
        self.nextpkeylist=nxtpkeylist
        self.oplist=oplist
    
    
    



        
        
    

    
    
    
    
    
    
Red=Player1("X","Red")   
Blue=Player2("O","Blue")

    
A=Game(5,5,Red,Blue) 


A.play_game(Red.tr,Blue.rt,A.board)







    


# # 

# In[64]:




# In[ ]:




# In[ ]:




# In[ ]:



