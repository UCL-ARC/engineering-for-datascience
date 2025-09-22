from ..analysis import *

import pytest
import os

def test_can_analyse_file():
    fixture = os.path.join(os.path.dirname(__file__),
        'fixtures','collection',
        '99442.zip')
    result = analyse_file('arms', fixture)
    assert result["1851"] == 9

def test_can_analyse_collection():
    fixture = os.path.join(os.path.dirname(__file__),
        'fixtures','collection')
    result = analyse_collection(fixture, 'arms')
    print(result)
    assert result["1851"] == 9
    assert result["1852"] == 79

def test_can_analyse_collection_parallel():
    fixture = os.path.join(os.path.dirname(__file__),
        'fixtures','collection')
    result = analyse_collection(fixture, 'arms', True)
    print(result)
    assert result["1851"] == 9
    assert result["1852"] == 79

def test_can_analyse_spark_s2():
    import pyspark
    context = pyspark.sql.SparkSession.builder.master("local").appName('S3Example').getOrCreate().sparkContext
    result = analyse_spark("s3://comp0235-ucgajhe/676204.zip",context,'arms')
    assert result["1851"] == 9
    assert result["1852"] == 79