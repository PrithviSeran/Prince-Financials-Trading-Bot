

import sys
sys.path.insert(0, '/Users/prithviseran/Documents/Forex_Trading_Bot_Server/google_modules')
import requests
import pandas as pd
import numpy as np
import requests
import google_defs
import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_modules.auth.transport.requests import Request
from google_modules.oauth2.credentials import Credentials
import python_terraform
import shutil

#content of the 'defs.py' file
defs_file = ['# Taken from bluefeversoft\n',
            'API_KEY = "82327cb1b2120c2d6dce7f9f3c2ba5aa-831f9214a592b4e7ed8f1533d17f7b07"\n',
            "OANDA_URL = 'https://api-fxpractice.oanda.com/v3'\n",
            '\n',
            'SECURE_HEADER = {\n',
            "    'Authorization': f'Bearer {API_KEY}',\n",
            "    'Content-Type': 'application/json'\n", '}\n',
            '\n',
            "HOLIDAYS = ['01/01', '15/01', '29/03', '31/03', '01/05', '04/07', '25/12']\n",
            '\n',
            "ORDERCANCELLATION = 'orderCancelTransaction'\n"]


class Google_API:
    """
    Class for interacting with various Google APIs.
    """

    def __init__(self, project_id, topic_id, location, bucket, terraform_path):
        """
        Initializes the Google API object with session and configuration parameters.

        Parameters:
        - project_id (str): Google Cloud Project ID.
        - topic_id (str): Google Cloud Pub/Sub Topic ID.
        - location (str): Google Cloud region.
        - bucket (str): Google Cloud Storage bucket name.
        - terraform_path (str): Path to Terraform configurations.
        """

        self.session = requests.Session()
        self.project_id = project_id
        self.topic_id = topic_id
        self.location = location
        self.bucket = bucket
        self.t = python_terraform.Terraform(working_dir=terraform_path)


    def create_credentials(self):
        """
        Creates and retrieves Google API credentials.

        If credentials do not exist or are expired, it prompts the user to authorize.

        Returns:
        - Credentials: Google API credentials.
        """

        creds = None
        if os.path.exists('/Users/prithviseran/Documents/Forex_Trading_Bot_Server/token.json'):
            print(True)
            creds = Credentials.from_authorized_user_file(
                '/Users/prithviseran/Documents/Forex_Trading_Bot_Server/token.json',
                defs.SCOPES
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(defs.CLIENT_FILE, defs.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('/Users/prithviseran/Documents/Forex_Trading_Bot_Server/token.json', 'w') as token:
                token.write(creds.to_json())

        self.credentials = creds


    def create_API_reaquest(self, api_name, version):
        """
        Creates an API request for a specific Google API.

        Parameters:
        - api_name (str): Name of the Google API.
        - version (str): Version of the Google API.

        Returns:
        - Resource: Google API resource.
        """
        return build(api_name, version, credentials=self.credentials)


    def create_pubsub(self, body={}):
        """
        Creates a Pub/Sub topic using the Google Pub/Sub API.

        Parameters:
        - body (dict): Request body for creating the Pub/Sub topic.

        Returns:
        - dict: Result of the Pub/Sub topic creation.
        """

        service_pubsub = self.create_API_reaquest('pubsub', 'v1')

        result = service_pubsub.projects().topics().create(
            name=f"projects/{self.project_id}/topics/{self.topic_id}",
            body=body
        ).execute()

        return result


    def create_scheduler(self, job_payload):
        """
        Creates a Cloud Scheduler job using the Google Cloud Scheduler API.

        Parameters:
        - job_payload (dict): Request body for creating the Cloud Scheduler job.

        Returns:
        - dict: Result of the Cloud Scheduler job creation.
        """

        service_schedule = self.create_API_reaquest('cloudscheduler', 'v1')

        result = service_schedule.projects().locations().jobs().create(
            parent=f"projects/{self.project_id}/locations/{self.location}",
            body=job_payload
        ).execute()

        return result


    def pause_scheduler(self, name):
        """
        Pauses a Cloud Scheduler job using the Google Cloud Scheduler API.

        Parameters:
        - name (str): Name of the Cloud Scheduler job.

        Returns:
        - dict: Result of pausing the Cloud Scheduler job.
        """

        service_schedule = self.create_API_reaquest('cloudscheduler', 'v1')

        result = service_schedule.projects().locations().jobs().pause(
            name=f"projects/{self.project_id}/locations/{self.location}/jobs/" + name
        ).execute()

        return result


    def create_function(self, job_payload, version):
        """
        Creates a Cloud Function using the Google Cloud Functions API.

        Parameters:
        - job_payload (dict): Request body for creating the Cloud Function.
        - version (str): Version of the Cloud Functions API.

        Returns:
        - dict: Result of the Cloud Function creation.
        """

        service_function = self.create_API_reaquest('cloudfunctions', version)

        result = service_function.projects().locations().functions().create(
            location=f"projects/{self.project_id}/locations/{self.location}",
            body=job_payload
        ).execute()

        return result


    def create_storage_object(self, tf_main_path):
        """
        Creates a storage object using Terraform configurations.

        Parameters:
        - tf_main_path (str): Path to the main Terraform configuration file.

        Returns:
        - dict: Result of applying the Terraform configurations.
        """

        terraform_import_file = ['resource "google_storage_bucket" "buffer" {\n',
                                 f'   name = "{self.bucket}"\n',
                                 '   location = "US"\n',
                                 '}\n',
                                 '\n',
                                 'resource "google_storage_bucket_object" "static_site_src"{\n',
                                 '    name = "Trading_Bot.zip"\n',
                                 '    source = "/Users/prithviseran/Documents/Forex_Trading_Bot_Server/Trading_Bot.zip"\n',
                                 '    bucket = google_storage_bucket.buffer.name\n',
                                 '}\n']

        f = open(tf_main_path, 'w')

        for line in terraform_import_file:
            f.write(f"{line}")

        f.close()

        self.t.init()

        result = self.t.apply(skip_plan=True)

        return result
    

def make_defs_to_import(path_to_file, account_id):
    """
    Add the user's Oanda Account ID to defs.py file.

    Parameters:
    - path_to_file (str): The path to the file where definitions will be written.
    - account_id (str): The account ID to be written to the file.
    """

    f = open(path_to_file, 'w')

    for line in defs_file:
        f.write(f"{line}")

    f.write(f"ACCOUNT_ID = '{account_id}'")

    f.close()


def make_zip_store(path_to_folder, zip_name):
    """
    Creates a zip archive of the contents of a folder.

    Parameters:
    - path_to_folder (str): The path to the folder to be archived.
    - zip_name (str): The name of the resulting zip archive.
    """

    shutil.make_archive(zip_name, 'zip', path_to_folder)


def main(username):
    # Define names for bucket, topic, and schedule job based on the username
    bucket_name = "Prince-Trading-Bucket-" + username
    topic_name = "Prince-Trading-Topic-" + username
    job_id = "Prince-Trading-Schedule-" + username

    # Create definitions file and set Oanda account ID
    make_defs_to_import(""" defs.py absolute path """, """ Oanda Account ID """)

    # Create a zip archive of the folder containing files to be imported
    make_zip_store(
        """ Absolute path of the folder containing all the files to be imported """,
        """ Absolute path of the zipped file of the folder """
    )

    # Create an instance of the Google_API class with project-specific parameters
    google_api_object = Google_API(
        project_id="Your-Google-Cloud-Project-ID-Here",
        topic_id=topic_name,
        location="us-central1",
        bucket=bucket_name,
        terraform_path=""" Absolute path of all the Terraform files """
    )

    # Create credentials and Pub/Sub topic using the Google API object
    google_api_object.create_credentials()
    google_api_object.create_pubsub()

    # Create a Cloud Scheduler job using the Google API object
    google_api_object.create_scheduler({
        "name": "projects/testingpythonclouddep/locations/us-central1/jobs/job_id",
        "schedule": '0 * * * 1-5',
        "pubsubTarget": {
            "topicName": f'projects/testingpythonclouddep/topics/{google_api_object.topic_id}',
            "attributes": {
                "test": "Why?"
            }
        }
    })

    # Create a storage object using Terraform configurations
    storage_result = google_api_object.create_storage_object( """ Absolute path of the main.tf file """ )

    # Create a Cloud Function using the Google API object
    function_result = google_api_object.create_function({
        "name": f"projects/{google_api_object.project_id}/locations/{google_api_object.location}/functions/" + username,
        "entryPoint": "princetrading",
        "runtime": "python311",
        "eventTrigger": {
            "eventType": "google.pubsub.topic.publish",
            "resource": f"projects/{google_api_object.project_id}/topics/{google_api_object.topic_id}"
        },
        "sourceArchiveUrl": f"gs://{google_api_object.bucket}/Trading_Bot.zip"
    }, "v1")

    # Pause the Cloud Scheduler job using the Google API object
    google_api_object.pause_scheduler(name=job_id)

    # Return a success message
    return "Bot Has Been Deployed!"


if __name__ == "__main__":

    main()