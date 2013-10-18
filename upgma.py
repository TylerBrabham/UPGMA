#Tyler Brabham
#CS 176 Fall 2013

import numpy as np

'''
Function takes in a dissimilarity map as an numpy array/matrix.
Uses upgma to produce the phylogenetic tree corresponding to the
dissimilarity map.

Return value will be a string representing a graph, using nested
parantheses to denote level.
'''
def upgma(dis_map):
	upgma_tree = ''
	C = [1 for i in range(dis_map.shape[0])]

	current_map = dis_map
	(m,n) = current_map.shape
	while n>2:
		#find the closest pairs
		min_dist = float('inf')
		min_i = 0
		min_j = 0
		for i in range(n):
			for j in range(n):
				dist = current_map[i,j]
				if dist<min_dist:
					min_dist = dist
					min_i = i
					min_j = j

		new_map = np.arange((n-1)*(n-1)).reshape(n-1,n-1)
		(m,n) = (m-1,n-1)

		#create a new count variable for the cluster sizes
		new_C = [1 for i in range(n)]
		new_C[0] = C[min_i]+C[min_j]
		j = 1
		for l in range(1,n):
			if l==min_i or l==min_j:
				pass
			else:
				new_C[j] = C[l]
				j += 1
		print new_C

		#update the dis map by removing min_i,min_j and adding new letter k in the 
		#first position
		i = 1
		for k in range(n):
			j = 1
			if k==min_i:
				pass
			else:
				for l in range(n):
					if l==min_j:
						pass
					else:
						new_map[i,j] = current_map[i,j]
						j += 1
				i += 1

		for l in range(n):
			new_map[0,l] = float(current_map[min_i,l]*C[min_i] + current_map[min_j,l]*C[min_j])/float(C[min_i]+C[min_j])
			new_map[l,0] = new_map[0,l]#symmetric


		C = new_C
		current_map = new_map
		print current_map


	return upgma_tree


dis_map = np.matrix('0 1 1; 1 0 1; 1 1 0')

upgma(dis_map)