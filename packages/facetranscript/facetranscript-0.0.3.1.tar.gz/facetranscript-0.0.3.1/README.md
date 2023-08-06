# FaceDatabse-Identifier
A simple python package to identify the user on bases of there face and store there features in database

## Prerequisite :
* Must have GCC for dlib to work
## Sample Code : 
```py
from facetranscript import CaptureFaceInDataBase

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

### Delete user from database :
- To delete a single user
```py
from facetranscript import CaptureFaceInDataBase
face = CaptureFaceInDataBase()
# delete_user_data returns bool value if it is True user is deleted
is_user_deleted = face.delete_user_data("TestUser")
```
- To drop the complete table
```py
from facetranscript import CaptureFaceInDataBase
face = CaptureFaceInDataBase()
# is_table_dropped returns bool value if it is True table is deleted
is_table_dropped = face.drop_table()
```