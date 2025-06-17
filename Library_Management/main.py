from book import Book
import os
import sqlite3

TABLE_CREATION = """
	CREATE TABLE IF NOT EXISTS books(
		id INT PRIMARY KEY,
		title VARCHAR(50),
		author VARCHAR(50) NOT NULL,
		year INT NOT NULL,
		availability BOOLEAN DEFAULT TRUE
	)
"""

class CLI:
	def __init__(self) -> None:

		try:
			self.__connection = sqlite3.connect(str(os.path.dirname(__file__))+str('/books.db'))
			self.__cursor = self.__connection.cursor()
			self.__cursor.execute(TABLE_CREATION)
		except sqlite3.Error as e:
			print(e)

	def closeConnection(self):
		self.__cursor.close()
		self.__connection.close()
	
	def addToDB(self, book : Book) -> bool:
		try:
			add = 'INSERT INTO books VALUES(?,?,?,?,?)'
			self.__cursor.execute(add, (book.getID(), book.getTitle(), book.getAuthor(), book.getYear(), book.checkAvailability()))
			self.__connection.commit()
			return True

		except sqlite3.Error as e:
			print("ERROR: ",e)
			return False

	def getAvailableBooks(self) -> list[Book]:
		self.__cursor.execute("SELECT * FROM books WHERE availability = True")
		books : list[Book] = []
		for data in self.__cursor.fetchall():
			books.append(Book(data[0], data[1], data[2], data[3], data[4]))
		return books

	def getBooks(self, title : str):
		sql = "SELECT * FROM books WHERE title LIKE ?"
		self.__cursor.execute(sql, (f'%{title}%',))
		books : list[Book] = []
		for data in self.__cursor.fetchall():
			books.append(Book(data[0], data[1], data[2], data[3], data[4]))
		return books

	def getBook(self, id : int = -1, title : str = ''):
		if (id == -1):
			print("You need either id or title:")
			return None
		
		sql = "SELECT * FROM books WHERE id = ?"
		self.__cursor.execute(sql, (id,))

		data = self.__cursor.fetchone()
		if data is None:
			print("No match found")
			return None
		else:
			book = Book(data[0], data[1], data[2], data[3])
			return book
	
	def borrow(self, book : Book):
		self.__cursor.execute("UPDATE books SET availability = FALSE WHERE id = ?", (book.getID(),))
		self.__connection.commit()

	def returnBook(self, book : Book):
		self.__cursor.execute("UPDATE books SET availability = TRUE WHERE id = ?", (book.getID(),))
		self.__connection.commit()

	def menu(self) -> bool:
		loop : bool = True
		print('''
			Enter the number corresponding to the option:
			1) Add a book
			2) List available books
			3) Borrow a book
			4) Return a book
			5) Search a book by title
			x) Any other number to quit	
		''')
		try:
			choice : int = int(input("Enter your choice: "))

			if (choice == 1):
				id = int(input("Enter book id: "))
				title = input("Enter the title of the book: ")
				author = input("Enter the author of the book: ")
				year = int(input("Enter the year of publishment: "))
				if (self.addToDB(Book(id, title, author, year))):
					print("Book added to the list")
				else:
					print("Could not add the book")

			elif (choice == 2):
				print("The list of available books: ")
				for book in self.getAvailableBooks():
					print(book)

			elif(choice == 3):
				id = int(input("Enter the id of the book: "))
				book = self.getBook(id)
				if (book != None):
					yn = input(f"Borrow this book {book} (y/n): ")
					if (yn == 'y' and book.borrow()):
						self.borrow(book)

			elif(choice == 4):
				id = int(input("Enter the id: "))
				book = self.getBook(id)
				if (book != None):
					yn = input(f"Return this book {book} (y/n): ")
					if (yn == 'y'):
						book.returnBook()
						self.returnBook(book)
			elif (choice == 5):
				title = input("Enter the title of the book: ")
				books = self.getBooks(title)
				if (books != None):
					for book in books:
						print(f"{book} Availability: {book.checkAvailability()}")
			else:
				loop = False
				

		except Exception as e:
			print("Error: ",e)

		return loop
		

if __name__ == '__main__':
	cli = CLI()
	while(True):
		if (cli.menu() is False):
			break
	cli.closeConnection()
	print('Exiting')