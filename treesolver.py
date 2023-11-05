
# This is a small library to find the ratio between the substance which we want to know and the starting substance. It is implemented as a tree with the known substance as the root and the wanted substance as the destination.


class Elemnode:
	def __init__(self, substance, coefficient):
		self.coefficient = coefficient
		self.substance = substance
		self.next_substances = []
		self.previous_substances = []
		self.visited = False # This is used to prevent going into an infinite loop when traversing the tree when there is a circular path.


class Elemtree:
	def __init__(self, stuff):

		# stuff is basically shitoof in the original script.

		# [[[1, 6, 6, 6], (['C6.H12.O6', 'O2'], ['C1.O2', 'H2.O1'])], [[1, 4, 1, 2], (['C1.O2', 'H2'], ['C1.H4', 'H2.O1'])]]

		self.substances = [] # a list of the nodes of the graph.

		self.stuff = stuff

		self.nodes = []

	def construct_tree(self):

		# Loop over all of the chemical equations and add the nodes as we go.

		for equation_stuff in self.stuff:
			print(equation_stuff)
			# Now equation_stuff is of the format [<equation_coefficients> [<elements_left_side>, <elements_right_side>]]
			coeffs = equation_stuff[0]

			# First construct the nodes (the edges aka. "connections" will be added later on)

			rhs_nodes = []
			lhs_nodes = []

			rhs_substances = equation_stuff[1][1]
			rhs_coefficients = coeffs[len(equation_stuff[1][0]):]
			lhs_substances = equation_stuff[1][0]
			for i, subst in enumerate(rhs_substances):


				for subst_node in self.nodes:
					# This is to check if the substance already is in the tree, so we do not add two nodes with the same substance.
					if subst_node.substance == subst:
						rhs_nodes.append(subst_node)
						continue

				new_node = Elemnode(subst, rhs_coefficients[i])



				self.nodes.append(new_node)

				rhs_nodes.append(new_node)


			lhs_substances = equation_stuff[1][0]
			lhs_coefficients = coeffs[:len(lhs_substances)]

			for i, subst in enumerate(lhs_substances):
				for subst_node in self.nodes:
					# This is to check if the substance already is in the tree, so we do not add two nodes with the same substance.
					if subst_node.substance == subst:
						lhs_nodes.append(subst_node)
						continue
				new_node = Elemnode(subst, lhs_coefficients[i])



				self.nodes.append(new_node)

				lhs_nodes.append(new_node)




			# Now set the connections (edges)

			for lhs_node in lhs_nodes: # If we want to go backwards
				for rhs_node in rhs_nodes:
					rhs_node.previous_substances.append(lhs_node) # set the previous thing

			for rhs_node in rhs_nodes: # If we want to go forwards
				for lhs_node in lhs_nodes:
					lhs_node.next_substances.append(rhs_node)

		return

	def traverse_tree(self, begin_substance, end_substance):
		
		# This get's the route from begin_substance to end_substance.

		for node in self.nodes:
			if node.substance == begin_substance:
				return self.traverse_node(node, node, end_substance)


	def traverse_node(self, node, begin_node, end_substance):
		print("node.substance == "+str(node.substance))
		if node.substance == end_substance:
			return [node]

		if node.next_substances == []:
			return None

		for child_node in node.next_substances:

			if self.traverse_node(child_node, begin_node, end_substance) != None:
				return [node]+self.traverse_node(child_node, begin_node, end_substance)

		return None


if __name__=="__main__":

	# Test suite.

	stuff = [[[1, 6, 6, 6], (['C6.H12.O6', 'O2'], ['C1.O2', 'H2.O1'])], [[1, 4, 1, 2], (['C1.O2', 'H2'], ['C1.H4', 'H2.O1'])]] # this is the oofshit when running with "sample_system_of_equations.txt" file.

	tree = Elemtree(stuff)

	tree.construct_tree()

	print("Tree: "+str(tree))

	route = tree.traverse_tree('C6.H12.O6', 'C1.H4')
	print("Route: "+str(route))
	print("Elements: "+str([x.substance for x in route]))
	exit(0)


