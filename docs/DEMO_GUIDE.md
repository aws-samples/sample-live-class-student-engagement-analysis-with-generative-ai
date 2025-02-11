## You can manually test by uploading a jepg sample screenshot inside S3 bucket.

Step 1: Navigate to the S3 console and locate the S3 bucket created using the SAM template. You can use the **sample_screenshot** image located under the **assets** folder for testing.

To upload files to the bucket directory, follow this guide:: https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-upload.html

NOTE: You must create a folder first and then upload the image.

Step 2. It will trigger rest of the flow of the architecture and finally you will be able to see the processing log of final AWS Lambda function with name LambdaFunctionToRecieveUniqueQuestion

To Access Lambda function logs using the console follow this steps: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs-view.html#monitoring-cloudwatchlogs-console

![Fig 7.2](../asset/testing-demo/image3.png)