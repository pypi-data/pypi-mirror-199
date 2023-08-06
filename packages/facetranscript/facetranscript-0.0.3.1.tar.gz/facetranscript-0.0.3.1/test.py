from facetranscript import CaptureFaceInDataBase

# if __name__=="__main__":
#     face = CaptureFaceInDataBase()
#     # Capture photo from front camera for user -> 'TestUser'
#     face.take_photo(username="TestUser")
#     # Fetch all stored users and there images in database 
#     face_list = face.get_all_users()
#     # face_list is list [a,b,c...] where a,b,c.. are list of users with there images(Bytes)
#     print(face_list)
#     # To terminate all connections (camera/database)
#     face.close_all_connections()


# if __name__=="__main__":
#     face = CaptureFaceInDataBase()
#     print(face.delete_user_data("TestUser"))
#     # face.take_photo(username="TestUser")
#     # print(face.drop_table())
#     face_list = face.get_all_users()
#     print(len(face_list))
#     # To terminate all connections (camera/database)
#     face.close_all_connections()

if __name__ == "__main__":
    face = CaptureFaceInDataBase()
    face.take_photo(username="TestUser")
    face_list = face.get_all_users()
    print(len(face_list))
    face.close_all_connections()