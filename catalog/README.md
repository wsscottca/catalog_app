#Item Catalog app#

##Setup# -

 1. Install virtual machine from [here](https://github.com/udacity/fullstack-nanodegree-vm)
 2. Clone the catalog project into your shared vagrant folder
 3. Start the machine by changing into it's directory and entering `vagrant up`
 4. Log in to the machine using `vagrant ssh`
 5. Change into the vagrant folder then catalog app using `cd /vagrant/catalog`
 6. Install dependencies using:
    ```
    	sudo apt-get python
    	sudo apt-get flask
    	sudo apt-get flask-login
    ```
 7. Setup the database using `python database_setup.py`
 8. Fill the database with mock data using `python starter_content.py`

##Run the app#

  To run the app enter the catalog directory and run `python project.py`,
    app should start on http://localhost:5000/ connect using your browser.
