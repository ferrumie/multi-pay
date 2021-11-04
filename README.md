# Multi-Pay
- Checkout examples
- ![Screenshot from 2021-11-04 03-02-06](https://user-images.githubusercontent.com/57694834/140299391-f9d20684-75d6-4342-b3fe-8fea34be06f4.png)
- ![Screenshot from 2021-11-03 09-21-39](https://user-images.githubusercontent.com/57694834/140299433-b90edcb6-1bfc-48c6-869b-19ccdf60c8df.png)
- ![Screenshot from 2021-10-31 16-21-12](https://user-images.githubusercontent.com/57694834/140299470-3f97b043-0557-45df-86ba-ea3b9e1a8d03.png)




Multipay is a Payment MicroService API that links to various payment platforms to give you various range of options with just a single token id!

## Technology Stack
- Django
- Django REST Framework
- Postgres
- Stripe Payment
- Paystack API
- FlutterWave API
- Coinbase API
etc...

### Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.7.0
    ```

-   Install virtualenv or pipenv:

-   Clone the multi-pay repo and cd into it:

    ```
    git clone https://github.com/ferrumie/multi-pay.git
    ```
- Create a virtual enviroment
	```
	python3 -m venv env
	```
- Activate the virtual enviroment:
    - On Linux/Mac:
	    ```
	    source env/bin/activate
	    ```
    -  On Windows:
        ```
	   env/scripts/activate
	    ```
	Feel free to use other tools such as pipenv

-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```
- Setup up local postgres db
	```
	Download and install postgres locally
	Here is a useful guide for windows
	[Install Postgres on Windows](https://www.guru99.com/download-install-postgresql.html)

	For MacOS install the psogress app 
	[Install Postgres on Mac](https://postgresapp.com/)
	Start postgres
	Create and visualize the databse using [Postico](https://eggerapps.at/postico/)
	```
-   Make a copy of the .env.sample file in the app folder and rename it to .env and update the variables accordingly:

    ```
    SECRET_KEY=generate a random django key # https://www.miniwebtool.com/django-secret-key-generator/
    DB_NAME=dbname
    DB_USER=dbuser
    DB_PASSWORD=secretpassword

    ```


-   Apply migrations:

    ```
     run python manage.py migrate
    ```


*   Run the application with the command

    ```
    python manage.py runserver
    ```

* Once the server is running navigate to http://127.0.0.1:8000 to access the project

* Visualize local postgres db using [Postico](https://eggerapps.at/postico/) or [Pgadmin](https://www.pgadmin.org/)

###  Running Tests
*   Run all tests
    ```
    python manage.py test
    ```

*   Run a particular test script (using testuser.py inside the unit module as an example)
    ```
    python manage.py test api.tests.unit.testuser
    ```

*   Run test in a particular folder:
    ```
    python manage.py test <folder>
    ```
Check out the django documentation on [Testing](https://docs.djangoproject.com/en/3.1/topics/testing/overview/) for more information

### PhoneNumbers 
*   The phonenumber fields currently support basically all the available number prefix for all service lines internationally
    This is a list of all the available number prefix in nigeria
    ```   
        '234701':{'en': 'Airtel'},
        '2347020':{'en': 'Smile'},
        '2347021':{'en': 'Ntel'},
        '2347022':{'en': 'Ntel'},
        '2347024':{'en': 'Prestel'},
        '2347025':{'en': 'MTN'},
        '2347026':{'en': 'MTN'},
        '2347027':{'en': 'Multilinks'},
        '2347028':{'en': 'Starcomms'},
        '2347029':{'en': 'Starcomms'},
        '234703':{'en': 'MTN'},
        '234704':{'en': 'MTN'},
        '234705':{'en': 'Glo'},
        '234706':{'en': 'MTN'},
        '234708':{'en': 'Airtel'},
        '234709':{'en': 'Multilinks'},
        '234801':{'en': 'Megatech'},
        '234802':{'en': 'Airtel'},
        '234803':{'en': 'MTN'},
        '234804':{'en': 'Ntel'},
        '234805':{'en': 'Glo'},
        '234806':{'en': 'MTN'},
        '234807':{'en': 'Glo'},
        '234808':{'en': 'Airtel'},
        '234809':{'en': '9mobile'},
        '234810':{'en': 'MTN'},
        '234811':{'en': 'Glo'},
        '234812':{'en': 'Airtel'},
        '234813':{'en': 'MTN'},
        '234814':{'en': 'MTN'},
        '234815':{'en': 'Glo'},
        '234816':{'en': 'MTN'},
        '234817':{'en': '9mobile'},
        '234818':{'en': '9mobile'},
        '234819':{'en': 'Starcomms'},
        '234901':{'en': 'Airtel'},
        '234902':{'en': 'Airtel'},
        '234903':{'en': 'MTN'},
        '234904':{'en': 'Airtel'},
        '234905':{'en': 'Glo'},
        '234906':{'en': 'MTN'},
        '234907':{'en': 'Airtel'},
        '234908':{'en': '9mobile'},
        '234909':{'en': '9mobile'},
        '234912':{'en': 'Airtel'},
        '234913':{'en': 'MTN'},
        '234915':{'en': 'Glo'},
    ```

# Oh and need i say?
``` Your keys are safe with me```
