import sqlite3
from pathlib import Path


def create_database_users(file_path):
    with open(file_path, "w"):
        con = sqlite3.connect(file_path)
        cursor = con.cursor()
        statement = """
        CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mail text not null,
        password text not null, 
        first_name text not null,
        last_name text not null);
        """
        cursor.execute(statement)
        con.commit()
        cursor.close()
        con.close()


def create_database_expenses(file_path):
    # with open(file_path, "r+"):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()
    statement = """
          CREATE TABLE Expenses (
          expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER not null,
          cost REAL not null,
          description text not null,
          category text not null,
          exp_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
          """
    cursor.execute(statement)
    con.commit()
    cursor.close()
    con.close()


def create_database_expense_category(file_path):
    # with open(file_path, "r+"):
    con = sqlite3.connect(file_path)
    cursor = con.cursor()
    statement = """
          CREATE TABLE Expense_category (
          category_id INTEGER PRIMARY KEY AUTOINCREMENT,
          expense_name text not null,
          category text not null);
          """
    cursor.execute(statement)
    con.commit()

    insert_statement = """
            INSERT INTO Expense_category (expense_name, category)
            VALUES 
            ("biedronka", "daily shoping"), 
            ("auchan", "daily shoping"), 
            ("walmart", "daily shoping"), 
            ("biedronka", "daily shoping"), 
            ("rossman", "cosmetic"),
            ("burger", "Street food & restaurant"), 
            ("pizza", "Street food & restaurant"),
            ("ramen", "Street food & restaurant"), 
            ("hindley", "Street food & restaurant");
            
            """
    cursor.execute(insert_statement)
    con.commit()
    cursor.close()
    con.close()


def database_exist():
    dir_path = Path.cwd() / Path("database")
    file_path = Path.cwd() / Path("database", "data.db")
    print(file_path)
    if not Path.exists(dir_path):
        Path.mkdir("database")
        create_database_users(file_path)
        create_database_expenses(file_path)
        create_database_expense_category(file_path)
        print("database was created")
        return file_path
    elif not Path.exists(file_path):
        create_database_users(file_path)
        create_database_expenses(file_path)
        print("database was created")
        return file_path
    else:
        print("database exist")
        return file_path


def user_exist(user_mail):
    file_path = database_exist()
    with open(file_path, "r+"):
        con = sqlite3.connect(file_path)
        cursor = con.cursor()
        statement = """
        SELECT mail
        FROM Users
        WHERE mail = ?;
        """
        cursor.execute(statement, (user_mail,))
        mail_finder = cursor.fetchall()
        con.commit()
        cursor.close()
        con.close()
        return bool(mail_finder)


def register_new_user(user_mail, user_password, user_first_name, user_last_name):
    file_path = database_exist()
    if user_exist(user_mail):
        return print("the mail exist in data base")
    else:
        with open(file_path, "r+"):
            con = sqlite3.connect(file_path)
            cursor = con.cursor()
            statement = """
            INSERT INTO Users (mail, password, first_name, last_name)
            VALUES (?, ?, ?, ?);
            """
            cursor.execute(statement, (user_mail, user_password, user_first_name, user_last_name))
            con.commit()
            cursor.close()
            con.close()

            return print("New user was register")


def correct_login(user_mail, user_password):
    file_path = database_exist()
    if user_exist(user_mail):
        with open(file_path, "r"):
            con = sqlite3.connect(file_path)
            cursor = con.cursor()
            statement = """
            SELECT password
            FROM Users
            WHERE mail = ? and password = ?;
            """
            cursor.execute(statement, (user_mail, user_password))
            selected_password = cursor.fetchall()
            return bool(selected_password)
    else:
        return False


def find_user_id(user_mail):
    file_path = database_exist()
    with open(file_path, "r"):
        con = sqlite3.connect(file_path)
        cursor = con.cursor()
        statement = """
        SELECT user_id
        FROM Users
        WHERE mail = ?;
        """
        cursor.execute(statement, (user_mail,))
        selected_user_id = cursor.fetchone()

        return selected_user_id[0]


def find_exp_category(description, file_path):
    with open(file_path, "r"):
        con = sqlite3.connect(file_path)
        cursor = con.cursor()
        statement = """
        SELECT category 
        FROM Expense_category
        WHERE expense_name = ?;
        """
        low_description = str(description).lower()
        cursor.execute(statement, (low_description,))
        found_category = cursor.fetchone()

        if bool(found_category):
            return found_category[0]
        else:
            return "unknown"
        con.commit()
        cursor.close()
        con.close()


def add_expense(user_mail, cost, description):
    user_id = find_user_id(user_mail)
    file_path = database_exist()
    category = find_exp_category(description, file_path)

    with open(file_path, "r+"):
        con = sqlite3.connect(file_path)
        cursor = con.cursor()
        statement = """
            INSERT INTO Expenses (user_id, cost, description, category)
            VALUES (?, ?, ?, ?);
            """
        cursor.execute(statement, (user_id, float(cost), description, category))
        con.commit()
        cursor.close()
        con.close()


def see_user_expenses(user_mail):
    user_id = find_user_id(user_mail)
    file_path = database_exist()

    with open(file_path, "r+"):
        con = sqlite3.connect(file_path)
        cursor = con.cursor()
        statement = """
        SELECT description, cost, category, exp_date
        FROM Expenses
        WHERE user_id = ?
        """
        cursor.execute(statement, (user_id,))
        user_expenses = cursor.fetchall()
        print(user_expenses)
        con.commit()
        cursor.close()
        con.close()
        return user_expenses
