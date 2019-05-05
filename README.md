# Amazing Catalog Project
This is the source code for the **Amazing Catalog** system.
In this version of the system, everyone can access the catalog contents, but only registered users can add categories and items. Each user can only edit and delete items created by them.

## Project Structure
```
|-- catalog                         // The catalog system source code
    |-- database                    // Database configuration files
        |-- query.py                // Functions to perform CRUD operations on the database
        |-- entities                // ORM entities
            |-- user.py             // User entity representation
            |-- category.py         // Category entity representation
            |-- item.py             // Item entity representation
            |-- base.py             // Base class for all entities
    |-- helpers
        |-- utils.py                // Utility functions
    |-- static                      // CSS, Scripts, images to be used on front-end
    |-- templates                   // front-end templates
    |-- catalog_app.py              // Application end-points implementation
    |-- google_client_secret.json   // Credentials to access google oauth service
    |-- populate_db.py              // Creates Dummy data on the database to test the system
|-- project_config.sh               // Installs the project dependencies.
|-- Vagrantfile                     // Vagrant script configuration file
|-- README.md
```

## Requirements
This project runs on a Vitual Box Machine managed with Vagrant. Please, make sure you have both Virtual Box and Vagrant installed before proceeding with the project installation:
* [Virtual Box](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

## Database
This section presents the Amazing Catalog database **tables structure**, each table is mapped to a ORM entity on the project:

### User

| Column        | Type           | Description  |
| ------------- |:-------------:| -----|
| id      | integer | The user id |
| username      | varchar (250)      |   The user email address |
| password_hash | varchar (64)      |    A hash value for the user's password |
| name | varchar (250)      |    The user's full name |
| picture | varchar (250)      |    A link to the user's picture |
| updated_at | datetime      |    The date when the user information was updated |
| created_at | datetime      |    The date when the user information was created |

### Category

| Column        | Type           | Description  |
| ------------- |:-------------:| -----|
| id      | integer | The category id |
| name      | varchar (80) | The category name |
| description      | text | The category description |
| updated_at | datetime      |    The date when the user information was updated |
| created_at | datetime      |    The date when the user information was created |

### Item
| Column        | Type           | Description  |
| ------------- |:-------------:| -----|
| id      | integer | The item id |
| name      | varchar (80) | The item name |
| description      | text | The item description |
| user_id      | integer | A foreign key to the id of the user that created the item |
| category_id      | integer | A foreign key to the id of the item category |
| updated_at | datetime      |    The date when the user information was updated |
| created_at | datetime      |    The date when the user information was created |

## Installation
1) Please **clone** the project's repository running the following command on a **terminal**:
```
git clone https://github.com/thiagothalison1/amazing-catalog-project.git
```
2) Setup Virtual Machine:
```
cd amazing-catalog-project
vagrant up
vagrant ssh
cd /vagrant/
./project_config.sh
```
**Note**: The vagrant up command may take a while to execute because it will download a linux distribution to be run on Virtual Box. Also, the project_config.sh script will install all the necessary dependencies to run the project.

3) Create the **catalog.db** database with some initial data:

* Open a terminal connected with the VM (if you have already run in step 2, it will not be necessary):
```
vagrant ssh
```
* Change to the project directory:
```
cd /vagrant/catalog
python populate_db.py
```

## Execution
1) To execute the project, please run the following command on a terminal:
```
cd /vagrant/catalog
python catalog_app.py
```

2) To access the project, please open your browser and type: http://localhost:5000

## License
This project is distributed under [MIT License](https://opensource.org/licenses/MIT)