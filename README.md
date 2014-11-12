# ROBOCHECKER

App created for the MISTIC Master of Computer Security given at UOC (Open University of Catalonia).

Its main goal is to check for the existence of the resources stated as 'Disallow' in a robots.txt file.

Its usage is as follows:

```
cd src/
python robochecker <my_url>
```

## REQUIREMENTS

- Python 3 (tested with Python 3.4.1, will not work with Python 2.X.x)
- requests third-party library

It is advised to use some kind of environment virtualization such as virtualenv and virtualenvwrapper for management easiness.

Once inside the virtual enviroment run

```
pip install -r requirements.txt
```

And all the requirements will get installed so they won't mess up with your system.
