import json
import mlflow
from mlflow.tracking import MlflowClient
import pyrebase
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import configparser
import os

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(
    __file__), 'endpoints.ini')


with open(config_path) as f:
    config.read_file(f)


class trail_init:
    GQL_ENDPOINT_CONFIG_SECTION = "GQL_ENDPOINT"
    GQL_ENDPOINT_URL_FIELD = "url"

    FIREBASE_CONFIG = {
        "apiKey": "AIzaSyDBbIiCyAFkz_bZQb0hbP5wFB-ioF6xOyw",
        "authDomain": "trail-ml-9e15e.firebaseapp.com",
        "databaseURL": "THIS_IS_NOT_USED",
        "storageBucket": "THIS_IS_NOT_USED",
    }

    MUTATION = """
                mutation (
                    $projectId: String!,
                    $parentExperimentId: String!,
                    $title: String!, $comments: String!,
                    $instanceRunParameters: JSONString!,
                    $instanceRunMetrics: JSONString!
                    ) {
                        addExperiment(
                        projectId: $projectId,
                        parentExperimentId: $parentExperimentId,
                        title: $title,
                        comments: $comments,
                        instanceRuns: {
                            comment: "",
                            parameters: $instanceRunParameters,
                            metrics: $instanceRunMetrics
                        }
                    ) {
                        experiment {
                            id
                            title
                            comments
                            instanceRuns {
                            id
                            comment
                            parameters
                            metrics
                            }
                        }
                    }
                }
                """

    def __init__(self, username, password, project_id, parent, title=None):
        token = self._retrieve_jwt_token(username, password)
        transport = AIOHTTPTransport(url=config.get(trail_init.GQL_ENDPOINT_CONFIG_SECTION,
                                                    trail_init.GQL_ENDPOINT_URL_FIELD),
                                     headers={"authorization": f"Bearer {token}"})
        self.client = Client(transport=transport)
        self.project_id = project_id
        self.parent = parent
        self.title = title if title else "Unnamed Run"

    def __enter__(self):
        if (mlflow.active_run() is None):
            raise (Exception("No active mlflow run found"))

    def __exit__(self, type, value, traceback):
        run = mlflow.active_run()
        if (run):
            self.log_experiment(mlflow.get_run(run_id=run.info.run_id))

    def log_experiment(self, mlflowrun):
        tags = {k: v for k, v in mlflowrun.data.tags.items()
                if not k.startswith("mlflow.")}
        artifacts = [f.path for f in MlflowClient().list_artifacts(
            mlflowrun.info.run_id, "model")]
        d = {}
        d['run_id'] = mlflowrun.info.run_id
        d['time_stamp'] = mlflowrun.info.start_time / 1000.0
        d['user'] = mlflowrun.info.user_id
        d['artifacts'] = artifacts
        d['tags'] = tags

        self.client.execute(gql(self.MUTATION), {
            'projectId': self.project_id,
            'parentExperimentId': self.parent,
            'title': self.title,
            'comments': "",
            'instanceRunParameters': json.dumps(mlflowrun.data.params),
            'instanceRunMetrics': json.dumps(mlflowrun.data.metrics)
        })

    def _retrieve_jwt_token(self, email, password):
        firebase = pyrebase.initialize_app(self.FIREBASE_CONFIG)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        return user['idToken']

    def get_run_info(self):
        pass
