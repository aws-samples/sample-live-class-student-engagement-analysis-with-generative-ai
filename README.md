# Live class student attentiveness and engagement analysis with GenAI

Maintaining student engagement during live online classes is challenging, as active participation and real-time interaction are crucial for effective learning. Instructors often struggle to measure student engagement, impacting the learning process and overall experience. To address this, our solution enhances online learning by monitoring and improving student attentiveness in real-time. Using Amazon Interactive Video Service (IVS), the system captures screenshots of live sessions and generates interactive, content-driven questions. This technology, ideal for educational institutions and e-learning platforms, ensures continuous engagement and adapts to dynamic educational content, optimizing virtual classroom experiences.

# Architecture Diagram
 
In this section, we will walk you through the architecture of this sample solution, designed to analyze student engagement and attentiveness in live classrooms using Generative AI. This architecture follows Server-less architecture pattern with event-driven approach built to scale seamlessly with minimal overhead. Architecture follows event-driven approach which has been explained for each step below:

![Fig 1](./asset/architecture.png)

#### Step 1: Capturing Screenshots from the Live Classroom

The first step in our solution involves capturing screens at regular interval. Our demo integrates **Amazon Interactive Video Service (Amazon IVS)** for streaming, the solution is designed to be flexible and can work with any live streaming solution that allows screen capture programmatically / able to store them to Amazon S3 bucket. Solution then can store them on Amazon Simple Storage Service (Amazon S3) to proceed further. 

For the demo, we can use another existing Amazon IVS based solution **Amazon IVS UGC platform**—a reference demo application that allows live streaming, user authentication, live chat, and more. Follow **GitHub README.md** for more details including steps for installing it in your AWS account.

Amazon IVS allows you to configure Low Latency and Real-time both options with Recording Configuration that allows to capture screen thumbnails every second up to 60 seconds and store them to Amazon S3 bucket. For the demo we have configured thumbnail generation to be done every 30 seconds with Default Configuration. 


#### Step 2: Integrating thumbnails from Amazon S3 Bucket :

Once the thumbnail being captured and stored inside Amazon S3 bucket, we can use **Amazon S3 Event Notification** feature configured to notify for any new thumbnails being uploaded to the Amazon S3 bucket. This event triggers the next steps of the workflow, to process the image and generate the corresponding transcript and quiz/poll.  Every time a thumbnail is uploaded to Amazon S3, it triggers an **S3 Event Notification**, which stores message in Amazon Simple Queue Service (Amazon SQS) for asynchronous event-driven processing which then consume by an AWS Lambda function.

#### Step 3: Processing thumbnail with AWS Lambda Function

The Amazon SQS messages gets consumed by an AWS Lambda function that handles the entire image processing workflow, i.e. Understand what has been presented as part of captured screen thumbnail. Validate whether extracted content of thumbnail is relevant to the topic being taught, Validate whether content is complete and viable to generate a quiz and also validate content itself is a quiz/poll.

#### Step 4: Transcript Generation using Amazon Bedrock

After validating different scenario, the **AWS Lambda** function will process the image and use **Amazon Bedrock** to generate the transcript of the content from the thumbnail (e.g., text on a presentation slide, or a whiteboard drawing).

#### Step 5: Storing transcript and ensuring it’s Uniqueness

Once the transcript is generated, it is important to ensure its uniqueness before generating any questions, as it is possible that the teacher stays on the same screen for few minutes, which makes same screenshot captured multiple times. 

AWS Lambda function perform various steps mentioned below:

**Uniqueness Check**: The newly generated transcript is compared against previous transcripts to ensure that it is not repetitive. This is done by storing each transcript in **Amazon DynamoDB**, a fast and scalable NoSQL database. Each new transcript is checked against the previous records in DynamoDB to determine whether it has been already generated.

**Bedrock Prompt for Similarity Check**: To ensure the uniqueness of the transcript, we use a **custom prompt** , the prompt is designed to compare the semantic similarity between the new transcript and previous ones. If the similarity exceeds a certain threshold, the system will discard the new transcript and will not generate a new question. This step ensures that we don't overwhelm students with redundant questions.

**Generating Questions from the Transcript**: Once we have a unique transcript, we use **Amazon Bedrock based generative AI model** to generate a set of multiple-choice questions (MCQs)/polls. The system is designed to extract key concepts from the transcript and frame questions that test the students’ understanding of those concepts. For example, if the teacher explains a complex concept (e.g., Newton's laws of motion), the question generated will focus on the key principles behind those laws. 

**Handling Corner Cases**: In certain situations, like if the screen is empty or if the content on the screen does not match the theme of the class, we provide a fallback mechanism. This is again instructed in **Bedrock prompt** to skip generating questions. For example, if no content is available (i.e., a blank screen or loading screen or welcome screen), the system will not try to generate questions.

**Storing Questions in DynamoDB**: The generated questions (along with answer choices and the correct answer) are stored in **Amazon DynamoDB**. This serves as a reliable and efficient database for keeping track of all questions generated during the live session. Each question is stored with a timestamp to ensure chronological order.


#### Step 6:  Storing and Delivering Questions

To deliver these questions to students in real time, these questions are also being sent to an **Amazon SQS Queue** for extensible architecture. Here we can integrate it with existing solution as well to pull message from queue and integrate with any live-classroom solution.

#### Step 7: Triggering Lambda from SQS

We are using another **AWS Lambda function** which pulls message from Amazon SQS queue to fetch the poll/quiz and integrate it live-classroom solution.

#### Step 8:  Lambda Function for Delivery: 
    
1. The AWS Lambda function reads the messages from the Amazon SQS queue and sends the generated questions to the students’ UI. In our sample solution, we have integrated logic to deliver questions to the **Amazon IVS UGC platform** demo solution. Although, the AWS Lambda function is extensible and can be customized to integrate with any API integration to connect with your live-class streaming solution.

#### Further extension

Sample solution can be further extended to build UI dashboards showcasing engagement and attentiveness insights from student’s interaction for teachers and administrators. Current sample solution doesn't showcase this monitoring functionality.

**Student Interaction Monitoring**: As part of **Amazon IVS UGC platform** demo, when students answer polls and quizzes, their responses are tracked and stored in **Amazon DynamoDB table**. This data can be used to evaluate engagement and attentiveness, such as how many students have answered the quiz and how many of them have answered correctly, etc.

**Real-time Analytics**: Teachers can be provided with a **live dashboard** that visualizes key engagement metrics, such as the number of questions answered, average scores, and trends in student participation. With these data, teacher can adjust their teaching strategies, revisit challenging concepts, and identify disengaged students who may need additional support.

This functionality allows for personalized feedback and the ability to adapt teaching strategies in real-time, enhancing overall engagement and learning outcomes.


# License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.
