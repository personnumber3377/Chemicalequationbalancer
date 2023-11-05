
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


if __name__=="__main__":
	while input("Do you want to continue?:") != "n":

		known_values = str(input("Minkä aineen moolimassa halutaan tietää?: "))
		print(get_molar_mass(known_values))
	exit()
