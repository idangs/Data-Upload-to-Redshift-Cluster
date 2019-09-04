"""
Uploads files as redshift tables
Date: 03/09/2019
"""

# Import libraries
import os
import requests
import sys
import pandas as pd

import psycopg2
# http://initd.org/psycopg/docs/

import boto3
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html


'''
Fill these in - you get them when you create a Redshift cluster
'''

my_db = 'XXXXXXXXXXXXX'
my_host = 'XXXXXXXXXXXXX'
my_port = 'XXXXXXXXXXXXX'
my_user = 'XXXXXXXXXXXXX'
my_password = 'XXXXXXXXXXXXX'

'''
Enter your aws access credentials
'''

access_key = 'XXXXXXXXXXXXX'
secret_key = 'XXXXXXXXXXXXX'


'''
Create S3 bucket and upload files
'''

cmd_args = sys.argv

if len(cmd_args) == 2 and ('-h' in cmd_args or '--help' in cmd_args):
    print(__doc__)
    sys.exit()

os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'

# create a resource instance
s3 = boto3.resource('s3')
results = s3.create_bucket(
                             Bucket= cmd_args[2],
                             CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}
                            )

# the path to the local directory which contains the local files to be transferred
local_directory = cmd_args[1]

# the name of the destination bucket on s3
bucket = cmd_args[2]
if len(cmd_args) > 3:
    if '-d' in cmd_args:
        d_index = cmd_args.index('-d')

        # the destination folder in the destination bucket
        dest_directory = cmd_args[d_index + 1]
    else:
        dest_directory = ''

    if '-ext' in cmd_args:
        ext_index = cmd_args.index('-ext')
        extensions = tuple(cmd_args[ext_index + 1].split(','))
        files_list = [
            x for x in os.listdir(local_directory) if (
                not x.startswith(".") and
                os.path.isfile(os.path.join(local_directory, x))
                and x.endswith(extensions))
        ]
    else:
        files_list = [
            x for x in os.listdir(local_directory) if (
                not x.startswith(".") and
                os.path.isfile(os.path.join(local_directory, x)))
        ]

# get the code of the region where the destination bucket is stored
bucket_location = s3.meta.client.get_bucket_location(
    Bucket=bucket)['LocationConstraint']

# loop through the desired source files
for f in files_list:
    # get source file path
    src_path = os.path.join(local_directory, f)

    # specify the destination path inside the bucket
    dest_path = os.path.join(dest_directory, f)

    # upload the file 
    s3.meta.client.upload_file(src_path, bucket, dest_path,
                               ExtraArgs={'ACL': 'public-read'})
    print('Uploaded', f, 'with URL:')

    # get the url of the uploaded file. Prepare (Encode) it if necessary
    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location, bucket, dest_path)
    print(requests.Request('GET', object_url).prepare().url)
    print('=' * 30)

    print("preparing upload to redshift")

    # connect and create session
    con = psycopg2.connect(dbname=my_db,host=my_host,port=my_port,user=my_user,password=my_password) 
    cur = con.cursor() 
    table = pd.read_csv(src_path)

    '''
    Transfer files to redshift cluster
    '''

    # create a redshift table name
    string = f
    new_string = ""
    for i in string:
        if i != ".":
            new_string += i
        else:
            break
    table_name = new_string

    # create a redshift table
    sql_table = pd.io.sql.get_schema(table, table_name)
    cur.execute(sql_table)
    con.commit()
    cur.close()
    con.close()

    print("new table created")

    #transferring files from s3 to redshift table
    con = psycopg2.connect(dbname=my_db,host=my_host,port=my_port,user=my_user,password=my_password)
    cur = con.cursor()
    s3_location = 's3://{0}/{1}'.format(bucket, dest_path)
    table_name = f
    sql = "copy {table_name} from '{s3_location}' credentials 'aws_access_key_id={access_id};aws_secret_access_key={access_key} csv ignoreheader as 1 emptyasnull blanksasnull;".format(table_name=new_string, s3_location=s3_location, access_id =access_key, access_key=secret_key)

    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    print ("data uploaded to redshift table")