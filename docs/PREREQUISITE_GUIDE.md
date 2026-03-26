## Prerequisites:

Step 1. An active AWS account.

Step 2. AWS CLI installed and configured : https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

To verify if AWS CLI is installed, run the following command:

  aws --version

Step 3. Install sam cli: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

To check if SAM CLI is installed, use the following command:

  sam --version

Step 4. AWS CLI configured with valid credentials that have administrative access.

You can use IAM Identity Center (SSO), IAM user credentials, or any supported authentication method. To verify your credentials are working:

 aws sts get-caller-identity

     or use
 
 aws configure
