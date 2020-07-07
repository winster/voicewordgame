
https://cloud.google.com/sdk/gcloud/reference/functions/deploy




* pip install virtualenv
* virtualenv ENV
* pip install -r requirements.txt
* export FLASK_APP=main.py
* python -m flask run
*
* gcloud functions deploy df_game --entry-point=webhook --runtime=python37 --trigger-http --allow-unauthenticated --source=.

