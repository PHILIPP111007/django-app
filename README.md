# django-app

Hello everyone! This is my first Django application. It is designed to work with a table. I created a primitive model that describes a person (first name, last name, age). Pretty little information, but you can easily change the models and forms if you want, also add more fields for statistics.

When you start the application you will see the first page where you can see the table and a small statistic accompanying it, you can also see a field for the user to log in as an administrator. The table cannot be changed until you enter your login and password.

I recorded the login and password in the SQLite model.

#### Login: admin
#### Password: admin

You can change this information in the database if you want, or you can enter more.

After logging in as a system administrator you can:

1) add new users one at a time (the corresponding form is provided for this purpose)
2) add new users by uploading a .csv file
3) delete all records at a time
4) save all records as a .csv file
5) Search for entries, for this you will see the form on the page (the search includes a filtering function, for example you can search for users who have the age of 20). As a result of the search you will see a table with the result, which can also be saved as a .csv file

Have fun!
