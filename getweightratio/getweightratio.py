import sympy
import numpy as np
from sympy.parsing.sympy_parser import parse_expr


"""

Todo:

1. Get input of two chemical equations
2. Get mass of the two leftover reagents and mass of gas which gets released.
3. Construct equations out of given values which the user gives.







"""



import dataloader


def get_molar_mass(substance):
	# first seperate the substance to individual elements and coefficients:
	print(substance)
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



def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


def removeintegers(string):
	return ''.join([i for i in string if not i.isdigit()])



def parse_formula(chemical_formula: str):
	reactants = chemical_formula[:chemical_formula.find("->")]
	products = chemical_formula[chemical_formula.find("->")+2:]

	
	reactants = reactants.split("+")
	products = products.split("+")
	
	substances = reactants+products
	substances = list(dict.fromkeys(substances))


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
	
	
	matrixthing = []
	oofpaska = []
	for element in elements_r:
		ooflist = []
		for substance in reactants:
			
			
			
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
		
		print(ooflist)
		matrixthing.append(ooflist)
	

	elementmatrix = sympy.Matrix(matrixthing)
	print("Nullspace:")
	print(elementmatrix.nullspace())
	solutions = []
	for solution in elementmatrix.nullspace():
		solutions.append(solution)

	
	print("Dot product: ")
	print(elements_r)

	

	oofs = []
	for oof in range(len(solutions)):
		oofs.append(sympy.lcm([val.q for val in solutions[oof]]))

	
	
	for i in range(len(solutions)):
		solutions[i] = solutions[i].tolist()
		solutions[i] = flatten(solutions[i])

	
	
	
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
	
	return (substances, vectorsum, len(reactants), (reactants, products))


from sympy import solve_poly_system

def solve_system(eq1, eq2, k1, mass, k2, mass2):

	# first balance equations:

	substances, solution, oof, things = parse_formula(eq1)

	substances2, solution2, oof2, things2 = parse_formula(eq2)

	print(solution)
	print(solution2)


	# we have the coefficients for the chemical equations

	# construct the two equations:

	# first construct the n(C1)+n(C2)=mass2/(M(C))

	# the indexes are in k2

	# refer to all of the molar amounts as variables from the alphabet

	how_many_variables = len(substances)+len(substances2)

	print(how_many_variables)

	# generate a list of variables

	alphabet = "abcdefghijklmnopqrstuvxyz"
	variables = []
	for i in range(how_many_variables):
		variables.append(sympy.symbols(alphabet[i]))
	print(variables)

	# parse k2

	k2_integers = [int(x) for x in k2.split(" ")]

	print(k2_integers)


	variable1 = variables[k2_integers[0]-1]
	variable2 = variables[k2_integers[1]+len(substances)-1]
	print(variable1)
	print(variable2)

	# mass2/M(mass2) = variable1 + variable2


	n_mass2 = float(mass2)/(get_molar_mass(substances[k2_integers[0]-1]))
	print(n_mass2)


	# generate equation
	print(str(variable1) +"+"+str(variable2))
	print(n_mass2)
	carbon_dioxide_eq = sympy.Eq(n_mass2, parse_expr(str(variable1) +"+"+str(variable2)))
	print(carbon_dioxide_eq)


	# generate second equation ( m(A)+m(D) = mass1 )

	# aka (  n(A)*M(A) + n(D)*M(D) = mass1  )


	# n(A)=variables[k1_integers[0]-1]
	# n(D) = variables[k1_integers[1]+len(substances)-1]
	k1_integers = [int(x) for x in k1.split(" ")]



	thing1 = variables[k1_integers[0]-1]
	thing2 = variables[k1_integers[1]+len(substances)-1]

	# calculate M(A)

	molar_A= get_molar_mass(substances[k1_integers[0]-1])

	molar_D = get_molar_mass(substances2[k1_integers[1]-1])

	# parse equation:

	mass_eq = sympy.Eq(parse_expr(str(thing1)+"*"+str(molar_A)+"+"+str(thing2)+"*"+str(molar_D)), parse_expr(str(mass)))
	print(mass_eq)


	# now the stoichiometrix ratio equations from the solutions to the chemical equations:

	# get ratio in the first equation

	# the first equation is of the form m1*a = m2*c

	# solution[k1_integers[0]]*variables[k1_integers[0]] = solution[k2_integers[0]] * variables[k2_integers[0]]
	print(solution[k1_integers[0]-1])
	print(str(variables[k1_integers[0]-1]))
	print(solution[k2_integers[0]-1])
	print(variables[k2_integers[0]-1])
	#first_stoichiometric_eq = sympy.Eq(parse_expr(str(solution[k1_integers[0]-1])+"*"+str(variables[k1_integers[0]-1])), parse_expr(str(solution[k2_integers[0]-1])+"*"+str(variables[k2_integers[0]-1])))
	first_stoichiometric_eq = sympy.Eq(parse_expr(str(variables[k1_integers[0]-1])+"/"+str(solution[k1_integers[0]-1])), parse_expr(str(variables[k2_integers[0]-1])+"/"+str(solution[k2_integers[0]-1])))

	print(first_stoichiometric_eq)

	# second stoichiometric equation:

	#second_stoichiometric_eq = sympy.Eq(parse_expr(str(solution[k1_integers[0]-1])+"*"+str(variables[k1_integers[0]-1])), parse_expr(str(solution[k2_integers[0]-1])+"*"+str(variables[k2_integers[0]-1])))

	#second_stoichiometric_eq = sympy.Eq(parse_expr(str(solution2[k1_integers[1]-1])+"*"+str(variables[k1_integers[1]+len(substances)-1])), parse_expr(str(solution2[k2_integers[1]-1])+"*"+str(variables[k2_integers[1]+len(substances)-1])))
	second_stoichiometric_eq = sympy.Eq(parse_expr(str(variables[k1_integers[1]+len(substances)-1])+"/"+str(solution2[k1_integers[1]-1])), parse_expr(str(variables[k2_integers[1]+len(substances)-1])+"/"+str(solution2[k2_integers[1]-1])))

	print(second_stoichiometric_eq)


	# now we have all of the required equations:


	print(solve_poly_system([second_stoichiometric_eq, first_stoichiometric_eq, mass_eq, carbon_dioxide_eq]))







	exit()


# get user inputs:




if __name__=="__main__":



	eq1 = str(input("Give first chemical equation: "))

	eq2 = str(input("Give second chemical equation: "))

	k1 = str(input("Give indexes which masses are equal to something"))

	mass = str(input("Give mass: "))

	k2 = str(input("Give mass of the thing which is the mass: "))

	mass2 = str(input("Give another mass: "))


	print(solve_system(eq1, eq2, k1, mass, k2, mass2))
	exit()











