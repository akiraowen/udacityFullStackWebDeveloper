Place your catalog project in this directory.

1a. Deploy repository on server
1b. Insure python libraries are installed: 
	sudo apt-get install python-flask python-sqlalchemy python-requests postgresql
2. Initialise the database with: python database_setup.py
3. Insert base item catalog into database: python database_init.py
4. Run server code: python project.py
