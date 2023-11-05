
from pandas import read_csv

def load_data():
	filename = "/home/cyberhacker/Asioita/Ohjelmointi/Python/Chemicalequationbalancer/PeriodicTableCSV.csv"
	data = read_csv(filename)

	#print(data['symbol'].tolist())
	#print(data['atomic_mass'].tolist())
	return data['symbol'].tolist(), data['atomic_mass'].tolist()










if __name__=="__main__":
	print(load_data())
