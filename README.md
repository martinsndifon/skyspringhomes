# skyspringhomes
* This is a real estate web application for a small real estate company
* Live Version
   <to be updated>
## Goal
The major goal of this project was to further solidify my knowledge of using the technologies listing below in building an application. The application gives the owner of the small real estate company the flexibility of dynamically updatating the websites by creating, modifying or deleting properties/listings as they desire.

## Future update
The mvp of the project was completing the major functionality of allowing for secure CRUD operations by admin to dynamically update the website. Listing below are other features that will be added either to this version of the build or a totally new version using this version as the base for that build.
- Users can signup in two categories; an agent and a client(regular user)
- Signed in clients will have more functionalities which include but not limited to;
	* Favoriting a property for easy reference on revisit
	* A messaging section where clients can leave a message for an agent
- Signed in agents will also have more functionalities
	* A messaging section to interact with client messages
	* A section to manage their uploaded properties(Create, modify or delete)
- Location will be improved to contain different states and cities
- Listings will have a better setup, which will include amenities and other distinguishing factors
- A robust search feature will be added so users can better filter out properties based on different options

## Technologies used
- Backend in python
- RestfulApi
- MySQL
- sqlalchemy
- flask
- JQuery

# API Routes

| Method  |       Route                     | Authentication | Description                                           |
|:-------:|:-------------------------------:|:--------------:|:-----------------------------------------------------:|
|  GET    | /api/v1/rent                    |       NO       | Returns all the listings for rent                     |
|  GET    | /api/v1/rent/{id}               |       YES      | Returns a single rented property                      |
|  GET    | /api/v1/rent/type/{rent_type}   |       NO       | Returns rented properties of a particular type        |
|  POST   | /api/v1/rent                    |       YES      | Creates a new property for rent                       |
|  PUT    | /api/v1/rent/{id}               |       YES      | Updates a rented property with new information        |
|  DELETE | /api/v1/rent/{id}               |       YES      | Deletes a rented property                             |
|  GET    | /api/v1/sale                    |       NO       | Returns all the listings for sale                     |
|  GET    | /api/v1/sale/{id}               |       YES      | Returns a single sale property                        |
|  POST   | /api/v1/sale                    |       YES      | Creates a new property for sale                       |
|  PUT    | /api/v1/sale/{id}               |       YES      | Updates a sale property with new informatioin         |
|  DELETE | /api/v1/sale/{id}               |       YES      | Deletes a sale property                               |
|  GET    | /api/v1/service_apartments      |       NO       | Returns all service apartments listings               |
|  GET    | /api/v1/service_apartments/{id} |       YES      | Returns a single service apartment                    |
|  POST   | /api/v1/service_apartments      |       YES      | Creates a new service apartment                       |
|  PUT    | /api/v1/service_apartments/{id} |       YES      | Updates a service apartments with new information     |
|  DELETE | /api/v1/service_apartments/{id} |       YES      | Deletes a service apartment                           |

# Backend 

# Requirements
- MySQL
- Python3.8 upwards

```bash
# Clone the repo
git clone https://github.com/martinsndifon/skyspringhomes
# Move into the project directory
cd skyspringhomes/
# Copy env template to .env
cp env .env
```

- Edit .env
```bash
SKY_MYSQL_USER=your_db_user
SKY_MYSQL_PWD=your_db_pwd
SKY_MYSQL_HOST=your_db_host
SKY_MYSQL_DB=your_db_name
SKY_ENV=dev_or_test
ADMIN_USERNAME=name_for_api_authentication
ADMIN_PASSWORD=password_for_api_authentication
```

- Setup the database
```bash
# This step assumes you have sucessfully installed and configured MySQL 8.0.xx with root login
# edit the place holder names in the setup file before proceeding to the next step
cat setup_mysql_dev.sql | mysql -uroot -p
# create the necessary tables in the db
cat setup.sql | mysql -uroot -p your_db_name
```

# How to run the backend
```bash
# Install required dependencies from the requirement.txt file
pip3 install -r requirement.txt
# Start the Restful api
python3 -m api.v1.app
```

# Run the frontend
```bash
# Run the main website
python3 -m web_dynamic.app
# Run the admin version of the website
python3 -m web_dynamic_admin.app
```
Open you browser and navigate to the flask url to view to the development website