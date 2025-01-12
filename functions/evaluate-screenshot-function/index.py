import json
import boto3
import requests
import json
from lzstring import LZString

lz = LZString()

url_link = "DUMMY.cloudfront.net/channel/actions/send"
client_id = "YOUR_CLIENTID"

def pack(metadata_obj):
    json_str = json.dumps(metadata_obj)
    compressed_metadata_str = lz.compressToBase64(json_str)
    return compressed_metadata_str

def unpack(metadata_str):
    decompressed_json_str = lz.decompressFromBase64(metadata_str)
    decompressed_metadata_obj = json.loads(decompressed_json_str)
    return decompressed_metadata_obj

cognito_client = boto3.client('cognito-idp', region_name='us-west-2')

def authenticate_user(username, password):
    print("Username:", username)
    print("Password:", password)
    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            }
        )
        if 'AuthenticationResult' not in response:
            print("Response received without 'AuthenticationResult':", response)
            raise Exception("Authentication failed without an authentication result.")
       
        return response['AuthenticationResult']['AccessToken']
   
    except cognito_client.exceptions.NotAuthorizedException as e:
        raise Exception("The username or password is incorrect.") from e
    except Exception as e:
        print("Exception details:", e)
        raise Exception(f"Error authenticating user: {str(e)}")
   
def send_action(metadata, access_token):
    url = url_link
    print(url)
   
    # Prepare the headers with the JWT token for authorization
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{access_token}'  # Include the JWT token
    }
   
    # Prepare the payload
    payload = {
        "metadata": metadata
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Check if the request was successful
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print(f"Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

def lambda_handler(event, context):
    with open('env', 'r') as file:
        for line in file:
            if line.startswith('username='):
                username = line.strip().split('=')[1]
            elif line.startswith('password='):
                password = line.strip().split('=')[1]
   
    body = json.loads(event['Records'][0]['body'])
    question = body["Question"]
    options = body["Options"]
    solution = body['Solution']
    options = body['Options']
    solution_index = options.index(solution)

    # Authenticate user and get the access token
    access_token = authenticate_user(username, password)

    # '{"data":{"question":"what is yuour name","answers":["1341313","31313131","131313113"],"correctAnswerIndex":0,"duration":15},"name":"quiz"}'
   
    json_ques_ans = {
        "data" : {
            "question" : question,
            "answers" : options,
            "correctAnswerIndex" : solution_index,
            "duration" : 30
        },
        "name" : "quiz"
    }
   
    metadata = pack(json_ques_ans)
   
    send_action(metadata, access_token)
   
    return {
        'statusCode': 200,
        'body': json.dumps({'access_token': access_token})
    }
