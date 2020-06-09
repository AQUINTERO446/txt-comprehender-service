import os
import sys
import signal
import connexion
import urllib.request
import tempfile
import boto3
import json

# Setup handler to catch SIGTERM from Docker
def sigterm_handler(_signo, _stack_frame):
    print('Sigterm caught - closing down')
    sys.exit()

# Health function
def health():
    return 'OK', 200

def comprehend(text):
    detection = {}
    lang = comprehend_resource.detect_dominant_language(Text = text)
    entities = comprehend_resource.detect_entities(Text=text, LanguageCode=lang['Languages'][0]['LanguageCode'])
    sentiment = comprehend_resource.detect_sentiment(Text=text, LanguageCode=lang['Languages'][0]['LanguageCode'])
    detection['Languages'] = lang['Languages']
    detection['Entities'] = entities['Entities']
    detection['Sentiment'] = {
        'SentimentScore': sentiment['SentimentScore'],
        'Sentiment': sentiment['Sentiment']
    }


    # return {
    #     "dominant_lang": comprehend_resource.detect_dominant_language(Text = txt)
    # }, 200
    return detection, 200

def get_job_results(job_id):
    return {'status': 'Working on it'}, 200


def comprehend_from_url(text):
    try:
        res = comprehend(text)
    except:
        return 'Error in comprehend', 500
    return res

def comprehend_from_file():
    try:
        uploaded_file = connexion.request.files['txt_file']
        # Use mkstemp to generate unique temporary filename
        fd, txt_file = tempfile.mkstemp(".txt")
        uploaded_file.save(txt_file)
        file_obj = open(txt_file, 'r')
        data = file_obj.read()
        file_obj.close()
        os.close(fd)

    except:
        return 'Error in getting/reading file', 500
    try:
        res = comprehend(data)
        os.unlink(txt_file)
    except Exception as err:
        print("Unexpected error:", err)
        return 'Error in comprehend', 500
    return res


def comprehend_whatsapp_conversation(wp_file):
    return {'status': 'Working on it'}, 200


# Setup AWS credentials 
comprehend_resource = boto3.client(
    'comprehend',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
    region_name=os.environ.get('AWS_REGION')
)

# Create API:
app = connexion.App(__name__)
app.add_api('swagger.yaml')

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    app.run(debug=True, port=80, server='gevent')


