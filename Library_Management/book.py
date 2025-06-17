class Book:
	'''The default book class'''
	def __init__(self,id: int, title : str, author : str, year : int, availability : bool = True):
		self.__id = id
		self.__title = title
		self.__author = author
		self.__year = year
		if (availability is bool):
			self.__availability = availability
		else:
			self.__availability = True if availability == 1 else False
	
	def __str__(self) -> str:
		return f'{self.__id}: {self.__title}, {self.__author} ({self.__year})'
		
	def borrow(self) -> bool:
		'''Allows the borrowing of the book if it is available'''
		if (self.__availability is True):
			self.__availability = False
			print("Book borrowed")
			return True
		else:
			print(self, " is unavailable")
			return False
		
	def returnBook(self) -> bool:
		self.__availability = True
		print("Book returned")
		return True
	
	def checkAvailability(self) -> bool:
		return self.__availability
	
	def getTitle(self) -> str:
		return self.__title
	
	def getAuthor(self) -> str:
		return self.__author
	
	def getYear(self) -> int:
		return self.__year
	
	def getID(self) -> int:
		return self.__id
	