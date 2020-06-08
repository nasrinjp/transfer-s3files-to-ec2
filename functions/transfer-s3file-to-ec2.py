from logging import getLogger, INFO
import boto3
import os
import re
 
logger = getLogger()
logger.setLevel(INFO)
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')
instance_id = os.getenv('target_instance_id')
s3_defined_prefix = os.getenv('s3_defined_prefix')
target_directory = os.getenv('target_directory')
#s3bucket = os.getenv('s3bucket')

def lambda_handler(event, context):
    try:
        ec2_response = ec2.describe_instances(InstanceIds=[instance_id])
        ec2_state = ec2_response['Reservations'][0]['Instances'][0]['State']['Name']
        if not ec2_state == "running":
            logger.info('The specific EC2 instance is not running.')
            return
        prefix = []
        for record in event['Records']:
            transport_file = record['s3']['object']['key']
            path_split = transport_file.split('/')
            path_depth = len(path_split)
            for i in range(path_depth-1):
                prefix.append(path_split[i])
            s3prefix = '/'.join(prefix)
            file_name = transport_file.split('/')[path_depth-1]
            s3bucket = record['s3']['bucket']['name']
            if s3prefix == s3_defined_prefix:
                command = f'aws s3 cp s3://{s3bucket}/{transport_file} {target_directory}{file_name}'
            else:
                logger.info('No transport file found.')
                continue
            logger.info(command)
            ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunPowerShellScript",
                Parameters={
                    "commands":[command]
                }
            )
            logger.info('Run Command has been executed successfully.')
    except Exception as error:
        logger.error(error)
        raise error