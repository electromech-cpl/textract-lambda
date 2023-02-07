# textract-lambda
textract-lambda
Automatically extract handwriting, text or data from any document using machine learning.
Here,  we are looking for textract from invoice documents. We are using the AWS Lambda function to extract invoice documents that are uploaded to s3 bucket. 

Prerequisites: 

Lamda Service
- Textract Service
- Simple Storage Service(s3)
- Identity Access Management Service(IAM)

Details architecture of implementation is given below: 


![Screenshot from 2023-02-07 16-26-15](https://user-images.githubusercontent.com/72973799/217235708-bcacc6f9-6d99-43a6-b5e8-fbb60e94ea00.png)


Steps to create above architecture are mentioned below: 
- Step 1: Create the S3 Bucket
- Step 2: Create The S3 Lambda Trigger
- Step 3: Creating Lambda function
- Step 4: Create Lambda Layer with boto3, trp.trp2, and tabulate package
- Step 5 : write a lambda code to use aws textract service and it will give output in json format to cloudwatch logs.
