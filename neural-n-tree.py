import random
import math

class NNTNode:
	
	def __init__(self, point):
		
		self.point = point
		self.index = -1
		self.right = None
		self.left = None
		self.is_terminal = False
		self.parent = None
		
		
class NNT:

	def __init__(self, min, max, dimensions, alpha = 0.01, size = 8):
		
		self.terminals = []
		self.root = None
		self.dimensions = dimensions
		self.min = min
		self.max = max
		self.alpha = alpha
		self.index = 0
		self.size = size * 2 - 1
		
		node_array = self.__random_array()
		
		self.__init_tree(node_array)
		
		self.__post_order(self.root)
		
	
	def similarity(self, codebook, feature):
		
		a = 0.0
		b = 0.0
		c = 0.0
        
		for i in range(self.dimensions):
			a += float(codebook[i]) * float(codebook[i])
			b += float(feature[i]) * float(feature[i])
			c += float(codebook[i]) * float(feature[i])
        	
		return (c / (math.sqrt(a) * math.sqrt(b)))
		
	
	def __random(self, min, max):
		
		return random.uniform(min, max)
		
	
	def __random_array(self):
		
		node_array = []
		
		for i in range(0, self.size):
			point_array = []
			for j in range(0, self.dimensions):
				point_array.append(self.__random(self.min, self.max))
			node_array.append(point_array)
		
		return node_array
		
	
	def __init_tree(self, point_array):
		
		return self.__init_tree_recursive(0, len(point_array) - 1, point_array)
		
	
	def __init_tree_recursive(self, min, max, point_array):
		
		if min > max:
			return None

		mid = int(round((min + max) / 2))
		node = NNTNode(point_array[mid])
		
		if self.root == None:
			self.root = node
			
		node.left = self.__init_tree_recursive(min, mid - 1, point_array)
			
		if node.left != None:
			node.left.parent = node
        		
		node.right = self.__init_tree_recursive(mid + 1, max, point_array)
        
		if node.right != None:
			node.right.parent = node
        	
		if node.right == None and node.left == None:
			node.is_terminal = True
        	
		return node
        
		
	def level_order(self, node):
	
		temporary = []
		tree = []
		nodes = []
		current = node
		level = 1
		
		temporary.append(current)
		tree.append([current])
		
		while len(temporary) > 0:
		
			if len(nodes) >= 2 ** level:
			
				tree.append(nodes)
				nodes = []
				level += 1	
			
			current = temporary.pop(0)
			
			if current != None:
			
				left = current.left
				right = current.right
				
				temporary.append(left)
				nodes.append(left)
				
				temporary.append(right)
				nodes.append(right)
				
			else:
			
				nodes.append(None)
				nodes.append(None)
				
		if len(nodes) > 0:
			tree.append(nodes)
			
		return tree
		
		
		
	def __post_order(self, node):
		
		if node != None:
		
			self.__post_order(node.left)
			self.__post_order(node.right)
			
			index = self.index
			node.index = index
			
			self.index += 1
			
			if node.is_terminal:
				self.terminals.append(node)
				
				
		
	def forward_train(self, arg):
		
		current = self.root
		
		self.__level_update(current, arg)
		
		while not current.is_terminal:
		
			if current.left != None and current.right != None:
			
				left = self.similarity(current.left.point, arg)
				right = self.similarity(current.right.point, arg)
				
				if left >= right:
				
					current = current.left
					
				else:
				
					current = current.right
					
				self.__level_update(current, arg)
					
			elif current.left != None and current.right == None:
			
				curret = current.left
			
			else:
				
				current = current.right
		
		
	def backward_train(self, arg):
		
		bmu = None

		for node in self.terminals:
			
			if bmu == None:
				bmu = node
		
			bmu_similarity = self.similarity(arg, bmu.point)
			node_similarity = self.similarity(arg, node.point)
		
			if bmu_similarity > node_similarity:
				bmu = node

		while bmu != None:
        	
			self.__level_update(bmu, arg)
			bmu = bmu.parent

        
                

		
	def cluster(self, arg):
		
		current = self.root
		
		while not current.is_terminal:
		
			if current.left != None and current.right != None:
			
				left = self.similarity(current.left.point, arg)
				right = self.similarity(current.right.point, arg)
				
				if left >= right:
				
					current = current.left
					
				else:
				
					current = current.right
					
			elif current.left != None and current.right == None:
			
				curret = current.left
			
			else:
				
				current = current.right
				
		return current.index
		
		
		
	def __level_update(self, node, arg):
	
		tree = self.level_order(node)
		levels = len(tree)
		
		
		for i in range(levels):
			for j in range(len(tree[i])):
				if tree[i][j] != None:
					for k in range(len(tree[i][j].point)):
						tree[i][j].point[k] = self.__update(tree[i][j].point[k], arg[k], (float((i + 1)) / (float(levels + 1))))
						
						
		
	def __update(self, point, arg, level):
		
		return point + self.alpha * (1 / level) * (arg - point)
		
