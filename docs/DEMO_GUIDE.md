## You can manually test by uploading a sample screenshot inside Amazon S3 bucket.

Step 1: Navigate to the Amazon S3 console and locate the Amazon S3 bucket created using the AWS SAM template. You can use the **sample_screenshot** image located under the **asset** folder for testing. Supported image formats: PNG, JPEG, and WebP.

To upload files to the bucket directory, follow this guide: https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-upload.html

NOTE: You must create a folder first and then upload the image.

Alternatively, you can upload using the AWS CLI:

```bash
aws s3 cp asset/sample_screenshot/image1.png s3://<YOUR_BUCKET_NAME>/test/class1/image1.png --region <YOUR_REGION>
```

Step 2. It will trigger rest of the flow of the architecture and finally you will be able to see the processing log of final AWS Lambda function with name LambdaFunctionToRecieveUniqueQuestion

To Access Lambda function logs using the console follow this steps: https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs-view.html#monitoring-cloudwatchlogs-console

![Fig 7.2](../asset/testing-demo/image3.png)
