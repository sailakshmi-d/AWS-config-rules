import boto3 import datetime import json # Import json to parse JSON safely 

def lambda_handler(event, context): config = boto3.client('config') cloudtrail = boto3.client('cloudtrail') 

# Use json.loads instead of eval to parse the JSON string safely 
invoking_event = json.loads(event['invokingEvent']) 
result_token = event['resultToken'] 
 
trail_name = 'Trailtest' 
compliance_type = 'COMPLIANT' 
annotation = 'CloudTrail logging is ON' 
 
# Check logging status 
status = cloudtrail.get_trail_status(Name=trail_name) 
 
if not status['IsLogging']: 
    # Remediate: start logging 
    cloudtrail.start_logging(Name=trail_name) 
    compliance_type = 'NON_COMPLIANT' 
    annotation = 'CloudTrail logging was OFF and has been remediated by enabling it.' 
 
# Report compliance result to AWS Config 
config.put_evaluations( 
    Evaluations=[ 
        { 
            'ComplianceResourceType': 'AWS::CloudTrail::Trail', 
            'ComplianceResourceId': trail_name, 
            'ComplianceType': compliance_type, 
            'Annotation': annotation, 
            'OrderingTimestamp': datetime.datetime.now() 
        } 
    ], 
    ResultToken=result_token 
) 
 
return { 
    'statusCode': 200, 
    'body': f"Compliance check complete. Status: {compliance_type}" 
} 
 