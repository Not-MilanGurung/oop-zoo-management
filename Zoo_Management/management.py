from datetime import datetime
from os import path
import sqlite3
from animals import *

TABLE_CREATION = """
	CREATE TABLE IF NOT EXISTS animal(
		name VARCHAR(50) PRIMARY KEY,
		species VARCHAR(50) NOT NULL,
		age INT NOT NULL,
		feedingTime INT
	)
"""

SQL_INSERT = "INSERT INTO animal VALUES(?, ?, ?, ?)"
SQL_GET_ANIMALS = "SELECT * FROM animal"

class Management:
	def __init__(self) -> None:
		try:
			self.__connection = sqlite3.connect(str(path.dirname(__file__))+str('/animals.db'))
			self.__cursor = self.__connection.cursor()
			self.__cursor.execute(TABLE_CREATION)
		except sqlite3.Error as e:
			print(e)

	def closeConnection(self):
		self.__cursor.close()
		self.__connection.close()

	def addAnimal(self, animal : Animal):
		data = (animal.getName(), animal.getSpecies(), animal.getAge(), animal.getFeedingTime())
		self.__cursor.execute(SQL_INSERT, data)
		self.__connection.commit()

	def getAllAnimals(self):
		self.__cursor.execute(SQL_GET_ANIMALS)
		animals : list[Animal] = []
		for data in self.__cursor.fetchall():
			if (data[1] == 'Lion'):
				animals.append(Lion(data[0], data[2], data[3]))
			elif (data[1] == 'Elephant'):
				animals.append(Elephant(data[0], data[2], data[3]))
		return animals
	

def display_animals(animals):
    if not animals:
        print("No animals in the zoo.")
    for idx, animal in enumerate(animals):
        print(f"{idx+1}. {animal.getSpecies()} - {animal.getName()} (Age: {animal.getAge()}, Feeding Time: {animal.getFeedingTime():04d})")

def add_animal(mgmt: Management):
    name = input("Enter Animal Name: ")
    species = input("Enter Species (Lion/Elephant): ")
    age = int(input("Enter Age: "))
    feeding_time = int(input("Enter Feeding Time (HHMM 24hr format): "))

    if species.lower() == "lion":
        animal = Lion(name, age, feeding_time)
    elif species.lower() == "elephant":
        animal = Elephant(name, age, feeding_time)
    else:
        print("Unsupported species!")
        return

    try:
        mgmt.addAnimal(animal)
        print("Animal added successfully!")
    except Exception as e:
        print(f"Error adding animal: {e}")

def feed_animals(animals):
    current_time = datetime.now()
    print(f"Current Time: {current_time.strftime('%H:%M')}")
    for animal in animals:
        if animal.checkFeedingTime(current_time):
            print(f"Feeding {animal.getName()} the {animal.getSpecies()}:")
            animal.feed()
        else:
            print(f"{animal.getName()} is not scheduled to feed now.")

def change_feeding_time(animals, mgmt: Management):
    display_animals(animals)
    idx = int(input("Select animal number to change feeding time: ")) - 1
    if 0 <= idx < len(animals):
        new_time = int(input("Enter new Feeding Time (HHMM 24hr format): "))
        animals[idx].changeFeedingTime(new_time)

        # Update in DB
        animal = animals[idx]
        mgmt.addAnimal(animal)  # Overwrite with new feeding time
        print("Feeding time updated!")
    else:
        print("Invalid selection!")

def main():
    mgmt = Management()

    while True:
        print("\n--- Zoo Management System ---")
        print("1. Display All Animals")
        print("2. Add Animal")
        print("3. Feed Animals")
        print("4. Change Feeding Time")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            animals = mgmt.getAllAnimals()
            display_animals(animals)
        elif choice == '2':
            add_animal(mgmt)
        elif choice == '3':
            animals = mgmt.getAllAnimals()
            feed_animals(animals)
        elif choice == '4':
            animals = mgmt.getAllAnimals()
            change_feeding_time(animals, mgmt)
        elif choice == '5':
            print("Exiting Zoo Management System.")
            mgmt.closeConnection()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
