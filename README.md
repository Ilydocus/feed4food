# feed4food

The following code deploys a web application that allows to input daily produce reports for registered users. 
The web app is built using Django and the data is stored in a PostgreSQL database.

## File description

- `/src`: Source Django files used to create and deploy the website.
- `/docker-compose`: Folder that houses all-in-one docker deployment for the whole application. 
- `Dockerfile`: Container definition for a standalone Django app environment (without database and other features).
- `pixi.toml`: Pixi file which describes the minimal Django environment.
- `pixi.lock`: Pixi lock file.

## Deployment

### Prerequisites

There are several prerequisites in order to deploy the web app. 
* Make sure the following environment variables are defined in your shell or through a `.env` file:
```bash
POSTGRES_DB=db_name
POSTGRES_USER=db_user
POSTGRES_PASSWORD=db_password
DJANGO_SUPERUSER_USERNAME=admin_name
DJANGO_SUPERUSER_PASSWORD=admin_password
DJANGO_SUPERUSER_EMAIL=admin_email
GF_SECURITY_ADMIN_PASSWORD=grafana_password
```
* (Optional) If deploying Django app outside Docker, make sure to also define the database environment variable:
```bash
export DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
```
* Make sure that **no** application is running on ports:
    * 3000 Grafana
    * 5432 PostgreSQL
    * 8000 Django App 
    * 8080 Scaphandre power monitor tool
    * 9090 Prometheus
    * 9100 Prometheus node exporte
* Git is installed on your machine and you pulled the repository: 
```bash
git clone git@github.com:Ilydocus/feed4food.git
```


There are several ways to deploy the web application: Docker and local deployment.
In this README, I will only cover the Docker deployment.

### Docker deployment

The web app is composed of several services, so it is best to deploy it using Docker.
Firstly, make sure you have Docker installed on your machine.
Then inside the repository, go to the `docker-compose` folder and build up the docker containers:
```bash
cd docker-compose
sudo docker compose up --build
```
give it around 20-40 secons to build all of the containers.
The Docker containers built are for PostgreSQL, Django, Grafana, Prometheus and its corresponding data exporters.
The Django server will be running on http://127.0.0.1:8000/ by default with PostgreSQL running on port 5432.
Postgres data will be saved in the `/db_data` folder on the root of the repository.
A prometheus server will be running on http://127.0.0.1:9090/
Similarly, Prometheus data will be saved in the `/prometheus` folder on the root of the repository.
and Grafana will be running on http://127.0.0.1.:3000/.

### Possible troubleshooting 
- Sometimes there are can be issues with database migrations.
To fix this, run the following commands **within `/src`** folder:
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