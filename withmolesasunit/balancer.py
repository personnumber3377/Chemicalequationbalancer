
import numpy as np
import sympy
import copy
import re
import dataloader










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

def removeintegers(string):
	return ''.join([i for i in string if not i.isdigit()])

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

	
	reactants = reactants.split("+")
	products = products.split("+")
	
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
	
	for oof in products:
		for elem in oof.split("."):
			#elements_r.append(elem)
			
			result = ''.join([i for i in elem if not i.isdigit()])
			elements_r.append(result)
	elements_r = set(elements_r)
	
	# next append a row for every element found in chemical equation 
	matrixthing = []
	oofpaska = []
	for element in elements_r:
		ooflist = []
		for substance in reactants:
			
			#paska = substance.split(".")
			#for i in range(len(paska)):
			#	paska[i] = ''.join([k for k in paska[i] if not k.isdigit()])
			
			if element in substance:
				elementstuff = substance.split(".")
				thing = False
				count = 0
				for element2 in elementstuff:
					

					if removeintegers(element) == removeintegers(element2):
						print("Check")
						print(element2)
						print(element)
						print(int(element2[element2.find(element)+len(element):]))
						print("Count: ")
						print(count)
						print(substance)
						ooflist.append(int(element2[element2.find(element)+len(element):]))
						thing = True
						
				if not thing:
					ooflist.append(0)
			else:
				ooflist.append(0)
		#oofpaska.append(ooflist[0])
		#ooflist.pop(0)
		for substance in products:
			
			if element in substance:
				elementstuff = substance.split(".")
				thing = False
				for element2 in elementstuff:
					
					if removeintegers(element) == removeintegers(element2):
						print("Check")
						print(element2)
						print(element)
						print(int(element2[element2.find(element)+len(element):])*-1)
						ooflist.append(int(element2[element2.find(element)+len(element):])*-1)
						thing = True
						
				if not thing:
					ooflist.append(0)
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

	
	print("Dot product: ")
	print(elements_r)

	#oof = sympy.lcm([val.q for val in solution])
	#oof2 = sympy.lcm([val.q for val in solution2])

	oofs = []
	for oof in range(len(solutions)):
		oofs.append(sympy.lcm([val.q for val in solutions[oof]]))

	print(matrixthing)
	print("Solution: ")
	
	for i in range(len(solutions)):
		solutions[i] = solutions[i].tolist()
		solutions[i] = flatten(solutions[i])

	
	
	print("Kinda oofthingyoof")
	#print([val for val in solution])
	#print([val for val in solution])
	#print(np.dot(np.array(matrixthing), np.array([val for val in solution])))
	count = 0
	vectors = []
	print("Partial solutions: ")
	print(solutions)
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
	return (substances, vectorsum, len(reactants), (reactants, products))


