import json
import boto3
import csv
from tabulate import tabulate
import trp.trp2 as t2

queries_csv = "paystub-questions_full.csv"
s3 = boto3.client('s3')
def lambda_handler(event, context):
    textract = boto3.client("textract")
    
    bucketname = event['Records'][0]['s3']['bucket']['name']

    # List all objects in the S3 bucket
    response = s3.list_objects_v2(Bucket=bucketname)

    # Extract the file names from the response
    files = [content['Key'] for content in response['Contents']]

    for image_filename in files:
        
        
        #image_filename = event['Records'][0]['s3']['object']['key']
        
        #s3.upload_file(file, bucketname, file)
        
        print(image_filename) # get the current event
        s3.download_file(bucketname, image_filename, '/tmp/' + image_filename)
        response = None
        with open("/tmp/" + image_filename, 'rb') as document:
            imageBytes = bytearray(document.read())
        response = textract.analyze_document(
            Document={'Bytes': imageBytes},
            FeatureTypes=["QUERIES"],
            QueriesConfig={
                "Queries": [{
                    "Text": "what is Taxable Amount?",
                    "Alias": "PAYSTUB_TAXABLE_VALUE"
                },
                {
                    "Text": "What is PAN No?",
                    "Alias": "PAYSTUB_PAN_NO"
                },
                {
                    "Text": "What is Invoice No?",
                    "Alias": "PAYSTUB_INVOICE_NO"
                },
                {
                    "Text": "What is Invoice Date?",
                    "Alias": "PAYSTUB_INVOICE_DATE"
                },
                {
                    "Text": "What is the Customers Name?",
                    "Alias": "PAYSTUB_CUSTOMER_NAME"
                },
                {
                    "Text": "what is BILL TO GST?",
                    "Alias": "PAYSTUB_BILLTO_GST"
                },
                {
                    "Text": "What is GST No?",
                    "Alias": "PAYSTUB_GST_No"
                },
                {
                    "Text": "What is  VENDOR NAME?",
                    "Alias": "PAYSTUB_VENDOR_NAME"
                },
                {
                    "Text": "What is the Customers Address?",
                    "Alias": "PAYSTUB_CUSTOMER_ADDRESS"
                },
                {
                    "Text": "what is Amount in words?",
                    "Alias": "PAYSTUB_AMOUNT_WORDS"
                },
                {
                    "Text": "what is Grand Total?",
                    "Alias": "PAYSTUB_GRAND_TOTAL"
                }]
        })
        d = t2.TDocumentSchema().load(response)
        page = d.pages[0]
    
        # get_query_answers returns a list of [query, alias, answer]
        query_answers = d.get_query_answers(page=page)
        for x in query_answers:
            print(f"{image_filename},{x[0]},{x[2]}")
        
        print(tabulate(query_answers, tablefmt="github"))
    
