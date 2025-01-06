# Project Structure

The `/src` folder contains the main codebase for the Django project. 
Below is an overview of the basic Django project structure and the purpose of each application folder within the directory.

## Basic Django Project Structure

- **manage.py**: A command-line utility that lets you interact with this Django project in various ways.
Run `python manage.py help` for a list of available commands.
- **/core/**: The directory containing global website settings, URLs, and WSGI configuration.
    - **__init__.py**: An empty file that tells Python that this directory should be considered a Python package.
    - **settings.py**: Contains all the settings and configuration for the Django project.
    - **urls.py**: The URL declarations for this Django project; a "table of contents" of your Django-powered site.
    - **wsgi.py**: An entry-point for WSGI-compatible web servers to serve your project.

## Application Folders

### Basic Structure

Each application folder within the `/src` directory represents a distinct component of the project, encapsulating related functionality.

- **/app_name/**: Each application directory typically contains the following files:
    - **migrations/**: A directory that stores database migration files.
    - **__init__.py**: An empty file that tells Python that this directory should be considered a Python package.
    - **admin.py**: Configuration for the Django admin interface.
    - **apps.py**: Configuration for the application itself.
    - **models.py**: Contains the data models for the application.
    - **tests.py**: Contains test cases for the application.
    - **views.py**: Contains the view functions or classes that handle requests and return responses.
    - **urls.py** (optional): URL declarations specific to this application.
    - **forms.py** (optional): Contains form classes for the application.
    - **templates/** (optional): A directory for HTML templates.
    - **static/** (optional): A directory for static files (CSS, JavaScript, images).

By organizing the project in this way, each application can be developed, tested, and maintained independently, promoting modularity and reusability.
Each application must be registered in the `INSTALLED_APPS` list within the `settings.py` file to be recognized by the Django project.

### List of Applications

- **/accounts/**: Contains user authentication and account management functionality. 
- **/dashboard/**: Contains functionality related to the user data dashboard.
- **/report/**: Contains functionality related to generating reports.
- **/report_view/**: Contains functionality related to viewing reports for users and editing them.

In addition, the `/static` and `/templates` directories within the `/src` folder contain static files and templates shared across multiple applications.