# BandSnap
## Local setup
First, ensure that Python 3.10 is installed on your machine.
  
Next, clone the repository:
```
git clone https://github.com/paulrtanderson/wad_group_project_bandsnap.git
```
To create the Conda environment, run:
```
conda create -n bandsnap python=3.10
```
Then, to setup the environment:
```
cd wad_group_project_bandsnap
conda activate bandsnap
pip install -r requirements.txt
```

Wait until the environment is setup. Next, to create the database, run:
```
python manage.py makemigrations
python manage.py migrate
python population_script.py
python manage.py collectstatic
```
Finally, to run the server, run:
```
python manage.py runserver
```

# Pythonanywhere
The project can also be accessed on PythonAnywhere at the following URL:  
<https://bandsnap.eu.pythonanywhere.com/>