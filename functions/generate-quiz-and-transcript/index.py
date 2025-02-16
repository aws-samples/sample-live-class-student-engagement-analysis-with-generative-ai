import boto3
import json
import base64
from botocore.exceptions import ClientError
import datetime
import time
import os
import boto3
from boto3.dynamodb.conditions import Key

region = os.environ['AWS_REGION']

bedrock = boto3.client(service_name="bedrock-runtime",region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
dynamodb_name = os.environ['DYNAMODB_NAME'] #"question-bot-haiku-ddbtable-13579"
queue_url = os.environ['QUEUE_URL'] 
table1 = dynamodb.Table(dynamodb_name)
s3_client = boto3.client('s3')
sqs = boto3.client('sqs')

modelId = "anthropic.claude-3-sonnet-20240229-v1:0" #"anthropic.claude-3-haiku-20240307-v1:0"

accept = "application/json"
contentType = "application/json"

prompt_transcript = '''
Analyze the image and extract the key educational information, including any relevant questions, answers, or educational content. Format the extracted text into a structured, readable format. Just focus on the educational content while maintaining the essence of the original text. Give the transcript as it is.
Keep the text as it.
Compulsory to translate the text into english language. If something is not visisble then dont add anything or if question is not  completely visible then just skip it, dont generate transcript of it. If it is not related to aws cloud then also skip it and give the transcript as "irrelevent" If there are two question and if second question is not visible completely then skip question as well as options, dont generate transcript.
In this case give the transcript of only first question with there visible option only. dont add anything, give as it is.  Just give the english converted one, dont give both transcript and transcript converted in english language. For same question give same transcript every time.
'''

prompt_compare_transcript = '''
If the similarity between two transcripts is greater than 60%, return "result": "True". Otherwise, return "result": "False". Don't give any explaination or code.

You are tasked with comparing two transcripts,
Transcript A: [{}]

and

Transcript B: [{}]
'''

prompt_generate_question = '''
Case 1: Assume the role of a teacher, If the transcript contains a question, use the same question directly for the multiple-choice question generation. If not, formulate a new multiple-choice question based on the generated transcript to assess student attentiveness in class. Assume your role as aws cloud teacher teaching students of class 12 preparing for exams. Your job is to take test of student by generating questions which are relevent to them. Generate question only if transcript is realted to aws cloud.
First you see the image shared of a digital-board. extract text from the screen, ignore written text on t-shirts, human, branding of  Adda247 Also dont consider anything written in bold. Generate question from transcript only. Don't include text inside [] bracket in transcript. Check if question is relevant with option, then only consider it. The question should include four options, with one correct answer. Return the output in the following JSON format and without additional commentary and generate question only in english language:
{
"question": "<generated question>",
"options": ["<option 1>", "<option 2>", "<option 3>", "<option 4>"],
"solution": "<correct option>",
"result": "True"
}

Case 2: Do not generate a question if the image:
- dont ask question regarding size of file
- Contains only a logo or irrelevant graphics such as simple shapes, colors, generic symbols, or specific letters.
- Displays single words, a Welcome page, or any screenshots that show a desktop or application interface. This includes browsers, pdf, chat applications, and any visible file management or folder structure, or if any thing forwarded in chat.
- Features file-related information visible on a computer or device screen, such as file names, sizes, types, or chat messages and document names.
- Contains fewer than 8 total words where the text does not provide substantial content for creating a meaningful educational question.
- Shows handwritten content on a chalkboard.
- Includes background elements or text that do not contribute directly to a meaningful educational topic or context.

If an image meets any of the above criteria and is deemed not suitable for question generation, return the following JSON response:
{
"result": "False"
}


Ensure to evaluate the content of the image strictly and generate a response for either Case 1 or Case 2 based on the content's relevance and substantiality. Do not return outputs for both cases. Do not add additional commentary.
'''

def get_latest_entry(table_name, path):
    # Create a DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Query to fetch the latest entry for the given date
    response = table.query(
        KeyConditionExpression=Key('Path').eq(path),
        ScanIndexForward=False,  # This will sort the results by sort key in descending order
        Limit=1  # Return only the latest entry
    )

    # Extract the latest entry from the response
    items = response.get('Items')
    if items:
        return items[0]['Transcript']  # Return the latest entry
    else:
        return None  # No entries found for the given date

def get_data_from_model(prompt, image):
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image,
                        },
                    },
                ],
            }
        ],
    }

    # Invoke haiku model to get transcript
    response = bedrock.invoke_model(
        modelId=modelId,
        body=json.dumps(request_body),
    )
    result = json.loads(response.get("body").read())
    return result

