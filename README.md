# python-rest-api
Django Rest API für Übersetzung von HTML/plain-text Inhalten

### Prerequisites
Ensure Docker and Docker Compose are installed on your system.

### Clone the Repo
1. Open a terminal.
2. Clone the repository:
    ```
    git clone <repo-url>
    ```
3. Navigate to the cloned repository:
    ```
    cd <repo-name>
    ```

### Start the Project
Build the container and install dependencies:
```
docker-compose build
```

Start Docker containers:
```
docker-compose up -d
```

### Run Tests
Execute tests with:
```
docker-compose run --rm app sh -c "python manage.py test"
```

### Create Superuser
Create a superuser with:
```
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
Follow the prompts to set the username and password for the superuser.

Access the project by entering `localhost:8000` in your web browser.

### Use the Translation API

#### Activate DeepL API with your key
add a file with your Key for the DeepL REST API to a file at '/app/app/config.py'
the file should look like this:
```
DEEPL_AUTH_KEY = "your-api-key"
```
#### API Documentation
There is a Swagger API Documentation at
'http://localhost:8000/api/docs/'
In short, the Translations can be passed and retrieved here:
'http://localhost:8000/admin/core/translation/'
The User API you'll find here:
'http://localhost:8000/admin/core/user/'

Happy translating! :sparkles: :fireworks: