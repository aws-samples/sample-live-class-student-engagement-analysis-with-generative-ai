# Live class student attentiveness and engagement analysis with GenAI

### Version 1.0.0
## Overview

Maintaining student engagement during live online classes is challenging, as active participation and real-time interaction are crucial for effective learning. Instructors often struggle to measure student engagement, impacting the learning process and overall experience. To address this, our solution enhances online learning by monitoring and improving student attentiveness in real-time. Using Amazon Interactive Video Service (IVS), the system captures screenshots of live sessions and generates interactive, content-driven questions. This technology, ideal for educational institutions and e-learning platforms, ensures continuous engagement and adapts to dynamic educational content, optimizing virtual classroom experiences.

# Architecture Diagram
 
In this section, we will walk you through the architecture of this prototype, designed to analyze student engagement and attentiveness in live classrooms using Generative AI. This architecture ensures that teachers can get real-time insights into how well students are engaging with the lesson content, and it is built to scale seamlessly with minimal overhead. We have created 1-click deployment option of this prototype solution in form of AWS CloudFormation template allowing you to deploy easily in your AWS account. Follow “How to deploy” section below for more details.

  ![Fig 1](./asset/architecture.png)

### Step 1: Capturing Screenshots from the Live Classroom

The first step in our solution involves capturing regular screenshots of the content being shared during a live classroom session. This process is essential for analyzing the content and creating contextually relevant polls and quizzes for student engagement. Our demo integrates Amazon Interactive Video Service (Amazon IVS) for streaming, the solution is designed to be flexible and can work with any live streaming platform that allows screen capture. A solution then can store them on Amazon Simple Storage Service (Amazon S3) to proceed further. 

Here, we can use already existing Amazon IVS demo Amazon IVS UGC platform—a reference demo application that allows for live streaming, user authentication, live chat, and more. Follow GitBub README.mdfor installing this demo in your AWS account.

Amazon IVS allows you to configure Low Latency and Real-time both options with Recording Configuration that allows to simple capture thumbnail every second up to 60 seconds. For the demo we have configured thumbnail generation to be done every 60 seconds with Default Configuration. For Storage, select an existing Amazon S3 bucket which will be created as part of the prototype AWS CloudFormation template based deployment.

### Step 2: Integrating thumbnails from Amazon S3 Bucket to :

Once the thumbnail being sent and stored inside Amazon S3 bucket, we can use Amazon S3 Event Notification feature configured to notify when any new thumbnails being uploaded to the Amazon S3 bucket. This event triggers the next steps of the workflow, to process the image and generate the corresponding transcript and quiz/poll.  Every time a thumbnail is uploaded to Amazon S3, it triggers an S3 Event Notification, which stores message in Amazon Simple Queue Service (Amazon SQS) for asynchronous event-driven processing which then consume by an AWS Lambda function. 

This configuration and rest of setup will get deployed as part of the prototype solution.

### Step 3: Processing thumbnail with AWS Lambda Function

The Amazon SQS message gets consumed by an AWS Lambda function that handles the entire image processing workflow, i.e. Understand what has been presented as part of thumbnail. Validate whether extracted content of thumbnail is relevant to the topic being taught, Validate content is complete and viable to generate a quiz and also validate content itself is a quiz/poll. We also make sure thumbnail is having unique content wrt previous thumbnails (same screen).

### Step 4: Transcript Generation using Amazon Bedrock


Now, the AWS Lambda function will process the image and use Amazon Bedrock to generate a transcript of the content from the thumbnail. Here we are using Anthropic Claude 3.5 Sonnet V2 foundation model provided by Amazon Bedrock service, which helps extract relevant text(e.g., text on a presentation slide, or a whiteboard drawing) from the image content.

### Step 5: Storing transcript and ensuring it’s Uniqueness


Once the transcript is generated, it is important to ensure its uniqueness before generating any questions, as it is possible that the teacher stays on the same screen for few minutes, which makes same screenshot captured multiple times. 

