# transfer-s3files-to-ec2
Transfer S3 file to EC2 instance.

## Prerequisite

### Environment

* Python 3.8
* AWS SAM

### Variables examples

S3DefinedPrefix: scripts/functions  
TargetDirectory: C:\\scripts\\functions\\  

If you deploy using --parameter-overrides option, you need to specify the TargetDirectory as follows.
C:\\\\scripts\\\\functions\\\\

## Build
To build, execute the following command.

```
sam build
```

## Deploy
To deploy, execute the following command.

```
sam deploy --guided
```
