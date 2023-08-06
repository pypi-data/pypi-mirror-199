# Trail

Trail is a Python package that makes it easier to bring transparency to your machine learning (ML) experimentation process. It helps you keep track of your experiments, so you can better understand how your models are performing and communicate that information to your team and stakeholders.

## Prerequisites

Before you can use Trail, you'll need to sign up for a user account on the Trail-ML homepage (see Project-Links). Once you've signed up, you can start using MLflow to track your experiments. You'll need your email and password to use Trail, as well as your project ID and parent values, which you can find in the Trail web app.

## Installation

Install Trail from Pypi via 
```python 
pip install traildb
```

## Get started

```python 
from traildb import trail_init
```

## log experiment

Logging experiments is as easy as including one line of code. You'll get the parameters email and password at signup and see the project_id and parent values in the web app. <br />

<br />

```python
with mlflow.start_run() as run:
    with trail_init(email, password, project_id, parent):
      ...your training code...
```

This will start a new MLflow run and initialize a Trail experiment for that run, using the provided email, password, project ID, and parent values. You can then use the MLflow tracking API to log metrics, parameters, and artifacts for that run, and Trail will automatically record this information as part of the experiment.

By using Trail to track your ML experiments, you can gain greater transparency into your development process and better communicate your results to your team and stakeholders.