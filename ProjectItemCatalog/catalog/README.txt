# Deployment instructions


1. Deploy repository on target server.
2. Insure the python libraries are installed: 
	sudo apt-get install python-flask python-sqlalchemy python-requests postgresql python-oauth2client
3. Initialise the database:
	python database_setup.py
4. Insert some initial data into database:
	python database_init.py
5. Run webserver:
	python project.py
