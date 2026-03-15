## Prerequisites:

Step 1. An active AWS account.

Step 2. AWS CLI installed and configured : https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

To verify if AWS CLI is installed, run the following command:

  aws --version

Step 3. Install sam cli: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

To check if SAM CLI is installed, use the following command:

  sam --version

Step 4. Having AWS profile with AWS account administrative access.

To create an IAM user with administrative access, follow this guide: https://docs.aws.amazon.com/streams/latest/dev/setting-up.html

Once the IAM user is created, generate secret credentials by following this guide: https://docs.aws.amazon.com/cli/v1/userguide/cli-authentication-user.html#cli-authentication-user-create

After obtaining the access key and secret key, use them to configure AWS CLI:

 aws configure
