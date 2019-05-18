# -*- coding: utf-8 -*-
#TODO: 

# Recommendaitions!!
# Add validation to ensure file was downloaded succesfully
# Add AWS Loggin to all parts of Script https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
# Add SNS/Email Notication For Successful or On Error of Script
# Exactract KeyName from s3 Event
# Recommendaitions!!


#Notes: #####
# You need a role for lamdba to access s3
# You need to provision NS API Key/Upload Account.
# You need Akamai Open API User Account
# You need to know the NS HOSTNAME, KEYNAME, KEY AND CPCODE
# You need to s3 Object Key (Path/File)


import json, os, requests, boto3
# Akamai Open Libs
from akamai.netstorage import Netstorage, NetstorageError
from akamai.edgegrid import EdgeGridAuth


def purgeCPCode(CP=None):


    #Fetch Credentials from Env Variables from AWS
    AO_ACCESS_TOKEN = os.environ['AO_ACCESS_TOKEN']
    AO_CLIENT_SECRET = os.environ['AO_CLIENT_SECRET']
    AO_API_HOST = os.environ['AO_API_HOST']
    AO_CLIENT_TOKEN = os.environ['AO_CLIENT_TOKEN']
    
    apiRequest = requests.Session()
    apiRequest.auth = EdgeGridAuth(
        client_token=AO_CLIENT_TOKEN,
        client_secret=AO_CLIENT_SECRET,
        access_token=AO_ACCESS_TOKEN
    )
    apiBaseUrl = "https://"+AO_API_HOST
    apiEndpoint = apiBaseUrl+ "/ccu/v3/invalidate/cpcode/staging"
    # Change Path for production network Purge
    #apiEndpoint = apiBaseUrl+ "/ccu/v3/invalidate/cpcode/production"
    postbody = '{"objects": ["' + str(CP) + '"]}'
    response = apiRequest.post(apiEndpoint, postbody, headers={"Content-Type": "application/json"})
    return {
            'status':response.status_code,
            'body': json.dumps(response.text)
        }

def uploadToNS():
    # Fetch s3 Variables from Env from AWS
    S3_Bucket = os.environ['S3_Bucket']
    S3_Path = os.environ['S3_PATH']
    S3_File = os.environ['S3_File']


    #Fetch Akamai NS Variables from Env from AWS
    NS_HOSTNAME = os.environ['NS_HOSTNAME']
    NS_KEYNAME = os.environ['NS_KEYNAME']
    NS_KEY = os.environ['NS_KEY']
    NS_CP = os.environ['NS_CP']

    getObjectFromS3(S3_Bucket,S3_Path,S3_File)

    ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY, ssl=False)
    if os.path.exists('/tmp/'+S3_File):
        ok, response = ns.upload('/tmp/'+S3_File,'/'+S3_Path+str(NS_CP)+'/')
    else:
        return {
                'status':"ERROR",
                'body': "The File /tmp/"+S3_File+" Does Not Exist!"
        }
    if ok:
        if os.path.exists('/tmp/'+S3_File):
                os.remove('/tmp/'+S3_File)
    return {
            'status':response.status_code,
            'body': json.dumps(response.text)
        }

def getObjectFromS3(bucket, path, file):
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket, path+'/'+file, '/tmp/'+file)
    return True

def run(event=None, context=None):

     return {"NetStorageUpload":uploadToNS(), "PurgeRequest":purgeCPCode(832468)

    }





