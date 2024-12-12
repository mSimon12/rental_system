# Rental System

Managing clients renting your products might look something easy in the beginning, 
but if your store gets bigger it will at some moment become very hard to monitor who 
has rented what and when. This application provides a simple Website to your 
store to manage the rentals.

Initially the focus of this project was provide a simple API for managing databases
of clients, items and the link client-item required for keeping track of the rentals. 
This API is ready to be used, and you can check out the API documentation 
[here](https://github.com/mSimon12/rental_system/tree/master/flaskr/api).
We are currently implementing the Frontend and access authentication, to make the 
system accessible and easy to use for any user.

The system is already composed by a client session, where clients can register, login and 
rent items according to their desire. Clients can access the stock and check for
availability of items (Comments on items is in development).
For the store staff it provides a session with restricted access where is possible 
to manage the stock. 

### Tech Stack:
Python, Flask, SQLite, HTML, Pytest

## Getting Started

To accomplish the installation of this system and run it, follow these steps:

```
git clone https://github.com/mSimon12/rental_system
cd rental_system
pip install -r requirements.txt

flask --app flaskr init-db
flask --app flaskr run
```

## Roadmap

The evolution of this project follows the sequence described below:

1. Initially, the basic implementation of a REST API with Flask have been done following the [Flask guetting started tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/)
2. With a first running application, we have configured our Database with SQLite. At this moment we added 2 tables for storing the items from the store and clients.
3. Base CRUD API was implemented to allow adding and deleting items to the store, as well as renting and returning them.
4. Included basic template for store main page, showing the items list and the available amount. Items specific pages were also included for accessing extra information and for item rental.
5. Manager page was inserted for store management.
6. API interface have been implemented to decouple Web app and API and translate calls made in the Frontend to the Backend.
7. Implemented rent and return buttons in store/item
8. Track on database who rented what
9. Implement use credentials management
10. Added unit test for client and items APIs
11. Create initial pipeline for continuous test at push
12. Implemented stateless role based authentication with JWT


### To-Do: 
* Split the app into 2 flask instances (backend and frontend-flask just for testing)
* Dockerize each instance
* Implement microservices
* Update Model base to SQLAlchemy and Postgress as db
* Add Flask-Admin for better admin management
* Save comments added on item page
* Deploy the application

## System view


![Representation of the system components](images/arch.png)