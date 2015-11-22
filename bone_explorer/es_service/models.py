# -*- coding: utf-8 -*-
"""
    bone_explorer.es_service.models
    ~~~~

    Elastic Search Models
"""

from elasticsearch_dsl import (
    DocType, String, Completion, Date, Float
)


class Scan(DocType):
    genus = String()
    species = String()
    s3uri = String()
    genus_suggest = Completion(
        analyzer='simple',
        payloads=True,
        perserve_seperators=True,
        perserve_position_increments=True,
        max_input_length=50
    )
    species_suggest = Completion(
        analyzer='simple',
        payloads=True,
        perserve_seperators=True,
        perserve_position_increments=True,
        max_input_length=50
    )
    scan_date = Date()
    scientist = String()
    institution = String()
    thumbnail_key = String()
    faculty_archive = String()
    sti_url = String()
    averaging = Float()
    skip = Float()
    timingval = Float()
    current = Float()
    voxelsizex = Float()
    voxelsizey = Float()

    class Meta:
        index = 'ct_scans'
