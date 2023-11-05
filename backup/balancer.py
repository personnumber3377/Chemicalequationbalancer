
import numpy as np
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





'''





def parse_formula(chemical_formula: str):
	reactants = chemical_formula[:chemical_formula.find("->")]
	products = chemical_formula[chemical_formula.find("->")+2:]

	print(reactants)
	print(products)
	reactants = reactants.split("+")
	products = products.split("+")
	print(reactants)



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
			if element in substance:
				elementstuff = substance.split(".")
				for element2 in elementstuff:
					if element in element2:
						ooflist.append(int(element2[element2.find(element)+len(element):])*-1)
			else:
				ooflist.append(0)
		oofpaska.append(ooflist[0])
		ooflist.pop(0)
		print(ooflist)
		matrixthing.append(ooflist)
	#matrixthing.append([0,0,0,1])
	A = np.array(matrixthing)
	#print(A.shape)
	#inv_A = np.linalg.inv(A)
	B = np.array([0]*A.shape[0])
	#print("B: "+str(B))
	#X = np.linalg.inv(A).dot(B)
	#print(X)
	print(A)
	print(np.linalg.solve(A,np.array(oofpaska)*-1))
	#print(oofpaska)




def balanceformula(chemical_formula: str):
	indexes = parse_formula(chemical_formula)


if __name__ == "__main__":
	balanceformula(input("Enter chemical formula: "))

