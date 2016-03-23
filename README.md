# ITECH-Group-Project-2016
To run the project locally, first clone the application to your local machine:

## Run Natively

```
git clone git@github.com:Alphasite/ITECH-Group-Project-2016.git
```

Then under the ITECH-Group-Project-2016 directory, create a directory called 'data':

```
cd ITECH-Group-Project-2016
mkdir data
```

Install in requirements using pip:

```
pip install -r requirements.txt
```

Run migrations from the 'prototype' directory:

```
cd prototype
python manage.py migrate
```

Then run the application under local host:

```
python manage.py runserver
```

Now try to earn money and survive the zombie apololypses!

## Run in Docker

```
git clone git@github.com:Alphasite/ITECH-Group-Project-2016.git
```

Then under the ITECH-Group-Project-2016 directory, create a directory called 'data':

```
cd ITECH-Group-Project-2016
mkdir data
```

Then build the docker-compose image.

```
docker-compose build
```

Then run it.

```
docker-compose up -d
```

