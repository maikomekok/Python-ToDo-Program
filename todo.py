import datetime 
import pytz
import sqlite3



connection = sqlite3.connect("todo_database.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS todos(
						uid INTEGER PRIMARY KEY AUTOINCREMENT,
						todo_text TEXT,
						Adate TEXT,
						Edate TEXT,
						status TEXT DEFAULT 'undone' )""")


	
class Todo:

	@staticmethod
	def _get_local_time():
		return pytz.utc.localize(datetime.utcnow()).astimezone().isoformat()

	
	def __init__(self):
		self.uid = None
		self.text = ""
		self.date = datetime.datetime.now()
		self.Adate = self.date.strftime("%d/%m/%Y %H:%M")
		self.Edate = ""
		self.status = "undone"
		

	def add_todo_db(self, text, Edate):
		self.text = text
		self.Edate = Edate

		cursor.execute("""INSERT INTO todos(todo_text, Adate, Edate)
								VALUES
								(?, ?, ?)""", (self.text, self.Adate, self.Edate))

		connection.commit()

		cursor.execute("SELECT last_insert_rowid()")

		self.uid = cursor.fetchone()[0]

		print("\nჩანაწერი წარმატებით დამატებულია!")



	def edit_todo_db(self, position, newText, status):
		position_uid = get_position_uid(position)

		cursor.execute("""UPDATE todos SET todo_text = ?, status = ?
							WHERE uid = ?""", (newText, status, position_uid))


		connection.commit()

		
	def edit_todo_deadline_db(self, Edate, position):
		position_uid = get_position_uid(position)

		cursor.execute("""UPDATE todos SET Edate = ?
							WHERE uid = ?""", (Edate, position_uid,))

		print("\nჩანაწერი წარმატებით შეცვლილია!")

		connection.commit()


	def delete_todo_db(self, position):
		position_uid = get_position_uid(position)

		cursor.execute("DELETE FROM todos WHERE uid = ?", (position_uid,))
		connection.commit()

		print("\nჩანაწერი წარმატებით ამოშლილია!")



	def show_all_db(self):
    
		data = fetch_data()

		for index, item in enumerate(data, 1):

			print("-" * 35 + str(index) + "-" * 35)
			print(f"{item[1]} - added: {item[2]}, deadline: {item[3]}, status: {item[4]}")
			print("-" * 71)
	




def fetch_data():
	cursor.execute("SELECT * FROM todos")
	data = cursor.fetchall()

	return data



def checked_choice(choice):
	if choice.isdigit():
		choice = int(choice)

	else:
		choice = choice.lower()

	return choice



def get_data_last_index():
	data = fetch_data()

	for index, item in enumerate(data, 1):
		last_item_index = index

	return last_item_index



def get_position_uid(position):
	data = fetch_data()
	position_uid = data[position][0]

	return position_uid


def deadline_time():
	d = input("შეიყვანეთ Todo-ს დასრულების დღე: ")
	m = input("შეიყვანეთ Todo-ს დასრულების თვე: ")
	Y = input("შეიყვანეთ Todo-ს დასრულების წელი: ")
	H = input("შეიყვანეთ Todo-ს დასრულების საათი: ")
	M = input("შეიყვანეთ Todo-ს დასრულების წუთი: ")

	Edate = f"{d}/{m}/{Y} {H}:{M}"

	return Edate

def edit_deadline(todo, position):
	deadline_update = input("გსურთ დედლაინის შეცვლა? (Y/N): ")
	deadline_update = deadline_update.lower()


	if deadline_update == "y" or deadline_update == "1":
		todo.edit_todo_deadline_db(deadline_time(), position)

	else:
		print("\nჩანაწერი წარმატებით შეცვლილია!")



def user_input(menu_status):
	
	last_item_index = get_data_last_index()

	while True:
		position = input(f"აირჩიეთ ჩანაწერი {menu_status}: ")

		if not position.isdigit():
			print("გთხოვთ შეიტანოთ რიცხვი!")
			continue

		if int(position) > (last_item_index + 1) or int(position) < 0:
			print("გთხოვთ აირჩიოთ დადებითი მნიშვნელობა დიაპაზონში!")
			continue

		position = int(position) - 1
		break

	return position




def menu():
	
	choice = None
	todo = Todo()


	while True:
		print("\nToDo პროგრამის მენიუ:")
		print("1. ToDo-ს დამატება")
		print("2. ToDo-ს რედაქტირება")
		print("3. ToDo-ს ამოშლა")
		print("4. ჩანაწერების ჩვენება")
		print("პროგრამიდან გამოსასვლელად აკრიფეთ 'exit'")


		choice = input("\nაირჩიეთ მოქმედება: ")
		choice = checked_choice(choice)



		if choice == 1:
			
			text = input("შეიყვანეთ ტექსტი ToDo-სთვის: ")
			Edate = deadline_time()

			todo.add_todo_db(text, Edate)


		elif choice == 2:
			
			if get_data_last_index():
				todo.show_all_db()

				position = user_input("ჩასანაცვლებლად")

				newText = input("შეიტანეთ ახალი ტექსტი: ")
				status = input("შეიტანეთ სტატუსი (done/undone): ")

				edit_deadline(todo, position)

				todo.edit_todo_db(position, newText, status)


			else:
			 	print("ბაზაში ჩანაწერები ვერ მოიძებნა")



		elif choice == 3:
			
			if get_data_last_index():

				todo.show_all_db()

				position = user_input("ამოსაშლელად")

				todo.delete_todo_db(position)


			else:
				print("ჩანაწერები ამოსაშლელად ვერ მოიძებნა")



		elif choice == 4:
			todo.show_all_db()


		elif choice == "exit":
			print("ნახვამდის")
			break


		else:
			print("გთხოვთ სწორად აირჩიოთ მენიუს პუნქტი!")		


menu()