# Journaling Therapy

## what is journaling therapy
    Journaling Therapy is an online ecommerce site that deals with wellness items that is journals, affirmation cards and other kinds of gifts.
    The website is written in Django, users have the ability to create accounts to retain information and for repeat buys but one can also make purchases as a guest. The project is responsive making it viewable on different viewports. The project also has javascript for dom manipulations and for validations.


## Setup and installation

   The unsaid part is ofcourse you hhave to clone this repo and **cd** into it only then you can start working following the steps below.

1. Set up virtualenv

   ```bash
        virtualenv venv
   ```

2. Activate virtualenv 

   ```bash
      LINUX/MAC

      . venv/bin/activate

      WINDOWS

      . venv/scripts/activate
      
   ```

3. Install dependencies

   ```bash
        pip install -r requirements.txt
   ```

4. Database configuration.

   The project uses PostgreSQL to persist data and if you wish to use the same you can [get it here](https://www.postgresql.org/download/), also when installing Postgresql install PgAdmin, it is really going to come in handy in managing your databases.

   Once you have successfully installed create **journaling**. After creating the database create a **.env** file

   ## .env file example

  Create the **env** file in the root of your project and place the following settings in the file and others that you might want to add to the file.

   ```bash
      DEBUG = on
      SECRET_KEY = "yoursecretkey"
      SENDGRID_KEY = "sendgrid api key to assit in sending emails"
      DATABASE_URL = "postgres://postgres:{your postgres password}@localhost/journaling"
   ```

   Once you are done with the **.env** file then you can run the below command to prepare the database for use, if for some reason the **makemigrations** command does not work or returns **no changes detected**
   just run the command with apps flags -> python manage.py makemigrations app1 app2 app3 and so on the app1 and app2 are names of the apps in the project.

   ```bash
      python manage.py makemigrations

      python manage.py migrate
   ```

5. Start the server

   ```bash
      python manage.py runserver
   ```

<details open>

Incase of a bug or anything else use any on the below channels to reach me

[Find me on twitter](https://twitter.com/kabakikiarie) OR  drop me an email at kabaki.antony@gmail.com.
