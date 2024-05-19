# ALNM_Baheya Project

ALNM_Baheya is an AI-driven application designed to predict Axillary Lymph Node Metastasis based on patient data provided by doctors. This application not only predicts metastasis but also incorporates feedback from doctors on the ground truth of predictions to continually retrain and enhance the model's accuracy.

## Prerequisites

Ensure you have Python installed on your machine. Python 3.8 or later is recommended. You can download it from [python.org](https://www.python.org/downloads/).

## Setup Instructions

#### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/omarelnsary/ALNM_Baheya
cd ALNM_Baheya
```

### 2. Create and activate a virtual environment

#### For Windows:

```cmd
python -m venv ALNM_BAHEYA_env
ALNM_BAHEYA_env\Scripts\activate.bat
```

#### For macOS:

```bash
python3 -m venv ALNM_BAHEYA_env
source ALNM_BAHEYA_env/bin/activate.bat
```

#### Check the environment

run this command this sould return the "ALNM_BAHEYA_env" path

```bash
echo $VIRTUAL_ENV
```

### 3. Install required packages

#### Install all the necessary packages using the following command:

```bash
pip install -r ALNM_BAHEYA\\requirements.txt
```

### 4. Install PostgreSQL: If it's not already installed, you can install PostgreSQL on Ubuntu by running:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```
#### 1. Start the PostgreSQL Service: Make sure the PostgreSQL service is running:

```bash
sudo service postgresql start
```
#### 2. Switch to the PostgreSQL User: PostgreSQL creates a user named postgres by default for handling the database tasks. Switch to this user:

```bash
sudo -i -u postgres
```
##### [sudo] password for vboxuser: 
##### postgres@Ubuntu:~$

#### Open the PostgreSQL Command Line Interface (psql): Once you're the postgres user, you can open the PostgreSQL command line interface by typing:

```bash
psql
```
### 5. Run migrations

#### Check the django:

```bash
python manage.py check
```

#### Initialize the database and prepare it for use by running:

```bash
python manage.py migrate
```

### Using the Application

#### To start the application, run:

```bash
python manage.py runserver
```
