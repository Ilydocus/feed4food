# feed4food

The following code deploys a web that allows to input daily produce reports for registered users. 
The web app is built using Django and the data is stored in a SQLite database.

## Local deploymennt 

To deploy the web app locally, follow the steps below:

0. Prerequisites:
    - Python 3.8 or higher
    - Git
    - A terminal
    - Google Maps API key
        - Store it in environment variable `GOOGLE_MAPS_API_KEY`:
        ```bash
        export GOOGLE_MAPS_API_KEY="your_api_key"
        ```
    - SpatialLite to handle spatial SQL data for [GeoDjango](https://docs.djangoproject.com/en/5.1/ref/contrib/gis/install/spatialite/#installing-spatialite)
        - On Ubuntu, run the following command:
        ```bash
        sudo apt-get install libsqlite3-mod-spatialite gdal-bin
        ```
    - [Optional] If you had a previous version of the project, you may need to delete the `src/db.sqlite3` file to avoid conflicts. 
    Run the following command:
    ```bash
    rm src/db.sqlite3 -f
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 
    find . -path "*/migrations/*.pyc"  -delete
    ```

1. Install [pixi](https://pixi.sh/dev/):

    Pixi is a snappier replacement to conda/mamba. 
    It is an easy-to-use tool that simplifies making virtual environments for python projects. 

    On linux/macOS, run the following command:
    ```bash
    curl -fsSL https://pixi.sh/install.sh | bash
    ```
    On windows, in powershell:
    ```powershell
    iwr -useb https://pixi.sh/install.ps1 | iex
    ```

2. Clone the repository:
    ```bash
    git clone git@github.com:Ilydocus/feed4food.git
    ```

3. Initialize the virtual environment:
    ```bash
    pixi init
    pixi install
    ```
    make sure to run these commands **inside the repository**

4. Initialize the database:
    Firstly, go into the `src` directory:
    ```bash
    cd src
    ```
    Then, run the following commands:

    ```bash
    pixi run python manage.py makemigrations
    pixi run python manage.py migration
    ```
    That will create the database file `db.sqlite3` which will store all application data.

5. Create superuser:
    ```bash
    pixi run python manage.py createsuperuser
    ```
    This will allow you to access the admin panel with the superuser credentials.

6. Run the server:
    ```bash
    pixi run python manage.py runserver
    ```
    The server will be running on http://127.0.0.1:8000/ by default. 

## Admin Panel

To access the admin panel, go to http://127.0.0.1.:8000/admin and log in with the superuser credentials.
Here, you can create new users and add new produce items to the database.
For example, select "+Add" next to "item names" and add a couple of few itmes, like "Apples" and Potatoes". 

## Produce Form

From the home directory of the website, the user can select "Fill out daily produce report". 
Here, the user selects the date range for the report, and then selects "Add Item" which will opem up a dropdown menu with the items added to the database ("Apples" and "Potatoes").
Once selected, additional information can be added, such as the quantity and the type. 
Once done, click "submit" and the report will be saved in the database. 
You can see them by directly querying the database in `/src/db.sqlite3`. 
