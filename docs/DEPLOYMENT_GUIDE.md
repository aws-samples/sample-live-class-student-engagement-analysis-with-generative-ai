## Prerequisites:

Step 1. An active AWS account.

Step 2. AWS CLI installed and configured

Step 3. Enable Amazon Bedrock Model access.

 a. Navigate to AWS console, search for **Amazon Bedrock**. 

 b. Click on **Get Started** and then click on **Request access model** from the bottom of left pannel.

  ![Fig 1.1](/live-class-student-engagement-analysis-with-genai/asset/bedrock/image1.png)

  ![Fig 1.2](/live-class-student-engagement-analysis-with-genai/asset/bedrock/image2.png)

 c. Enable Claude 3 sonet Model and click on **Next**.

  ![Fig 1.3](/live-class-student-engagement-analysis-with-genai/asset/bedrock/image3.png)

 d. Click on **Submit** button to save the changes.

  ![Fig 1.4](/live-class-student-engagement-analysis-with-genai/asset/bedrock/image4.png)

## Now Deploy the CloudFormation template to launch all the resources

Step 3. To obtain all the necessary files locally, run the following command:

`git clone git@ssh.gitlab.aws.dev:nehanejh/live-class-student-engagement-analysis-with-genai.git`

Alternatively, you can download the provided files directly.

Step 2. Go to the AWS console and navigate for **cloudformation**.

Step 3. Click on **create stack**  button and select **with new resource(standard)** .

  ![Fig 2](/live-class-student-engagement-analysis-with-genai/asset/cloudformation-stack/image1.png)

step 4. Then select **Choose an existing template** under prepare template. Under template source select **upload a template file** and then choose file **main-template.yaml** from the extreacted zip-file and click on **Next**.

  ![Fig 3](/live-class-student-engagement-analysis-with-genai/asset/cloudformation-stack/image2.png)

Step 5. Provide the stack details:

  > [!NOTE]

  > This will create all the resources. Make sure that a resource with the same name does not already exist.

  > Bucket name should be globally unique and bucket should contain only lowercase and  hyphon.

  ![Fig 4](/live-class-student-engagement-analysis-with-genai/asset/cloudformation-stack/image3.png)


     i. DynamoDBForAllData : This DynamoDB will store all the transcript of image along with generated question and correct option

    ii. IVSScreenshotBucket : IVS image will get uploaded to this bucket

    iii.ThumbnailProcessingQueue : This queue will call lambda to generate question upon every put event in s3

    iv. UniqueQuestionQueue : Unique questions will be sent to this queue, which will trigger a Lambda function. This Lambda function will receive the unique questions and send it to the UI.

  Make sure to copy the bucket name and then click on **Next**

Step 6. Leave everything as default , and click on **Next**

  ![Fig 5](/live-class-student-engagement-analysis-with-genai/asset/cloudformation-stack/image4.png)

Step 7. Under capabilities click on checkbox, then click on **Submit** button to create the stack. This will launch all the required resources.
  
**I acknowledge that AWS CloudFormation might create IAM resources.**

  ![Fig 6](/live-class-student-engagement-analysis-with-genai/asset/cloudformation-stack/image5.png)


Now, if you go to CloudFormation, you will see the stack get created within 1-2 minutes. From there, you can access any resources by clicking on the physical ID.

# Upload the Lambda Function Code

Navigate to the CloudFormation stack and open the stack you have deployed. Go to the Resources section and click on the link for the AWS Lambda function named **LambdaFunctionToReceiveUniqueQuestion**.

![Fig 7.1](/live-class-student-engagement-analysis-with-genai/asset/lambda-fun/image1.png)

Click on **Upload** from the top and select .zip file.

![Fig 7.2](/live-class-student-engagement-analysis-with-genai/asset/lambda-fun/image2.png)

Choose th file named **lambda_function.zip** from your local and click on **Save**.

# Update the index.py File

Open the index.py file, replace the placeholder for client_id with your Cognito client ID:

Go to the Cognito console, open the user pool associated with your application.

Click on the **App Integration** tab and copy the **client ID** from the bottom of the page.

Paste the copied client ID into your index.py file.

Update the API URL

Replace the **url_link** variable in your index.py file with the following value:

apiBaseUrl/channel/actions/send

-> You can obtain this URL after deploying the IVS UGC demo from the CloudFormation stack named UGC dev, found in the output section and append /channel/actions/send at the end.

Update the Environment Variables

Open the .env file and replace the username and password fields with your UGC Demo login ID and password.



# Follow these steps to set up the IVS UGC demo(for dev environment).

link: https://github.com/aws-samples/amazon-ivs-ugc-platform-web-demo?tab=readme-ov-file#deployment

# Now do the following changes in Cognito

Go to the Cognito Console, you will find the the created channel, open the channel and go to **User Pool Properties** tab at the end.

From here delete all the Lambda Trigger.


# Integration of IVS UGC Demo with the solution to generate Question based upon captured Screenshot.


Step-1. Go to the CloudFormation console and locate the stack named **UGC dev**.

![Fig 8.1](/live-class-student-engagement-analysis-with-genai/asset/demo/image1.png)

Step-2. Click on the Outputs tab, scroll down, and find the frontendAppBaseUrl. Use this URL to open the login page.

![Fig 8.2](/live-class-student-engagement-analysis-with-genai/asset/demo/image2.png)

Step-3. Create a user account and login to access the home screen.

![Fig 8.3](/live-class-student-engagement-analysis-with-genai/asset/demo/image3.png)

![Fig 8.4](/live-class-student-engagement-analysis-with-genai/asset/demo/image4.png)

![Fig 8.5](/live-class-student-engagement-analysis-with-genai/asset/demo/image5.png)

Step-4. Now navigate to the **IVS Console**, you will find the channel you created. Next, we need to add the recording configuration to automatically capture screenshots from the live session and send them to the S3 bucket deployed from the first CloudFormation template.x

![Fig 8.6](/live-class-student-engagement-analysis-with-genai/asset/recording-config/image1.png)

Step-5. Access **Recording Configuration** From the left panel, select **Recording configuration** then **create recording configuration**.

![Fig 8.7](/live-class-student-engagement-analysis-with-genai/asset/recording-config/image2.png)

step-6. Provide a name for your recording configuration.

Step-7. Choose **Custom Configuration** and set the **Target thumbnail** interval to 30 seconds.

![Fig 8.8](/live-class-student-engagement-analysis-with-genai/asset/recording-config/image3.png)

Step-8. Select Storage Option: Under Storage, choose Select an **existing Amazon S3 bucket**.

![Fig 8.9](/live-class-student-engagement-analysis-with-genai/asset/recording-config/image4.png)

Step-8. Locate Your S3 Bucket: Use the S3 bucket name that you copied when providing the resource name for deploying the CloudFormation template, or you can find the name of your S3 bucket from the first stack you deployed.

Step-9. Finalize Configuration: Under Amazon S3 bucket, select the appropriate bucket, then click on **Create recording configuration**.

Step-10. Go to the channel, attach the recording configuration, click on **Edit** from the top menu.

![Fig 8.11](/live-class-student-engagement-analysis-with-genai/asset/recording-config/image7.png)

Step-11. **Enable automatic recording**, select the created recording configuration, and click **Save Changes.**

![Fig 8.12](/live-class-student-engagement-analysis-with-genai/asset/recording-config/image8.png)
