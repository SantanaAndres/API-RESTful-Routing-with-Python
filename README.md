# API-RESTful-Routing-with-Python
This repository, named "RESTfulAPIBuilder," showcases the development of a robust RESTful API using Flask and SQLAlchemy. The API is designed for managing information about cafes, including their locations, amenities, and pricing details. The API supports various HTTP methods for creating, reading, updating, and deleting cafe records.

Key Features:

## Random Cafe Generator:

### Endpoint: /random
Method: GET
Description: Returns a random cafe from the database, providing essential details such as location, amenities, and pricing.
List All Cafes:

### Endpoint: /all
Method: GET
Description: Retrieves information about all cafes stored in the database, presenting a comprehensive list of cafe records.
Search by Location:

### Endpoint: /search
Method: GET
Parameters: loc (Location to search)
Description: Allows users to search for cafes based on a specific location, providing details of matching cafes.
Add New Cafe:

### Endpoint: /add
Method: POST
Description: Enables the addition of a new cafe to the database, with parameters for specifying the cafe's details such as name, location, and amenities.
Update Cafe Price:

### Endpoint: /update-price/<int:cafe_id>
Method: PATCH
Parameters: new_price (New coffee price)
Description: Facilitates the modification of a cafe's coffee price based on the provided cafe ID.
Delete Cafe Record:

### Endpoint: /report-closed/<int:cafe_id>
Method: DELETE
Parameters: api-key (API key for authentication)
Description: Allows the removal of a cafe record from the database, provided the correct API key is supplied for authentication.
Usage:

Clone the repository.
Set up the Flask application and initialize the SQLite database.
Utilize the defined API endpoints for various operations, such as fetching random cafes, listing all cafes, searching by location, adding new cafes, updating prices, and deleting cafe records.
