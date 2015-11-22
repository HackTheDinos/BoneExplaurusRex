# -*- coding: utf-8 -*-
"""
    bone_explorer.es_service.ingest
    ~~~

    ingestion function for AWS lambda
"""

import urllib
import boto3
from models import Scan
from secrets import ELASTIC_SEARCH_CLUSTER_URI
from elasticsearch_dsl.connections import connections
from datetime import date, datetime
from dateutil.parser import parse as dateparse
from zipfile import ZipFile
import configparser


connections.create_connection(hosts=[ELASTIC_SEARCH_CLUSTER_URI])
print('Loading function')

s3 = boto3.client('s3')
config = configparser.ConfigParser()
TEMP_FILE_PATH = '/tmp/temp.zip'
S3_FILE_FORMAT = 'https://s3.amazonaws.com/{bucket}/{key}'

# map of types -> keys for the Scan model creation
scan_properties = {
    'string': {
        'genus',
        'species',
        'scientist',
        'institution',
        'faculty_archive',
    },
    'date': {
        'scan_date',
    }
}

# map of config section -> keys to extract for pca data
config_keys = {
    'CalibValue': {
        'averaging',
        'skip'
    },
    'Detector': {
        'timingval'
    },
    'Xray': {
        'current'
    },
    'Geometry': {
        'voxelsizex',
        'voxelsizey'
    }
}


def parse_config(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = 'N/A'
    return dict1


def _dateparse(datelike):
    if isinstance(datelike, datetime):
        return datelike
    if isinstance(datelike, date):
        return datetime.fromordinal(datelike.toordinal())
    return dateparse(datelike)


def _process_zip(response, key, bucket):
    zip_data = {}
    print("parsing the zip")
    # opent the content of the zip and stream the contents into a temp zip file
    with open(TEMP_FILE_PATH, 'w') as file_n:
        file_n.writelines(response['Body'].read())
    zfp = ZipFile(TEMP_FILE_PATH)
    print("zip read")

    # get the stl_files and pca_files
    stl_files = [f for f in zfp.namelist() if '.stl' in f]
    pca_files = [f for f in zfp.namelist() if '.pca' in f]

    if stl_files:
        # if they exist pull the first one and create an s3 object from it
        print("stl file exists!")
        stl_file = zfp.read(stl_files[0])
        stl_key = "{bucket}_{key}_stl.stl".format(bucket=bucket, key=key.split('.')[0])
        s3.put_object(
            Body=stl_file,
            Key=stl_key,
            Bucket=bucket,
            ACL='public-read'
        )

        # update the zip date with the uri for the stl_file
        zip_data.update(stl_uri=S3_FILE_FORMAT.format(bucket=bucket, key=stl_key))

    if pca_files:
        # if the pca file exists, extract its meaning data
        print("pca file exists!")
        pca_file = zfp.read(pca_files[0])
        config_file = config.read(pca_file)
        zip_data = {
            key: parse_config(config_file, section)[key]
            for section, keys in config_keys.iteritems()
            for key in keys
        }
    return zip_data


def ingest(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(
        event['Records'][0]['s3']['object']['key']
    ).decode('utf8')

    try:
        # grab the response
        response = s3.get_object(Bucket=bucket, Key=key)
        s3_uri = S3_FILE_FORMAT.format(
            bucket=bucket,
            key=key
        )

        zip_data = {}

        # set the permissions as public-read
        s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)
        metadata = response['Metadata']

        if metadata.get('parse_zip'):
            # only parse the zip if we want them
            zip_data = _process_zip(response, key, bucket)

        # get model's parameters from meta
        params = {
            key: metadata.get(key, 'N/A').lower()
            if t != 'date'
            else _dateparse(
                metadata.get(key, datetime.now())
            )
            for t, keys in scan_properties.iteritems()
            for key in keys
        }
        params.update(zip_data)

        scan = Scan(
            s3_uri=s3_uri,
            species_suggest=params['species'],
            genus_suggest=params['genus'],
            thumbnail_uri=S3_FILE_FORMAT.format(bucket=bucket, key=params['thumbnail_uri']),
            **params)
        print("saving the scan %s" % key)
        scan.save()

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
