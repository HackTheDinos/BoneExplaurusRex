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

S3_FILE_FORMAT = 'https://s3.amazonaws.com/{bucket}/{key}'
scan_properties = {
    'string': {
        'genus',
        'species',
        'scientist',
        'institution',
        'thumbnail_key',
        'faculty_archive',
    },
    'date': {
        'scan_date',
    }
}

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
    with open('temp.zip', 'w') as file_n:
        file_n.writelines(response['Body'])
    zfp = ZipFile('temp.zip')
    print("zip read")
    stl_files = [f for f in zfp.namelist() if '.stl' in f][0]
    pca_files = [f for f in zfp.namelist() if '.pca' in f][0]
    if stl_files:
        print("stl file exists!")
        stl_file = zfp.read(stl_files[0])
        stl_key = "{bucket}{key}_stl".format(bucket=bucket, key=key)
        s3.put_object(
            Body=stl_file,
            Key=stl_key,
            Bucket=bucket
        )
        zip_data.update(stl_uri=S3_FILE_FORMAT.format(bucket=bucket, key=key))
    if pca_files:
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
        response = s3.get_object(Bucket=bucket, Key=key)
        s3uri = S3_FILE_FORMAT.format(
            bucket=bucket,
            key=key
        )
        zip_data = {}
        s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)
        metadata = response['Metadata']
        if metadata.get('parse_zip'):
            zip_data = _process_zip(response, key, bucket)

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
            s3uri=s3uri,
            species_suggest=params['species'],
            genus_suggest=params['genus'],
            **params)
        scan.save()

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
