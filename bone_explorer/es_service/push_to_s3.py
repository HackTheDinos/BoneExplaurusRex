# -*- coding: utf-8 -*-
"""

Script to push zips to s3. The file is divided into sections that do a few
different functions. 

The section for "push zips to s3" is the main section which actually pushes
the zip files to S3 given meta data about each species.

"""

import boto3
import os
import requests

#%% initialize 
session = boto3.session.Session(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                      region_name='us-east-1')
client = session.client('s3',use_ssl=False)

#%% print file contents
response = client.list_objects(Bucket='ctscans')
for content in filter(lambda c: '/' in c, response['Contents']):
    content['Key']

#%% push thumbnails to s3
genus_s3thumb = {}
for fname in filter(lambda f: f.endswith('.jpg'), os.listdir('.')):
    print 'pushing', fname
    genus = fname[:-4]
    response = client.put_object(
        ACL='public-read',
        Body=open(fname,'rb'),
        Bucket='ctscans',
        Key=fname,
        Metadata={
            'genus':genus,
        }
        )
    genus_s3thumb[genus]=fname
    
#%% push thumbnails to s3
genus_s3stl = {}
for fname in filter(lambda f: f.endswith('.stl'), os.listdir('.')):
    print 'pushing', fname
    genus = fname[:-4]
    response = client.put_object(
        ACL='public-read',
        Body=open(fname,'rb'),
        Bucket='ctscans',
        Key=fname,
        Metadata={
            'genus':genus,
        }
        )
    genus_s3stl[genus]=fname

#%% push zips to s3
all_genus = [{'genus':'Anas', 'species':'platyrhynchos','scan_date':'1998-05-12', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'0035'},
             {'genus':'Gavia', 'species':'immer','scan_date':'2005-03-25', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'1202'},
             {'genus':'Alioramus', 'species':'remotus','scan_date':'2009-21-01', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'1997'},
             {'genus':'Chordeiles', 'species':'minor','scan_date':'2005-02-10', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'0968'},
             {'genus':'Brotogeris', 'species':'chrysopterus','scan_date':'2004-06-01', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'1032'},             
             {'genus':'Coragyps', 'species':'atratus','scan_date':'2004-02-03', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'0964'},             
             {'genus':'Melanerpes', 'species':'aurifrons','scan_date':'2004-04-05', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'0998'},
             #{'genus':'Grus', 'species':'canadensis','scan_date':'2004-02-06', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'0966'},
             #{'genus':'fregata', 'species':'magnificens','scan_date':'2004-06-01', 'institution':'University of Texas', 'scientist':'Dr. Timothy Rowe', 'faculty archive':'1032'},
             ]

for genus in all_genus:
    print 'pushing', genus['genus']+'.zip'
    response = client.put_object(
        ACL='public-read',
        Body=open(genus['genus']+'.zip','rb'),
        Bucket='ctscans',
        Key=genus['genus']+'.zip',
        Metadata={
            'genus':genus['genus'],
            'species':genus['species'],
            'genus_suggest':genus['genus'],
            'species_suggest':genus['species'],
            's3uri':genus['genus']+'.zip',
            'scan_date':genus['scan_date'],
            'scientist':genus['scientist'],
            'institution':genus['institution'],
            'thumbnail_uri':genus_s3thumb[genus['genus']],
            'faculty_archive':genus['faculty archive'],
            'stl_uri':genus_s3stl[genus['genus']],
            'parse_zip':'True'
        }
        )
        
#%% delete zips from s3
for fname in filter(lambda f: f.endswith('.zip'), os.listdir('.')):
    response = client.delete_object(Bucket='ctscans', Key=fname)
    
#%% delete from ES
url = 'https://wtfk1moh2k:hwf9jytoe8@boneexplorus-7582625496.us-east-1.bonsai.io/'
index = 'ct_scans/'
type_ = 'scan'
r = requests.delete(url+index+'_mapping/'+type_)
print r.json()
