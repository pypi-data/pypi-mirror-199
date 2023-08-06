# Trail

Trail brings more transparency in your ml experimentation and make your AI development understandable - for data science teams, product managers and business stakeholder

# Prerequisite:
To use trail, you need a user account, which you get on the trail-ml homepage  (see Project-Links).
Once your signed up you can start by using mlflow to track experiments and follow the steps below.

# Installation

Install Trail from Pypi via 
```python 
pip install traildb
```

# Get started

```python 
from traildb import trail_init
```

# log experiment

Logging experiments is as easy as including one line of code. You'll get the parameteres email and password at signup and see the project_id and parent values in the web app. <br />

<br />

```python
with mlflow.start_run() as run:
    with trail_init(email, password, project_id, parent):
      ...your training code...
```
