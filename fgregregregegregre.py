
import numpy as np
import sympy
'''

Todo:

Parse user input to list of numbers
Solve system of equations
Print out solution to SOE


Chemical equation for photosynthesis is for example (as input):

C1.O2+H2.O1->C6.H12.O6+O2     aka elements are prefixes and multipliers are aforementioned integers and
"->" signifies chemical reaction from reactants to products.

C1.H4+O2->C1.O2+H2.O


Na3.P1.O4+Ca1.Cl2->Ca3.P2.O8+Na1.Cl1

C2.H6.O1+O2->C1.O2+H2.O1



'''
def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


def express(a, b, name, expr=None):
	sym = sympy.symbols(name)
	if expr:
		sym = expr
	print("New cycle")
	print(a)
	print(sym)
	sol = sympy.solve(a-sym, b)
	print(sol)
	assert len(sol) == 1
	return (sym, sol[0])

def parse_formula(chemical_formula: str):
	reactants = chemical_formula[:chemical_formula.find("->")]
	products = chemical_formula[chemical_formula.find("->")+2:]

	print(reactants)
	print(products)
	print("ifoerfewgewgewgwe")
	reactants = reactants.split("+")
	products = products.split("+")
	print(reactants)
	print(products)
	substances = reactants+products
	substances = list(dict.fromkeys(substances))




	'''
	for every reactant in reactants:
		append column to matrix.
	for every product in products:
		append column*-1 to matrix
	append zero column


	matrix is shape (len(reactants)+len(products)+1,len(elements))




	'''
	# get all distinct elements from equation

	elements_r = []

	for reactant in reactants:
		for elem in reactant.split("."):
			#elements_r.append(elem)
			result = ''.join([i for i in elem if not i.isdigit()])
			elements_r.append(result)
	print(elements_r)
	for oof in products:
		for elem in oof.split("."):
			#elements_r.append(elem)
			print("Element:")
			print(elem)
			result = ''.join([i for i in elem if not i.isdigit()])
			elements_r.append(result)
	elements_r = set(elements_r)
	print(elements_r)
	# next append a row for every element found in chemical equation 
	matrixthing = []
	oofpaska = []
	for element in elements_r:
		ooflist = []
		for substance in reactants:
			print(substance)
			if element in substance:
				elementstuff = substance.split(".")
				for element2 in elementstuff:
					if element in element2:
						ooflist.append(int(element2[element2.find(element)+len(element):]))
			else:
				ooflist.append(0)
		#oofpaska.append(ooflist[0])
		#ooflist.pop(0)
		for substance in products:
			print(substance)
			print("ooofff")
			if element in substance:
				elementstuff = substance.split(".")
				for element2 in elementstuff:
					if element in element2:
						ooflist.append(int(element2[element2.find(element)+len(element):])*-1)
			else:
				ooflist.append(0)
		#oofpaska.append(ooflist[0])
		#ooflist.pop(0)
		print(ooflist)
		matrixthing.append(ooflist)
	'''
	#matrixthing.append([0,0,0,1])
	A = np.array(matrixthing)
	#print(A.shape)
	#inv_A = np.linalg.inv(A)
	B = np.array([0]*A.shape[0])
	#print("B: "+str(B))
	#X = np.linalg.inv(A).dot(B)
	#print(X)
	print(A)
	print(np.linalg.solve(A,B))
	#print(oofpaska)
	'''

	elementmatrix = sympy.Matrix(matrixthing)
	print("Nullspace:")
	print(elementmatrix.nullspace())
	solutions = []
	for solution in elementmatrix.nullspace():
		solutions.append(solution)

	#solution = elementmatrix.nullspace()[0]
	#solution2 =elementmatrix.nullspace()[1]
	print("Dot product: ")

	#oof = sympy.lcm([val.q for val in solution])
	#oof2 = sympy.lcm([val.q for val in solution2])

	oofs = []
	for oof in range(len(solutions)):
		oofs.append(sympy.lcm([val.q for val in solutions[oof]]))

	print(matrixthing)
	print("Solution: ")
	#solution, solution2 = solution.tolist(), solution2.tolist()
	for i in range(len(solutions)):
		solutions[i] = solutions[i].tolist()
		solutions[i] = flatten(solutions[i])

	#solution = flatten(solution)
	#solution2 = flatten(solution2)
	'''
	integer1 = 1
	if not all(isinstance(x, int) for x in solution):
		#solution*= integer1
		solution = [x*integer1 for x in solution]
		integer1 += 1
	integer1 = 1
	if not all(isinstance(x, int) for x in solution2):
		#solution2*= integer1
		solution2 = [x*integer1 for x in solution2]
		integer1 += 1
	'''
	#print(solution)
	#print(solution2)
	print([val for val in solution])
	print([val for val in solution])
	print(np.dot(np.array(matrixthing), np.array([val for val in solution])))
	count = 0
	vectors = []
	print("Partial solutions: ")
	for solution in solutions:
		vectors.append([x*oofs[count] for x in solution])
		print([x*oofs[count] for x in solution])
		count += 1
	vectorsum = len(vectors[0])*[0]
	for vector in vectors:
		vectorsum = [vectorsum[i]+vector[i] for i in range(len(vector))]
	print("Sum solution: ")
	print(vectorsum)
	#solution = solution*oof
	#solution2 = [x*oof2 for x in solution2]
	#print(solution)
	#print(solution2)
	return (substances, vectorsum, len(reactants))




