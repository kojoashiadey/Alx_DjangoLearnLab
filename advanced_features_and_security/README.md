Permissions and Groups Setup
This project demonstrates managing permissions and groups in Django.

Custom Permissions
The Book model defines the following permissions:

can_view – Can view book records
can_create – Can create book records
can_edit – Can edit book records
can_delete – Can delete book records
Groups
Viewers → can_view
Editors → can_view, can_create, can_edit
Admins → all permissions
Views Protection
Views are protected using @permission_required:

book_list → requires can_view
book_create → requires can_create
book_edit → requires can_edit
book_delete → requires can_delete
Testing
Create users via Django Admin
Assign them to groups
Try accessing book pages to verify permissions enforcement
