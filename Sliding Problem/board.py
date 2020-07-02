##
# contains the Board class
# board.py
#

from tile import Tile
from node import Node
from node import Node_Network
from graph import Graph

class Board():
    def __init__(self, r,c=None):
        '''Takes two intergers c and r
        c for columns, r for rows
        if c not defined c = r for a square
        creates the board with r rows and c columns
        each tile is a switch set to off '''
        if c is None:
            c = r
        self.r = r
        self.c = c
        self.board = []
        for cn in range(c):# I would like to make this have a border of 0. That would help with other code
            self.board.append([])
            for rn in range(r):
                self.board[cn].append(Tile(tile_type = 'Switch'))
                

    def add_block(self,x=None,y=None,list_input = None):
        '''changes a switch with a block at x,y'''
        if x != None and y != None:
            self.board[y][x].change_type()
        elif list_input != None:
            for col in range(len(self.board)):
                for row in range(len(self.board[col])):
                    if list_input[col*self.r + row] == 1:
                        self.board[col][row].change_type()
                    

    def nodeify(self): 
        '''Returns a board that only contains the points in which the player can make a turn
        and the conecting places where they can make a turn
        each node will have a position and linking nodes'''


        # Identify all nodes 
        # Link nodes

        self.nn = Node_Network()
        for col in range(len(self.board)):
            for row in range(len(self.board[col])):

                # Check that is a switch
                if self.board[col][row].is_open():

                    # CHECK IF IT IS A NODE:

                    # all this checking can be made 4 methods... maybe

                    noder,nodel,nodeu,noded,nodew = False,False,False,False,False
                    try:
                        if self.board[col+1][row].is_block():
                            noder = True
                    except:
                        nodew = True

                    if col > 0:
                        if self.board[col-1][row].is_block():
                            nodel = True
                    else:
                        nodew = True
                            
                    try:
                        if self.board[col][row+1].is_block():
                            noded = True
                    except:
                        nodew = True

                    if row > 0:    
                        if self.board[col][row-1].is_block():
                            nodeu = True
                    else:
                        nodew = True

                        
                    if nodeu or noded or noder or nodel or nodew:
                        self.nn.add_node((row, col))


        self.nn.link_nodes(self.board)


    def check_linkage(self):
        '''Checks that from any given node you can reach any other given node'''
        g = Graph(self.nn.number_of_nodes())

        for i in range(self.nn.number_of_nodes()):
            for j in range(len(self.nn.nodes[i].links)):
                g.add_edge(i, self.nn.nodes[i].links[j].node_number)

        try:    
            g.find_paths(0,1)
        except:
            return []
        visits1 = g.get_visits() 

        return visits1 


    def switch_the_switches(self, on_nodes):
        '''Move along every nodes path on the board switching every switch'''
        for node in range(len(on_nodes)): #passed in
            if on_nodes[node]:
                to_switch_from = self.nn.poses[node]
                to_switch_to_l = self.nn.nodes[node].links
                self.board[to_switch_from[1]][to_switch_from[0]].touched()
                for link in to_switch_to_l:
                    for x in range(link.pos[0], len(self.board)):  
                        if self.board[link.pos[1]][x].is_open():                                     
                            self.board[link.pos[1]][x].touched()
                        else:
                            break
                    
                    for x in range(link.pos[0], -1,-1):
                        if self.board[link.pos[1]][x].is_open():
                            self.board[link.pos[1]][x].touched()
                        else:
                            break
                        
                    for y in range(link.pos[1], len(self.board)):
                        if self.board[y][link.pos[0]].is_open():
                            self.board[y][link.pos[0]].touched()
                        else:
                            break
                    
                    for y in range(link.pos[1], -1,-1):
                        if self.board[y][link.pos[0]].is_open():
                            self.board[y][link.pos[0]].touched()
                        else:
                            break

              
    def is_possible(self):
        '''If the board only consists of on switchs and blocks return True'''
        possible = True
        for col in range(self.c):
            for row in range(self.r):
                if self.board[col][row].is_switch():
                    if self.board[col][row].is_off():
                        possible = False
                        break
                    
        return possible


if __name__ == '__main__':
    b = Board(2)
##    b.add_block(0,1) 
##    b.add_block(1,0)
##    b.add_block(1,1)
    b.add_block(None, None, [1,0,0,1])
    
    b.nodeify()
    p = b.check_linkage()
    b.switch_the_switches(p)
    print(b.is_possible())
    
        
        
        

