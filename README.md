# Fly Airtech

Airtech is an airline that has had challenges with using spreadsheets to manage their flight booking system. 
They are ready to automate their processes with an application and so I have set out to build a flight booking 
application for the company.

## Installation

1.  Ensure you have Python installed in your system

2.  If you do not have virtualenv or virtualenvwrapper, install virtualenv which is a tool
that lets you create an isolated Python environment for your project
```commandline
pip install virtualenv
```

3. Clone this repository from Github
```
git clone git@github.com:ignatiusukwuoma/airtech.git
```

4. Navigate into the project directory
```commandline
cd airtech
```

5. Create a virtual environment and activate it

```commandline
virtualenv venv
source venv/bin/activate
```
Replace _venv_ with your desired virtualenv name. 
You should see a (venv) appear at the beginning of your terminal prompt indicating that you are working 
inside the virtualenv.



6. Install the required packages
```commandline
pip install requirements.txt 
```

7. Create a `.env` file in the root directory with the content of the `.env.sample` and edit with your personal details.

## Starting the app

To run this application on your local computer, follow the instructions in Installation above and run

```commandline
python manage.py runserver
```

## Stopping the app

To stop the application at any time, hit `Ctrl (or Cmd) + C`