from abc import ABC, abstractmethod
from datetime import datetime

class Animal(ABC):
	def __init__(self, name : str, age : int, feeding_time : int) -> None:
		self.__name = name
		self.__age = age
		self.__feeding_time = feeding_time # 24-hour format 4 digit number

	def __str__(self) -> str:
		return f'Name: {self.__name}, Age: {self.__age}'

	def getName(self) -> str:
		'''Returns the name of the animal'''
		return self.__name

	@abstractmethod
	def getSpecies(self) -> str:
		pass	

	def getAge(self) -> int:
		return self.__age
	
	def getFeedingTime(self) -> int:
		return self.__feeding_time
	
	def changeFeedingTime(self, newTime : int):
		if (newTime// 100 in range(0, 24)
	  		and newTime % 100 in range(0,60)):
			self.__feeding_time = newTime
			print("Changed feeding time")
		else:
			print("Invaild time. Must be 24-hour format (2300)")
	
	def checkFeedingTime(self, currentTime : datetime) -> bool:
		if (self.__feeding_time // 100 == currentTime.hour
	  		and self.__feeding_time % 100 == currentTime.minute):
			return True
		else:
			return False
	
	@abstractmethod
	def feed(self):
		pass

	def make_sound(self):
		print("Animal sounds!")

class Lion(Animal):
	def getSpecies(self):
		return "Lion"

	def feed(self):
		print("Lion eats the meat")

	def make_sound(self):
		print("Lion roars!")

class Elephant(Animal):

	def getSpecies(self) -> str:
		return "Elephant"
	
	def feed(self):
		print("Elephant is eating the plants")

	def make_sound(self):
		print("Elephant makes sound")
