from facetranscript import UserDatabase, CaptureFace
class CaptureFaceInDataBase:
    def __init__(self, database_name:str = 'db.sqlite3',
                table_name:str = 'users', save_image: bool= False, image_location:str="dataset",
                haarcascade_frontalface_location : str = './haarcascade_frontalface_default.xml') -> None:
        # Created database
        self.user_database = UserDatabase(database_name=database_name, table_name=table_name)
        self.user_database.create_user_database()
        # Initiating camera
        self.capture_face = CaptureFace(save_image=save_image, image_location=image_location, 
                                        haarcascade_frontalface_location=haarcascade_frontalface_location)
        
        self.save_image = save_image
        
    def take_photo(self, username )-> None:
        image_bytes = self.capture_face.capture_image(user_name=username)
        self.user_database.insert_user_data_no_image(
            user_name=username, image_bytes=image_bytes
        )

    def get_all_users(self)-> list:
        return self.user_database.get_all_user_data()
    
    def get_user_with_username(self, username)-> list:
        return self.user_database.get_user(user_name=username)
    
    def close_all_connections(self)-> None:
        self.user_database.terminate_database_connection()


