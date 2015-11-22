# -*- coding: utf-8 -*-
"""
    bone_explorer.es_service.models
    ~~~~

    Elastic Search Models
"""

from elasticsearch_dsl import DocType, String, Date


class Document(DocType):
    genus = String()
    species = String()
    date_scanned = Date()
    filename = String()

    class Meta:
        index = 'ct_scans'
