# Deployment instructions


1. Deploy repository on target server.
2. Insure the python libraries are installed: 
	sudo apt-get install python-flask python-sqlalchemy python-requests postgresql
3. Initialise the database:
	python database_setup.py
4. Insert some initial data into database:
	python database_init.py
5. Run webserver:
	python project.py
6. JSON endpoints:
	route('/api/v1/catalog.json')
		returns the entire catalog
	route('/api/v1/categories/JSON')
		returns all the categories
	route('/api/v1/categories/<int:category_id>/item/<int:item_id>/JSON')
		returns an items data selected by cataegory id and item id
