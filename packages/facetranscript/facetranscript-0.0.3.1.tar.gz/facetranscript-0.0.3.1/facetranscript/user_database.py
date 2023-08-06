import sqlite3
import logging
class UserDatabase:
    def __init__(self, database_name:str = 'db.sqlite3', table_name:str = 'users') -> None:
        self.database_name = database_name
        self.table_name = table_name
        self.sqlite_insert_blob_query = f""" INSERT INTO {self.table_name}
                                        (user_name, user_image) VALUES (?, ?)"""
        self.connect_to_database()

    def set_database_name(self, database_name: str) -> None:
        if '.sqlite3' not in database_name:
            database_name = database_name +".sqlite3"
        self.database_name = database_name

    def set_table_name(self, table_name: str) -> None:
        self.table_name = table_name
        self.sqlite_insert_blob_query = f""" INSERT INTO {self.table_name}
                                        (name, img) VALUES (?, ?)"""
    
    def connect_to_database(self) -> None:
        self.conn = sqlite3.connect(self.database_name)
        self.connection = self.conn.cursor()

    def create_user_database(self) -> None:
        self.connection.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table_name}
                ([user_name] TEXT PRIMARY KEY, [user_image] TEXT)
                ''')
        self.conn.commit()
    
    def insert_user_data(self, user_name:str, image_path:str)->None:
        user_image = convert_to_binary_data(image_path)
        data_tuple = (user_name, user_image)
        try:
            self.connection.execute(self.sqlite_insert_blob_query, data_tuple)
            self.conn.commit()
            print("Image and file inserted successfully as a BLOB into a table")
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                print(str(e) + " : Enter new user_name")
                raise ValueError("Enter new user_name")
            else:
                print(e)
                raise KeyError(str(e))
    
    def insert_user_data_no_image(self, user_name:str, image_bytes:bytes)->None:
        user_image = image_bytes
        data_tuple = (user_name, user_image)
        try:
            self.connection.execute(self.sqlite_insert_blob_query, data_tuple)
            self.conn.commit()
            print("Image and file inserted successfully as a BLOB into a table")
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                print(str(e) + " : Enter new user_name")
                raise ValueError("Enter new user_name")
            else:
                print(e)
                raise KeyError(str(e))
    
    def get_all_user_data(self) -> list:
        self.connection.execute(f'''
                            SELECT
                            USER_NAME, USER_IMAGE
                            FROM {self.table_name}
                                ''')
        return self.connection.fetchall()
    
    def get_user(self, user_name) -> list:
        self.connection.execute(f'''
                            SELECT
                            USER_NAME, USER_IMAGE
                            FROM {self.table_name}
                            WHERE USER_NAME is '{user_name}'
                                ''')
        return self.connection.fetchall()
    
    def delete_user_data(self, user_name)-> bool:
        try:
            self.connection.execute(f'''
                                DELETE
                                FROM {self.table_name}
                                WHERE USER_NAME is '{user_name}'
                                    ''')
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(str(e))
            return False
    
    def drop_table(self)-> bool:
        self.connection.execute(f'''DROP table {self.table_name}''')
        self.conn.commit()
        logging.info("Table dropped!")
        return True
    
    def terminate_database_connection(self)-> None:
        self.connection.close()

def convert_to_binary_data(filename):
    # Convert binary format to images 
    # or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

if __name__=="__main__":
    user = UserDatabase()
    user.create_user_database()
    user.insert_user_data(user_name="TestUser", image_path="dataset/TestUser.jpg")
    users_list = user.get_all_user_data()
    print(users_list[0][0])
    filtered_user = user.get_user(user_name="TestUser")
    if len(filtered_user) != 0:
        user_name = filtered_user[0][0]
        user_image = filtered_user[0][1]
        print(type(user_image))
    user.terminate_database_connection()
    