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

connections.create_connection(hosts=[ELASTIC_SEARCH_CLUSTER_URI])
print('Loading function')

s3 = boto3.client('s3')


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
        genus = response['Metadata'].get('genus', 'N/A')
        species = response['Metadata'].get('species', 'N/A')
        params = dict(
            species=species,
            species_suggest=species,
            genus=genus,
            genus_suggest=genus
        )
        scan = Scan(s3uri=s3uri, **params)
        scan.save()

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
