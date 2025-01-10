## Prerequisites:

Step 1. An active AWS account.

Step 2. AWS CLI installed and configured

Step 3. Enable Amazon Bedrock Model access.

 a. Navigate to AWS console, search for **Amazon Bedrock**. 

 b. Click on **Get Started** and then click on **Request access model** from the bottom of left pannel.

  ![Fig 1.1](/student-activity-monitor/live-class-student-engagement-analysis-with-generative-ai/asset/bedrock/image1.png)

  ![Fig 1.2](/live-class-student-engagement-analysis-with-generative-ai/asset/bedrock/image2.png)

 c. Enable Claude 3 sonet Model and click on **Next**.

  ![Fig 1.3](/live-class-student-engagement-analysis-with-generative-ai/asset/bedrock/image3.png)

 d. Click on **Submit** button to save the changes.

  ![Fig 1.4](/live-class-student-engagement-analysis-with-generative-ai/asset/bedrock/image4.png)

## Now Deploy the CloudFormation template to launch all the resources

Step 1. To obtain all the necessary files locally, run the following command:

`git clone git@ssh.gitlab.aws.dev:nehanejh/live-class-student-engagement-analysis-with-generative-ai.git`

Alternatively, you can download the provided files directly.

Step-2: Next, open the downloaded repository in VS Code and navigate to live-class-student-engagement-analysis-with-generative-ai.

Step-3: Then, run the following commands:

    sam build
    sam deploy

Step-4: It will prompt you for the stack name and S3 bucket name. Provide the stack name and S3 bucket name. For the rest of the parameters, you can either provide a value or leave them blank to accept the default values.

Note: The S3 bucket name must be globally unique.
Note: Make sure to copy the S3 bucket name for future reference.

These commands will launch all the required resources.

Afterwards, go to CloudFormation. Within 1-2 minutes, you’ll see the stack created. From there, you can access any resources by clicking on the physical ID.


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

![Fig 8.1](/live-class-student-engagement-analysis-with-generative-ai/asset/demo/image1.png)

Step-2. Click on the Outputs tab, scroll down, and find the frontendAppBaseUrl. Use this URL to open the login page.

![Fig 8.2](/live-class-student-engagement-analysis-with-generative-ai/asset/demo/image2.png)

Step-3. Create a user account and login to access the home screen.

![Fig 8.3](/live-class-student-engagement-analysis-with-generative-ai/asset/demo/image3.png)

![Fig 8.4](/live-class-student-engagement-analysis-with-generative-ai/asset/demo/image4.png)

![Fig 8.5](/live-class-student-engagement-analysis-with-generative-ai/asset/demo/image5.png)

Step-4. Now navigate to the **IVS Console**, you will find the channel you created. Next, we need to add the recording configuration to automatically capture screenshots from the live session and send them to the S3 bucket deployed from the first CloudFormation template.x

![Fig 8.6](/live-class-student-engagement-analysis-with-generative-ai/asset/recording-config/image1.png)

Step-5. Access **Recording Configuration** From the left panel, select **Recording configuration** then **create recording configuration**.

![Fig 8.7](/live-class-student-engagement-analysis-with-generative-ai/asset/recording-config/image2.png)

step-6. Provide a name for your recording configuration.

Step-7. Choose **Custom Configuration** and set the **Target thumbnail** interval to 30 seconds.

![Fig 8.8](/live-class-student-engagement-analysis-with-generative-ai/asset/recording-config/image3.png)

Step-8. Select Storage Option: Under Storage, choose Select an **existing Amazon S3 bucket**.

![Fig 8.9](/live-class-student-engagement-analysis-with-generative-ai/asset/recording-config/image4.png)

Step-8. Locate Your S3 Bucket: Use the S3 bucket name that you copied when providing the resource name for deploying the CloudFormation template, or you can find the name of your S3 bucket from the first stack you deployed.

Step-9. Finalize Configuration: Under Amazon S3 bucket, select the appropriate bucket, then click on **Create recording configuration**.

Step-10. Go to the channel, attach the recording configuration, click on **Edit** from the top menu.

![Fig 8.11](/live-class-student-engagement-analysis-with-generative-ai/asset/recording-config/image7.png)

Step-11. **Enable automatic recording**, select the created recording configuration, and click **Save Changes.**

![Fig 8.12](/live-class-student-engagement-analysis-with-generative-ai/asset/recording-config/image8.png)
