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


connections.create_connection(hosts=[ELASTIC_SEARCH_CLUSTER_URI])
print('Loading function')

s3 = boto3.client('s3')

scan_properties = {
    'string': {
        'genus',
        'species',
        'scientist',
        'institution',
        'thumbnail_key',
    },
    'date': {
        'scan_date',
        'dig_date'
    }
}


def _dateparse(datelike):
    if isinstance(datelike, datetime):
        return datelike
    if isinstance(datelike, date):
        return datetime.fromordinal(datelike.toordinal())
    return dateparse(datelike)


def ingest(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(
        event['Records'][0]['s3']['object']['key']
    ).decode('utf8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        s3uri = 'https://s3.amazonaws.com/{bucket}/{key}'.format(
            bucket=bucket,
            key=key
        )
        s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)
        metadata = response['Metadata']
        params = {
            key: metadata.get(key, 'N/A').lower()
            if t != 'date'
            else _dateparse(
                metadata.get(key, datetime.now())
            )
            for t, key in scan_properties.iteritems()
        }

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
