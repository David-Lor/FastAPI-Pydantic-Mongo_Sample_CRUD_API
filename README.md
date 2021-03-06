# FastAPI + Pydantic + MongoDB REST API Example

Sample API using FastAPI, Pydantic models and settings, and MongoDB as database - non-async.

The API works with a single entity, "Person" (or "People" in plural) that gets stored on a single Mongo database and collection.

The code is intended to create the whole OpenAPI documentation with the maximum detail, including full, detailed models for requests, responses and errors.

## Endpoints

Endpoints define the whole CRUD operations that can be performed on Person entities:

- GET `/docs` - OpenAPI documentation (generated by FastAPI)
- GET `/people` - list all available persons
- GET `/people/{person_id}` - get a single person by its unique ID
- POST `/people` - create a new person
- PATCH `/people/{person_id}` - update an existing person
- DELETE `/people/{person_id}` - delete an existing person

## Project structure (modules)

- `app.py`: initialization of FastAPI and all the routes used by the API. On APIs with more endpoints and different entities, would be better to split the routes in different modules by their context or entity.
- `models`: definition of all model classes. As we are using MongoDB, we can use the same JSON schema for API request/response and storage. However, different classes for the same entity are required, depending on the context:
    - `person_update.py`: model used as PATCH request body. Includes all the fields that can be updated, set as optional.
    - `person_create.py`: model used as POST request body. Includes all the fields from the Update model, but all those fields that are required on Create, must be re-declared (in type and Field value).
    - `person_read.py`: model used as GET and POST response body. Includes all the fields from the Create model, plus the person_id (which comes from the _id field in Mongo document) and the age (calculated from the date of birth, if any).
    - `person_address.py`: part of the Person model, address attribute.
    - `common.py`: definition of the common BaseModel, from which all the model classes inherit, directly or indirectly.
    - `fields.py`: definition of Fields, which are the values of the models attributes. Their main purpose is to complete the OpenAPI documentation by providing a description and examples. Fields are declared outside the classes because of the re-declaration required between Update and Create models.
    - `errors.py`: error models. They are referenced on Exception classes defined in `exceptions.py`.
- `database.py`: initialization of MongoDB client. Actually is very short as Mongo/pymongo do not require to pre-connecting to Mongo or setup the database/collection, but with other databases (like SQL-like using SQLAlchemy) this can get more complex.
- `exceptions.py`: custom exceptions, that can be translated to JSON responses the API can return to clients (mainly if a Person does not exist or already exists).
- `middlewares.py`: the Request Handler middleware catches the exceptions raised while processing requests, and tries to translate them into responses given to the clients.
- `repositories.py`: methods that interact with the Mongo database to read or write Person data. These methods are directly called from the route handlers.
- `exceptions.py`: custom exceptions raised during request processing. They have an error model associated, so OpenAPI documentation can show the error models. Also define the error message and status code returned.
- `settings.py`: load of application settings through environment variables or dotenv file, using Pydantic's BaseSettings classes.
- `utils.py`: misc helper functions.
- `tests`: acceptance+integration tests, that run directly against the API endpoints and real Mongo database.

## Requirements

- Python >= 3.7
- Requirements listed on [requirements.txt](requirements.txt)
- Running MongoDB server

## make tools

```bash
# Install requirements
make install-requirements

# Run the app (available at http://localhost:5000/...)
make run

# Install test requirements
make install-test-requirements

# Start MongoDB for tests (requires Docker)
make start-test-mongo

# Run the tests
make test
```
