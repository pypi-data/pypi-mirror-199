# FaceDatabse-Identifier
A simple python package to identify the user on bases of there face and store there features in database

## Sample Code : 
```py
from facetranscript import *

if __name__=="__main__":
    face = CaptureFaceInDataBase()
    # Capture photo from front camera for user -> 'TestUser'
    face.take_photo(username="TestUser")
    # Fetch all stored users and there images in database 
    face_list = face.get_all_users()
    # face_list is list [a,b,c...] where a,b,c.. are list of users with there images(Bytes)
    print(face_list)
    # To terminate all connections (camera/database)
    face.close_all_connections()
```