## Compliance Automation Framework using AWS Config

This project outlines a comprehensive automation framework that detects and remediates compliance violations in an AWS environment using AWS Config, SSM Automation, Lambda, SNS, EventBridge, and other services.

##  Objective

Build an end-to-end compliance automation solution that:
- Detects non-compliant resources using AWS Config rules
- Remediates issues automatically using SSM documents or Lambda
- Sends alerts via SNS and logs events to CloudWatch or S3

##  AWS Services Used

- AWS Config
- AWS Systems Manager (SSM)
- Amazon SNS
- AWS Lambda
- Amazon S3
- IAM
- CloudWatch
- EventBridge
- AWS CloudTrail

##  Scenarios Covered

1. *Open Security Group Remediation*
   - Detects Port 22 open to the public
   - Remediates using SSM
   - Sends notification via SNS

2. *Missing Required Tags on EC2*
   - Detects EC2 instances without Environment or Owner tags
   - Adds missing tags automatically

3. *CloudTrail Disabled*
   - Detects if CloudTrail logging is disabled
   - Automatically re-enables logging using Lambda

4. *S3 Public Access Block Enforcement*
   - Detects public access on S3 buckets
   - Triggers Lambda to block public access

## Testing

Each scenario includes a step-by-step guide to test the automation by simulating a non-compliant resource and verifying that the system remediates the issue and sends notifications.