'''

def find_limiting_factor(number_of_moles, all_substances, known_values, final_solutions, solutions, substanceslist, variables):
	# return the substance which is the limiting factor in the reaction:

	eliminated = []
	for i in range(len(known_values)):
		print("ooooooooofffffffffffffffffffffff")
		known_value = known_values[i]
		# eliminate all other possibilities until the limiting_factor remains

		for k in range(len(known_values)):
			known_value2 = known_values[k]
			# get number of moles of known_value and then check if said value is more than or equal to the moles of known_value2*ratioconstant
			right_index = all_substances.index(known_value2)

			moles_of_known_value2_needed = final_solutions.args[0][right_index]
			anotherindex = all_substances.index(known_value)
			#replacement = [(variables[anotherindex], number_of_moles[i])]
			#replacement = [(variables[anotherindex], number_of_moles[i])]

			replacements = []
			for j in range(len(known_values)):
				#if j == k:
				#	continue # do not replace current value
				replacements.append(tuple((variables[j], number_of_moles[known_values.index(all_substances[j])])))
			print(replacements)
			moles_of_known_value2_needed = moles_of_known_value2_needed.subs(replacements)
			print(moles_of_known_value2_needed)
			print(solutions)
			
			#if moles_of_known_value2_needed

		
'''
'''
def getratio(substance1, substance2, oofshit, all_substances):
	print(oofshit)
	counter = 0

	# generate all possible equations from all the chemical equations:
	variables = []
	for i in range(len(all_substances)):
		variables.append(sympy.Symbol('n'+str(i)))
	print(variables)
	equationslist = []
	for oof in oofshit:
		for k in range(len(oof[0])):
			equationsubstances = flatten(list(oof[1]))
			firststring = str(oof[0][k])+'*'+str(variables[all_substances.index(equationsubstances[k])])          #coeff*variable
			for l in range(len(oof[0])):
				secondstring = str(oof[0][l])+'*'+str(variables[all_substances.index(equationsubstances[l])])
				equationslist.append(str(firststring+'='+secondstring))
				print("qqqqqq")
				print(sympy.sympify("Eq("+str(str(firststring+'='+secondstring)).replace("=",",")+")"))
				print(sympy.solve(sympy.sympify("Eq("+str(str(firststring+'='+secondstring)).replace("=",",")+")"),str(variables[all_substances.index(equationsubstances[l])])))
				print(variables[all_substances.index(equationsubstances[l])])
				print("\n\n")
				#eval(str(firststring+'='+secondstring))
	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	while True in equationslist:
		equationslist.remove(True)
	print("aaaaaaaaaaafffffffffffffff")
	print(equationslist)
	#print(sympy.solve(equationslist, variables[all_substances.index(substance1)]))
	print("Equation: ")
	#print("Eq("+str(equationslist[0])).replace("=",",")+")"
	print(sympy.sympify("Eq("+str(equationslist[0]).replace("=",",")+")"))
	print(sympy.solve(sympy.sympify("Eq("+str(equationslist[1]).replace("=",",")+")"), "n1"))
	complete_eqs = []

	for k in range(len(equationslist)):
		complete_eqs.append(sympy.sympify("Eq("+str(equationslist[k]).replace("=",",")+")"))
	print(complete_eqs)
	#print(sympy.solve(complete_eqs, "n1"))
	print(all_substances)
	#print(sympy.solve(complete_eqs, "n0"))
	solutions = sympy.solve(complete_eqs)
	print("Solutions:")
	print(solutions)
	#print([eq.subs("n0", sympy.solve(complete_eqs, "n0")) for eq in complete_eqs])
	#print(variables[0]/variables[1])
	exit()


'''





def getratio(substance1, substance2, oofshit, all_substances):
	'''
	oofshit: the solutions to the problem
	all_substances: a list of all the substances
	substance1: a substance
	substance2: a substance


	'''

	# to get the stoichiometric ratio between two compunds is to find the ratio between their coefficients in a chemical equation:
	print("Paskaaa:")
	print(all_substances)
	print(oofshit)

	print(oofshit[0])

	print(substance1)

	print(oofshit[0][0][all_substances.index(substance2)])
	print(oofshit[0][0][all_substances.index(substance1)])



	ratio = oofshit[0][0][all_substances.index(substance1)]/oofshit[0][0][all_substances.index(substance2)]
	return ratio




def find_limiting_factor(number_of_moles, all_substances, known_values, final_solutions, solutions, substanceslist, variables, equations, oofshit):
	# return the substance which is the limiting factor in the reaction:

	eliminated = []
	for i in range(len(known_values)):
		print("ooooooooofffffffffffffffffffffff")
		known_value = known_values[i]
		# eliminate all other possibilities until the limiting_factor remains
		paska = copy.deepcopy(known_values)
		paska.remove(known_value)
		for k in range(len(paska)):
			known_value2 = paska[k]
			ratio = getratio(known_value, known_value2, oofshit, all_substances)
			print("Ratio: ")
			print(ratio)

			# so that all of the known_value substance gets used we need to compare that times ratio to the other amount
			print("Number of moles")
			print(number_of_moles)
			print(known_value)
			if number_of_moles[known_values.index(known_value)]/ratio >= number_of_moles[known_values.index(known_value2)]:
				eliminated.append(known_value)
			if len(eliminated) == len(known_values)-1:
				returnvalue = copy.deepcopy(known_values)
				for elim in eliminated:
					returnvalue.remove(elim)
				return returnvalue[0]