def get_result_from_model(prompt):
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
    }

    # Invoke haiku model to get transcript
    response = bedrock.invoke_model(
        modelId=modelId,
        body=json.dumps(request_body),
    )
    result = json.loads(response.get("body").read())
    return result

def lambda_handler(event, context):
    ########### Read it from sqs
    for record in event['Records']:
        message_body = json.loads(record['body'])
        s3_event = message_body['Records'][0]
        curr_ts = s3_event['eventTime']
        bucket = s3_event['s3']['bucket']['name']
        key = s3_event['s3']['object']['key']

    print(bucket)
    print(key)

    # bucket = "question-bot-haiku-bucket-13579"
    # key = "test/physics/id1/thumb2.jpeg"

    path = key.split("/")
    img = path.pop()
    path = "/".join(path)

    local_path = '/tmp/' + os.path.basename(key)
    s3_client.download_file(bucket, key, local_path)

    with open(local_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf8")

    last_transcript=get_latest_entry(dynamodb_name,path)

    result = get_data_from_model(prompt_transcript, image)
    output_list = result.get("content", [])
    transcript = output_list[0]['text']
    print("=========> ",transcript)

    prompt_compare_transcript_new = prompt_compare_transcript.format(last_transcript, transcript)
    result_compare = get_result_from_model(prompt_compare_transcript_new)
    output_list_compare = result_compare.get("content", [])
    transcript_compare = output_list_compare[0]['text']
    print(">>>>>>>>>>>", transcript_compare)

    match_or_not = False
    if '"result": "True"' in transcript_compare:
        match_or_not = True

    print("-----------",match_or_not)

    if match_or_not == True:
        print("Question already generated, Not generating question.............")
        response = table1.put_item(
            Item={
                'Path': path,  # Partition key
                'Timestamp': curr_ts, # Sort key
                'Image name':img,
                'Transcript':transcript,
                'match': 'True'
            }
        )
    else:
        start_prompt = " Given this transcript : " + transcript + "\n\n"
        prompt_generate_question_mod = start_prompt + prompt_generate_question
        result_question = get_result_from_model(prompt_generate_question_mod)
        output_list_question = result_question.get("content", [])
        ques_ans_opts_transcript = output_list_question[0]['text']
        print("\n",ques_ans_opts_transcript)
        if '"result": "False"' in ques_ans_opts_transcript:
            response = table1.put_item(
                Item={
                    'Path': path,  # Partition key
                    'Timestamp': curr_ts, # Sort key
                    'Image name':img,
                    'Transcript':transcript,
                }
            )
        else:
            try:
                final_values = json.loads(ques_ans_opts_transcript)
            except:
                try:
                    json_str = ques_ans_opts_transcript.split("{", 1)[1].rsplit("}", 1)[0]
                    json_str = "{" + json_str + "}"
                    final_values = json.loads(json_str)
                except:
                    print("SKIPPING IMAGE .........")
            curr_quest = final_values['question']
            curr_options = final_values['options']
            curr_sol = final_values['solution']
            response = table1.put_item(
                Item={
                    'Path': path,  # Partition key
                    'Timestamp': curr_ts, # Sort key
                    'Question': curr_quest,
                    'Options':curr_options,
                    'Solution':curr_sol,
                    'Transcript':transcript,
                    'Image name':img
                }
            )

            # Send generated output to sqs queue
            message_body = {'Question': curr_quest,'Options':curr_options,'Solution':curr_sol}
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_body)
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully done...')
    }