def balanceformula():
	substanceslist = []
	solutions = []
	oofs = []
	while True:
		substances, solution, oof = parse_formula(input("Give chemical formula: "))
		substanceslist.append(substances)
		solutions.append(solution)
		oofs.append(oof)
		print(substances)
		print(solutions)
		print(oofs)
		if input("Do you want to give another formula ? (y/N): ") != 'y':
			break
	#print(substanceslist)
	all_substances = flatten(substanceslist)
	print(all_substances)
	all_substances = list(dict.fromkeys(all_substances))
	equations = []
	print(oofs)
	
	
	for i in range(len(solutions)):
		equation = [0]*(len(all_substances)+1)
		for k in range(len(substanceslist[i])):
			index = all_substances.index(substanceslist[i][k])
			if k < oofs[i]:

				value = solutions[i][k]
			else:
				value = -1*solutions[i][k]

			equation[index] = value
		equations.append(equation)
	print(equations)
	alphabet = "abcdefghijklmnopqrstuvxyz"
	#variablestring = ""
	#for i in range(len(all_substances)):
	#	variablestring += alphabet[i]+", "
	#	print(variablestring)

	variables = []
	for i in range(len(all_substances)):
		variables.append(sympy.Symbol(alphabet[i]))
	print(variables)
	print(tuple(equations))
	print(tuple(variables))
	final_solutions = sympy.linsolve(sympy.Matrix(tuple(equations)),tuple(variables))

	unknown = str(input("Mikä aine halutaan?: "))
	unknown_var = variables[all_substances.index(unknown)]
	print(final_solutions)
	print(all_substances)
	unknown_var = final_solutions.args[0][all_substances.index(unknown)]
	print("!!!!!!!!!!!!!!!!!!!!\n\n\n")
	#print(final_solutions.args[0][0])
	print(unknown_var)
	print("\n\n")
	
	known_values = str(input("Mikä aine tiedetään?: "))
	print(str(known_values))
	


	lll = variables[all_substances.index(known_values)]
	#print(type(lll))
	#print(lll)
	print(unknown_var)
	print(str(unknown_var))
	print(variables[all_substances.index(known_values)])
	print("ooofffff")
	print(sympy.solve(variables[all_substances.index(known_values)], unknown_var))
	#_, unkown_var_as_expr_in_other_vars = express(str(unknown_var), variables[all_substances.index(known_values)], str(unknown_var))
	#_, unkown_var_as_expr_in_other_vars = express(variables[all_substances.index(known_values)], str(unknown_var), variables[all_substances.index(known_values)])
	_, unkown_var_as_expr_in_other_vars = express(variables[all_substances.index(known_values)], str(unknown_var), 'aaa', expr=unknown_var)

	print(unkown_var_as_expr_in_other_vars)


	

if __name__ == "__main__":
	balanceformula()

'''

[[ 3  0  0 -1],[ 1  0 -2  0],[ 0  1 -3  0],[ 0  2  0 -1],[ 4  0 -8  0]]


'''



'''

2 H2 + O2 --> 2 H2O


2a + b = 2c

c + d = e




'''




