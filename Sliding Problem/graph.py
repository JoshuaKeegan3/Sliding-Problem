##
# Python program to print all paths from a source to destination. 
# graph.py
#
from collections import defaultdict 



class Graph(): 

        def __init__(self,vertices): 
                #No. of vertices 
                self.V= vertices 
                	
                # default dictionary to store graph 
                self.graph = defaultdict(list) 
                self.paths = []
                self.all_vists = []


	# function to add an edge to graph 
        def add_edge(self,u,v): 
                self.graph[u].append(v)
                
        '''A recursive function to print all paths from 'u' to 'd'. 
        visited[] keeps track of vertices in current path. 
        path[] stores actual vertices and path_index is current 
        index in path[]'''
        def recursive_path_finder(self, u, d, visited, path): 

		# Mark the current node as visited and store in path 
                visited[u]= True
                self.all_vists[u]= True
                path.append(u) 

		# If current vertex is same as destination, then print 
		# current path[]
                if u == d:
                        self.paths.append(path) # This should be more general
                                                # Because sometimes no worky
                else: 
			# If current vertex is not destination 
			#Recur for all the vertices adjacent to this vertex 
                        for i in self.graph[u]: 
                                if visited[i]==False: 
                                        self.recursive_path_finder(i, d, visited, path) 
					
		# Remove current vertex from path[] and mark it as unvisited
                path.pop() 
                visited[u]= False

        def find_paths(self,s, d):

		# Mark all the vertices as not visited 
                visited =[False]*(self.V)
                self.all_vists = [False]*(self.V)

		# Create an array to store paths 
                path = [] 

		# Call the recursive function to get all paths 
                self.recursive_path_finder(s, d,visited, path)
                
        def get_visits(self):
                return self.all_vists


if __name__ == '__main__':
	# Create a graph given in the above diagram 
	g = Graph(6) 	#This is how many nodes
	g.add_edge(0, 1) 	# This is the links.
	g.add_edge(0, 2) 
	g.add_edge(0, 3) 
	g.add_edge(2, 0) 
	g.add_edge(2, 1) 
	g.add_edge(1, 3) 

