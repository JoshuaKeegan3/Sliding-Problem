##
# contains the Node Class for nodeifying the board
# contains the Node_Network Class for containing these nodes
# node.py
# 

def rotated(board):# lol I never used this. I kept it here because I love this code
        list_of_tuples = zip(*board[::-1])
        return [list(elem) for elem in list_of_tuples]

class Node():
        def __init__(self, pos, node_number):
                self.links = []
                self.pos = pos
                self.node_number = node_number

        def add_link(self, node):
                self.links.append(node)


class Node_Network():
        def __init__(self):
                self.nodes = []
                self.poses = []

        def add_node(self, pos):
                n = Node(pos, len(self.nodes))
                self.poses.append(n.pos)
                self.nodes.append(n)

        def intersept(self,board, node1,node2):
                if node1.pos[0] < node2.pos[0]:
                        for i in range(node1.pos[0], node2.pos[0]+1):
                                if board[node1.pos[1]][i].is_block():
                                        return True
                elif node1.pos[1] < node2.pos[1]:
                        for i in range(node1.pos[1], node2.pos[1]+1):
                                if board[i][node1.pos[0]].is_block():
                                        return True
                elif node1.pos[0] > node2.pos[0]:
                        for i in range(node1.pos[0], node2.pos[0], -1):
                                if board[node1.pos[1]][i].is_block():
                                        return True
                elif node1.pos[1] > node2.pos[1]:
                        for i in range(node1.pos[1], node2.pos[1],-1):
                                if board[i][node1.pos[0]].is_block():
                                        return True
                return False
        def stops(self,node1, node2,board):
                if node2.pos[0] > node1.pos[0]:
                        if node2.pos[0] == len(board)-1:
                                return True
                        if board[node2.pos[1]][node2.pos[0]+1].is_block():
                                return True
                elif node2.pos[0] < node1.pos[0]:
                        if node2.pos[0] == 0:
                                return True
                        if board[node2.pos[1]][node2.pos[0]-1].is_block():
                                return True

                elif node2.pos[1] > node1.pos[1]:
                        if node2.pos[1] == len(board)-1:
                                return True
                        if board[node2.pos[1]+1][node2.pos[0]].is_block():
                                return True

                elif node2.pos[1] < node1.pos[1]:
                        if node2.pos[1] == 0:
                                return True
                        if board[node2.pos[1]-1][node2.pos[0]].is_block():
                                return True

                return False


        def link_nodes(self, board):
                global b
                b = board
                for node1 in self.nodes:
                        for node2 in self.nodes:
                                if node1 != node2:
                                        if (node1.pos[1] == node2.pos[1]) != (node1.pos[0] == node2.pos[0]):  #XOR gate
                                                
                                                if not self.intersept(board,node1, node2) and self.stops(node1,node2,board):
                                                        node1.add_link(node2)
                              
        def number_of_nodes(self):
                return len(self.nodes)




