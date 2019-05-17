# -*- coding: utf-8 -*-
#TODO: 

# Pending #####
# Add validation to ensure file was downloaded succesfully
# Add AWS Loggin to all parts of Script https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
# Add SNS/Email Notication For Successful or On Error of Script
# Exactract KeyName from s3 Event


#Notes: #####
# You need a role for lamdba to access s3
# You need to provision NS API Key/Upload Account.
# You need Akamai Open API User Account
# You need to know the NS HOSTNAME, KEYNAME, KEY AND CPCODE
# You need to s3 Object Key (Path/File)
# You need 

import json, os, requests, boto3

# Akamai Open Libs
from akamai.netstorage import Netstorage, NetstorageError
from akamai.edgegrid import EdgeGridAuth

# [START] REMOVE THIS WHEN UPLOADED
# [START] CREDETIALS to run locally
# CCU Hardcoded Credentials user:rmartineos_ccu 
AO_CLIENT_SECRET = "3aBr7x6xSaGGBHXrNdPwp5vWr1Vvsxe1zoBhqZ6/hIs="
AO_API_HOST = "akab-ohy6cte6wxcwtupu-5jc2i7ury74bvzqj.purge.akamaiapis.net"
AO_ACCESS_TOKEN = "akab-khtzuwjwpe2o7zvt-3rkn5x3nzpk3ccxh"
AO_CLIENT_TOKEN = "akab-cajmk2oupzfgx762-akjkzaxzzogye5gb"

NS_HOSTNAME = 'rmartineos-nsu.akamaihd.net'
NS_KEYNAME = 'rmartineos_api'
NS_KEY = '13QQ6gGpT5tHGfUAMKn3yZimmuOamktgeYcUz1a6S6mq'
NS_CP = 746467
# [END] CREDETIALS to run locally

# [START] s3 Bucket
# s3 Bucket and File information, this can be fetched dynamically 
S3_Bucket = "rmartinezb"
S3_Path = "clarovideo"
S3_File = "epg"
# [END] s3 Bucket
# [END] REMOVE THIS WHEN UPLOADED

def purgeURL(CP=None):


    #Fetch Credentials from Env Variables from AWS
    #AO_ACCESS_TOKEN = os.environ['AO_ACCESS_TOKEN']
    #AO_CLIENT_SECRET = os.environ['AO_AO_CLIENT_SECRET']
    #AO_API_HOST = os.environ['AO_API_HOST']
    #AO_ACCESS_TOKEN = os.environ['AO_CLIENT_TOKEN']
    
    apiRequest = requests.Session()
    apiRequest.auth = EdgeGridAuth(
        client_token=AO_CLIENT_TOKEN,
        client_secret=AO_CLIENT_SECRET,
        access_token=AO_ACCESS_TOKEN
    )
    apiBaseUrl = "https://"+AO_API_HOST
    apiEndpoint = apiBaseUrl+ "/ccu/v3/invalidate/cpcode/staging"
    postbody = '{"objects": ["' + str(CP) + '"]}'
    response = apiRequest.post(apiEndpoint, postbody, headers={"Content-Type": "application/json"})
    return {
            'status':response.status_code,
            'body': json.dumps(response.text)
        }

def uploadToNS(directory,filename):
    
    #Fetch Akamai NS Variables from Env from AWS
    #NS_HOSTNAME = os.environ['NS_HOSTNAME']
    #NS_KEYNAME = os.environ['NS_KEYNAME']
    #NS_KEY = os.environ['NS_KEY']
    

    ns = Netstorage(NS_HOSTNAME, NS_KEYNAME, NS_KEY, ssl=False)
    if os.path.exists('/tmp/'+filename):
    #if os.path.exists('/tmp/'+filename):
        ok, response = ns.upload('/tmp/'+filename,'/'+directory+str(NS_CP)+'/')
    else:
        return {
                'status':"ERROR",
                'body': "The File /tmp/"+filename+" Does Not Exist!"
        }
    if ok:
        if os.path.exists('/tmp/'+filename):
                os.remove('/tmp/'+filename)
    return {
            'status':response.status_code,
            'body': json.dumps(response.text)
        }

def getObjectFromS3(bucket, path, file):
    #s3 = boto3.resource('s3')

    #s3.meta.client.download_file(bucket, path+'/'+file, '/tmp/'+file)
    return True

def run(event=None, context=None):
    #GET Env Variables

    #Fetch S3 Variables from Env
    #S3_Bucket = os.environ['S3_Bucket']
    #S3_Path = os.environ['S3_PATH']
    #S3_File = os.environ['S3_File']
    #NS_CP = os.environ['NS_CP']
    #getObjectFromS3(S3_Bucket,S3_Path,S3_File)

    
    return {"NetStorageUpload":uploadToNS("",S3_File), "PurgeRequest":purgeURL(832468)

    }

run()