To achieve uniqueness, we perform the following steps:

Uniqueness Check: The newly generated transcript is compared against previous transcripts to ensure that it is not repetitive. This is done by storing each transcript in Amazon DynamoDB, a fast and scalable NoSQL database. Each new transcript is checked against the previous records in DynamoDB to determine whether it has been already generated.
Bedrock Prompt for Similarity Check: To ensure the uniqueness of the transcript, we use a custom prompt , the prompt is designed to compare the semantic similarity between the new transcript and previous ones. If the similarity exceeds a certain threshold, the system will discard the new transcript and will not generate a new question. This step ensures that we don't overwhelm students with redundant questions.

Generating Questions from the Transcript


Once we have verified the uniqueness of the transcript, the next step is to generate questions from the transcript. The generation of questions follows a structured approach:

Transcript-to-Question Generation: Once we have a unique transcript, we use Amazon Bedrock’s generative capabilities to generate a set of multiple-choice questions (MCQs). The system is designed to extract key concepts from the transcript and frame questions that test the students’ understanding of those concepts.
 For example, if the teacher explains a complex concept (e.g., Newton's laws of motion), the question generated might focus on the key principles behind those laws. 

Handling Corner Cases: In certain situations, like if the screen is empty or if the content on the screen does not match the theme of the class, we provide a fallback mechanism. This is again instructed in Bedrock prompt to skip generating questions. For example, if no content is available (i.e., a blank screen or loading screen or welcome screen), the system will not try to generate questions.

Storing Questions in DynamoDB: The generated questions (along with answer choices and the correct answer) are stored in Amazon DynamoDB. This serves as a reliable and efficient database for keeping track of all questions generated during the live session. Each question is stored with a timestamp to ensure chronological order.

### Step 6:  Storing and Delivering Questions


Once the questions are generated, they need to be stored and delivered to the students in real time. For extensibility of solution, here we use Amazon SQS. Questions are pushed into an Amazon SQS queue.

### Step 7: Triggering Lambda from SQS


Once the questions are pushed into the Amazon SQS (Simple Queue Service) queue, it triggers an AWS Lambda function that processes the questions for delivery to the students.

### Step 8:  Lambda Function for Delivery: 
    
The AWS Lambda function reads the messages from the Amazon SQS queue and sends the generated questions to the students’ UI. In our sample demo, we have integrated this logic to deliver questions to the UGC demo solution. However, the Lambda function is extensible and can be customized to integrate with any API integration to connect with your live-class streaming solution. If you are using UGC demo the you can use the as-is AWS lambda Function.
    

### Monitoring Engagement and Providing Insights to Teachers


For better outcome, you can build capture student’s interaction and build live-dashboard for teachers and administrators focusing on monitoring student attentiveness and engagement to get better insights. Current demo doesn't showcase this monitoring functionality.

Student Interaction Monitoring: As part of UGC demo, when students answer polls and quizzes, their responses are tracked and stored in Amazon DynamoDB . This data can be used to evaluate engagement and attentiveness, such as how many students have answered the quiz and how many of them are answering correctly, etc.

Real-time Analytics: Teachers can be provided with a live dashboard that visualizes key engagement metrics, such as the number of questions answered, average scores, and trends in student participation. With this data, teachers can adjust their teaching strategies, revisit challenging concepts, and identify disengaged students who may need additional support.

This functionality allows for personalized feedback and the ability to adapt teaching strategies in real-time, enhancing overall engagement and learning outcomes.

## Deployment guide

### Pre-requisite

### How to install
[Click this link for step by step guide](docs/DEPLOYMENT_GUIDE.md)

### How to test
[Click this link to learn how to run the demo](docs/DEMO_GUIDE.md)

### How to clean-up

### How to test with UGC demo (optional)

  
## License

This library is licensed under the MIT-0 License.

Please see LICENSE for applicable license terms and NOTICE for applicable notices.
  

