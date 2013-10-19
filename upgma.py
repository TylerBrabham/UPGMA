#Tyler Brabham
#CS 176 Fall 2013

import numpy as np

'''
Function takes in a dissimilarity map as an numpy array/matrix.
Uses upgma to produce the phylogenetic tree corresponding to the
dissimilarity map.
'''
def upgma(dis_map):
	current_map = dis_map
	(m,n) = current_map.shape

	#represents the leaves. (node,child1,child2,height). -1 indicates no child
	upgma_tree = [(i,-1,-1,0) for i in range(n)]

	#Count value for each cluster (number of nodes in cluster)
	C = [1 for i in range(n)]
	cluster_count = n

	#Table for going between matrix index and cluster index
	cluster = {}
	for i in range(n):
		cluster[i] = i

	while n>2:
		#find the closest pairs
		min_dist = float('inf')
		min_i = 0
		min_j = 0
		for i in range(n):
			for j in [k for k in range(n) if i!=k]:
				dist = current_map[i,j]
				if dist<min_dist:
					min_dist = dist
					min_i = i
					min_j = j

		#Make a new matrix which combines clusters min_i and min_j
		new_map = np.arange((n-1)*(n-1)).reshape(n-1,n-1)

		#create a new count variable for the updated cluster sizes (after combining min clusters)
		new_C = [1 for i in range(n-1)]
		new_C[0] = C[min_i]+C[min_j]
		j = 1
		for l in range(1,n):
			if l==min_i or l==min_j:
				pass
			else:
				new_C[j] = C[l]
				j += 1

		#add the new cluster to the output leave list, with appropriate height
		upgma_tree.append((cluster_count,cluster[min_i],cluster[min_j],float(min_dist)/2.0))

		#shift the rest of the clusters over by 1 to make room for new cluster at front
		new_cluster = {}
		new_cluster[0] = cluster_count
		cluster_count += 1
		k = 1
		for i in range(1,len(cluster)):
			if i!=min_j and i!=min_i:
				new_cluster[k] = cluster[i]
				k+=1

		#update the dis map by removing min_i,min_j and adding new cluster to the matrix at index 0
		i = 1
		for k in range(n):
			j = 1
			if k==min_i or k==min_j:
				pass
			else:
				for l in range(n):
					if l==min_j or l==min_i:
						pass
					else:
						new_map[i,j] = current_map[k,l]
						j += 1
				i += 1

		l = 1
		for k in range(n):
			if k!= min_i and k!=min_j:
				new_map[0,l] = float(current_map[min_i,k]*C[min_i] + current_map[min_j,k]*C[min_j])/float(C[min_i]+C[min_j])
				new_map[l,0] = new_map[0,l]#symmetric
				l += 1

		#reset all the tables 
		C = new_C
		current_map = new_map
		cluster = new_cluster
		(m,n) = (m-1,n-1)

	#Now there are two remaining indices. We combine them and add them to the out list.
	print current_map
	upgma_tree.append((cluster_count, cluster[0], cluster[1], float(current_map[0,1])/2.0))

	return upgma_tree


dis_map = np.matrix('0 5 2; 5 0 1; 2 1 0')

upgma_tree = upgma(dis_map)
print upgma_tree