# django_account_administration

**Bank account administration system for Django**
This is a small Django application to manage (CRUD) users and their bank account data (IBAN).

There are two main model and one simple logic. 

 - Django's `User` model from  `django.contrib.auth`
	 - The term **user** is basically stands for the administrators who can login the system and do managing operations. 
	- They can add/delete `Account` to the system and can edit them. 
Administrator's actions restricted with manipulation operations on a user to the **administrator who created them.** 
	- Superuser (root) can delete or update any Account instance without the restriction specified above.
	- Users/Administrators can login the system using their Google accounts besides the origin admin login. ( [social_auth_app_django](http://python-social-auth.readthedocs.io/en/latest/configuration/django.html) library used )
	
 - `Account` model 
	 - Three field is required. `first_name` of the account owner, `last_name` of the account owner and the `IBAN` no of the account.
	 - For the IBAN field, [Django's localflavor](https://github.com/django/django-localflavor)'s `IBANField` has been used so that IBAN Validation and related controls handled by the third party library.
	 
**NOTE:**  Administrators can not delete accounts using `delete_selected` admin action either. Except the root user (superuser)

**TIP:** While playing around on this project, you can use [random IBAN generator](http://randomiban.com/). 



## How to run and use the project
Before running the project, be sure that you have [Docker](https://www.docker.com/get-docker) installed on your system. 

Open the terminal on your computer and cd to project root.
	
	source tools/dev.sh

This will use  `docker-compose.yml`  and  `Dockerfile`  to setup a development environment complete with all the needed services. The first time the process might take a few minutes, after that Docker will use its cache to speed up things.

You should be bashed into the container where django app lives.
If you are doing this for the first time run the followings.

-   `python manage.py migrate`  (This might raise an error. Wait a few seconds for database to be ready. Then run it again.)
-   `python manage.py createsuperuser`

After these, you can run 
	
	python manage.py runserver 0:8000
to run the server. 
**Now you can reach the app from your host machine at  [http://localhost:8000](http://localhost:8000/)**

**NOTE:** You should use 'localhost' instead of '127.0.0.1' or any other variations of localhost. Although they should land on the same page, the usage of Google API will give you an error.
   
### Testing

-   Bash into the container where django app runs.
-   run  `python manage.py test --settings=account_administration.settings.test`

