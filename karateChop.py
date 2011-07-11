#! /usr/bin/python

"""
 Kata Two - Karate Chop
 Binary Search that returns value's index positon or -1 if not found
 @author mmzyk
"""

"""
 Ways to implement:
	Iterative
	Recursive
	Threading
	Functional
	Continuations	
	Binary Search Tree - does this count?
	Others?
"""

import unittest
from threading import Thread

class kataSearch:

	index = None

	def run(self, method, needle, haystack):
		func = getattr(self, method)
		result = func(needle, haystack)
		print method , ' needle:', needle, ' haystack:', haystack, ' result: ', result
		return result
		
	def recursiveSearch(self, needle, haystack):
		length = len(haystack)
		
		if self.index == None:
			self.index = length - 1
		
		if length > 1:
			head = haystack[0:length/2]
			tail = haystack[length/2:]
			
			if head[len(head)-1] >= needle:
				self.index = self.index - len(tail)
				return self.recursiveSearch(needle, head)
			else:
				return self.recursiveSearch(needle, tail)
		elif length != 0:
			if haystack[0] == needle:
				return self.index
			else:
				return -1
		else:
			return -1				

	def iterativeSearch(self, needle, haystack):
		"""
		 In passing array slices around, I've done this in a more functional manner, as opposed
		 to the traditional binary search implemtation
		"""
		
		length = len(haystack)
		self.index = length - 1
		
		while True:
			
			if length == 1:
				if haystack[0] == needle:
					return self.index
				else:
					return -1	
			elif length != 0:
				head = haystack[0:length/2]
				tail = haystack[length/2:]
				
				if head[len(head)-1] >= needle:
					self.index = self.index - len(tail)
					haystack = head
				else:
					haystack = tail
			else:
				return -1
				
			length = len(haystack)	


	def threadedSearch(self, needle, haystack):

		global location

		location = len(haystack) - 1
		
		def search(needle, haystack):
			
			global location
			
			if len(haystack) > 1:
							
				head = haystack[0:len(haystack)/2]
				tail = haystack[len(haystack)/2:]

				if head[len(head)-1] >= needle:
					location = location - len(tail)
					slave = Thread(target=search, args=(needle, head))
					slave.start()
					slave.join()
				else:
					slave = Thread(target=search, args=(needle, tail))
					slave.start()
					slave.join()
			elif len(haystack) != 0:
				if haystack[0] != needle:
					location = -1
			else:
				location = -1

		
		worker = Thread(target=search, args=(needle, haystack))
		worker.start()
		worker.join()
		
		return location
		
	def traditionalSearch(self, needle, haystack):
		"""
		 The traditional binary search algorithm, using low and high markers.  I used 
		 Tim Bray's On the Goodness of Binary Search as the reference implementation for this method
		"""	
		high, low, probe = len(haystack), -1, None
		
		while (high - low > 1):
			probe = (low + high) / 2
			if haystack[probe] > needle:
				high = probe
			else:
				low = probe
				
		if low == -1 or haystack[low] != needle:
			return -1
		else:
			return low				
			
	
	def treeSearch(self, needle, haystack):
		"""
		 Build a binary search tree, storing the value and index as data.  
		 Search the tree. Upon finding the matching node return that node's index,
		 or -1 if not found
		"""
		tree = BinaryTree()
		root = None
		bale = list(haystack)
		
		if len(haystack) > 0:
			for straw in haystack:
				value = bale.pop()
				index = len(bale)
				root = tree.insert(root, { 'value':value, 'index':index })
		
		return tree.lookup(root, needle)
		

class node:
	
	data = left = right = None;
	
	def __init__(self, data, left, right):
		self.data = data
		self.left = left
		self.right = right
		
class BinaryTree:
	
	def lookup(self, node, target):
		if node == None:
			return -1
		else:
			if node.data['value'] == target:
				return node.data['index']
			else:
				if target < node.data:
					return self.lookup(node.left, target)
				else:
					return self.lookup(node.right, target)		
		
	def insert(self, node, data):
		if node == None:
			node = self.createNode(data)
		else:
			if data <= node.data:
				node.left = self.insert(node.left, data)
			else:
				node.right = self.insert(node.right, data)
				
		return node;			 	
		
	def createNode(self, data):
		return node(data, None, None)				
			
class kataTests(unittest.TestCase):
		
	methodList = ['recursiveSearch', 'iterativeSearch', 'threadedSearch', 'traditionalSearch', 'treeSearch']

	def call(self, method, needle, haystack):
		return kataSearch().run(method, needle, haystack)
	
	def testRun(self):
		
		for item in self.methodList:
			self.assertEqual(-1, self.call(item, 3, []))
			self.assertEqual(-1, self.call(item, 3, [1]))
			self.assertEqual(0,  self.call(item, 1, [1]))
			#
			self.assertEqual(0,  self.call(item, 1, [1, 3, 5]))
			self.assertEqual(1,  self.call(item, 3, [1, 3, 5]))
			self.assertEqual(2,  self.call(item, 5, [1, 3, 5]))
			self.assertEqual(-1, self.call(item, 0, [1, 3, 5]))
			self.assertEqual(-1, self.call(item, 2, [1, 3, 5]))
			self.assertEqual(-1, self.call(item, 4, [1, 3, 5]))
			self.assertEqual(-1, self.call(item, 6, [1, 3, 5]))
			#
			self.assertEqual(0,  self.call(item, 1, [1, 3, 5, 7]))
			self.assertEqual(1,  self.call(item, 3, [1, 3, 5, 7]))
			self.assertEqual(2,  self.call(item, 5, [1, 3, 5, 7]))
			self.assertEqual(3,  self.call(item, 7, [1, 3, 5, 7]))
			self.assertEqual(-1, self.call(item, 0, [1, 3, 5, 7]))
			self.assertEqual(-1, self.call(item, 2, [1, 3, 5, 7]))
			self.assertEqual(-1, self.call(item, 4, [1, 3, 5, 7]))
			self.assertEqual(-1, self.call(item, 6, [1, 3, 5, 7]))
			self.assertEqual(-1, self.call(item, 8, [1, 3, 5, 7]))
		
			
if __name__ == '__main__':
		unittest.main()

	