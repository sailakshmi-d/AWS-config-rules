import boto3
import json
import botocore

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # List all buckets
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    
    for bucket in buckets:
        # Check current public access block config
        try:
            pab = s3.get_public_access_block(Bucket=bucket)
            pab_config = pab['PublicAccessBlockConfiguration']
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchPublicAccessBlockConfiguration':
                pab_config = None
            else:
                raise
        
        # If no block or partial block, apply full block
        if (not pab_config or
            not pab_config.get('BlockPublicAcls', False) or
            not pab_config.get('IgnorePublicAcls', False) or
            not pab_config.get('BlockPublicPolicy', False) or
            not pab_config.get('RestrictPublicBuckets', False)):
            
            print(f"Applying full public access block to bucket: {bucket}")
            s3.put_public_access_block(
                Bucket=bucket,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
            
        # Optionally, remove overly permissive bucket policy
        try:
            policy = s3.get_bucket_policy(Bucket=bucket)
            policy_str = policy['Policy']
            policy_doc = json.loads(policy_str)
            statements = policy_doc.get('Statement', [])
            
            # Check for public access in policy statements
            public_statements = [stmt for stmt in statements if
                (stmt.get('Effect') == 'Allow' and
                 (stmt.get('Principal') == '*' or
                  stmt.get('Principal', {}).get('AWS') == '*') and
                 ('Action' in stmt) and
                 ('Condition' not in stmt))]
            
            if public_statements:
                print(f"Removing public statements from bucket policy for: {bucket}")
                # Remove public statements
                policy_doc['Statement'] = [stmt for stmt in statements if stmt not in public_statements]
                if policy_doc['Statement']:
                    s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy_doc))
                else:
                    s3.delete_bucket_policy(Bucket=bucket)
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucketPolicy':
                # No policy attached, nothing to remove
                pass
            else:
                print(f"Error processing bucket {bucket}: {str(e)}")
                raise
        except Exception as e:
            print(f"Unexpected error processing bucket {bucket}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('S3 bucket public access remediation complete.')
    }