def get_molar_mass(substance):
	# first seperate the substance to individual elements and coefficients:
	splits = substance.split(".")
	integers = "0123456789"
	total_molar_mass = 0
	elements, molar_masses = dataloader.load_data()
	for split in splits:
		index = 1
		while split[-index] in integers:
			index+=1
		integerpart = split[-index+1:]

		index = 0
		while split[index] not in integers:
			index+=1
		elementpart = split[:index]
		#print(split)
		#print("Integer part")
		#print(integerpart)
		#print("Element part")
		#print(elementpart)
		#print(molar_masses)
		#print(elements.index(elementpart))
		element_molar_mass = molar_masses[elements.index(elementpart)]
		#print(element_molar_mass)
		#print(integerpart)
		total_molar_mass += int(integerpart)*element_molar_mass
	return total_molar_mass







def convert_to_moles_one_substance(substance, number_of_grams):
	molar_mass = get_molar_mass(substance)
	return number_of_grams/molar_mass


def convert_to_moles(known_values, number_of_grams):
	return [convert_to_moles_one_substance(known_values[i], number_of_grams[i]) for i in range(len(number_of_grams))]

def convert_from_moles_one_substance(substance, number_of_moles):
	molar_mass = get_molar_mass(substance)
	return number_of_moles*molar_mass




def balanceformula():
	substanceslist = []
	solutions = []
	oofs = []
	oofshit = []
	while True:
		substances, solution, oof, things = parse_formula(input("Give chemical formula: "))
		substanceslist.append(substances)
		solutions.append(solution)
		oofs.append(oof)
		oofshit.append([solution, things])
		print(substances)
		print(solutions)
		print(oofs)
		if input("Do you want to give another formula ? (y/N): ") != 'y':
			break
	print("Oofshit: ")
	print(oofshit)
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
	print("zzzzzzzzzz")
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
	
	known_values = str(input("Mitkä aineet tiedetään?: ")).split(" ")
	print(str(known_values))
	print("Limiting factor:")

	# find the limiting factor:
	number_of_grams = str(input("Anna grammamäärät samassa järjestyksessä: ")).split(" ")
	#number_of_grams = [float(x) for x in number_of_grams]
	if 'm' in number_of_grams[0]:
		number_of_moles = []
		for thing in number_of_grams:
			number_of_moles.append(thing[:-1])
		number_of_moles = [float(x) for x in number_of_moles]
	else:
		number_of_grams = [float(x) for x in number_of_grams]
		number_of_moles = convert_to_moles(known_values, number_of_grams)
	#number_of_moles = convert_to_moles(known_values, number_of_grams)
	print("Number of moles")
	print(number_of_moles)

	if len(known_values)>1:
		# if there are multiple multiple known values, find the limiting factor which is used to calculate all of the results
		limiting_factor = find_limiting_factor(number_of_moles, all_substances, known_values, final_solutions, solutions, substanceslist, variables, equations, oofshit)
		print("Limiting factor is: "+str(limiting_factor))


	else:
		limiting_factor = known_values[0]




	ratio = getratio(limiting_factor, unknown, oofshit, all_substances)
	print("Ratiooooo")
	print(ratio)
	#print("Paskaaa")
	#print(ratio)
	#print(number_of_moles[known_values.index(limiting_factor)]/ratio)
	print("Amount of product: ")
	print(number_of_moles[known_values.index(limiting_factor)]/ratio)
	moles_of_product = number_of_moles[known_values.index(limiting_factor)]/ratio
	print(moles_of_product)
	print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
	print(unknown)
	print(moles_of_product)
	print(convert_from_moles_one_substance(unknown, moles_of_product))
	return



	'''


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

	'''
	

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




