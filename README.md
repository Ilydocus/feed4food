# feed4food

The following code deploys a web application that allows to input daily produce reports for registered users. 
The web app is built using Django and the data is stored in a PostgreSQL database.

## Deployment

### Prerequisites

There are several prerequisites in order to deploy the web app. 
* Make sure the following environment variables are defined in your shell:
```bash
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
DJANGO_SUPERUSER_USERNAME="admin_name"
DJANGO_SUPERUSER_PASSWORD="admin_password"
DJANGO_SUPERUSER_EMAIL="admin_email"
```
* Make sure that no application is running on port 8000 and 5432 (PostgreSQL default port).
* Git is installed on your machine and you pulled the repository: 
```bash
git clone git@github.com:Ilydocus/feed4food.git
```


There are several ways to deploy the web application: Docker and local deployment.
In this README, I will only cover the Docker deployment.

### Docker deployment

Using Docker is the easiest way to deploy the web app.
Firstly, make sure you have Docker installed on your machine.
Then inside the repository, run the following command:
```bash
sudo docker compose up --build
```

This will build the Docker images for PostgreSQL and Django, and run their respective containers.
The server will be running on http://127.0.0.1:8000/ by default with PostgreSQL running on port 5432.

### Possible troubleshooting 
- Sometimes there are can be issues with database migrations.
To fix this, run the following commands:
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 
find . -path "*/migrations/*.pyc"  -delete
```

## Admin Panel

To access the admin panel, go to http://127.0.0.1.:8000/admin and log in with the superuser credentials.
Here, you can create new users and add new produce items to the database.
For example, select "+Add" next to "item names" and add a couple of few itmes, like "Apples" and Potatoes". 

## Produce Form

From the home directory of the website, the user can select "Fill out daily produce report". 
Here, the user selects the date range for the report, and then selects "Add Item" which will opem up a dropdown menu with the items added to the database ("Apples" and "Potatoes").
Once selected, additional information can be added, such as the quantity. 
Once done, click "submit" and the report will be saved in the database. 