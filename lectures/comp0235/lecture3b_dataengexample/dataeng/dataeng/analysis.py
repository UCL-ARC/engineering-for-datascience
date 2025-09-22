
from lxml import etree
from zipfile import ZipFile
from json import dumps
import os
from argparse import ArgumentParser

def analysis_entry():
    parser = ArgumentParser(description="Process a collection or individual zip file")

    parser.add_argument('path')
    parser.add_argument('target_word')
    parser.add_argument('--parallel', action='store_true')

    arguments = parser.parse_args()

    # if the path is to a folder, then extract the names of the zip files in it, analyse each, and combine the results
    if os.path.isdir(arguments.path):
        results = analyse_collection(arguments.path, arguments.target_word, arguments.parallel)
    else: 
        results = analyse_file(arguments.target_word, arguments.path)

    print(dumps(results))

def analyse_file(target_word, source):
    try:
        with ZipFile(source) as zip:
            index_file = [name for name in zip.namelist() if "metadata" in name][0]
            with zip.open(index_file) as metadata:
                tree=etree.parse(metadata)
                date = tree.find('.//{http://www.loc.gov/mods/v3}dateIssued').text
            # for each other file in the ALTO xml
            other_files = [name for name in zip.namelist() if "metadata" not in name and name != "ALTO/"]
            count = 0
            for filename in other_files:
                with zip.open(filename) as file:
                    tree=etree.parse(file)
                    text = tree.findall(f".//String[@CONTENT='{target_word}']")
                    count += len(text)
        return {date: count}
    except AttributeError:
        return {"": 0}

def combine_dict(dict1, dict2):

    for key in dict2:
        if key in dict1:
            dict1[key]+=dict2[key]
        else:
            dict1[key] = dict2[key]

    return dict1

def analyse_collection(source, target_word, parallel=False):

    from functools import reduce, partial
    targets = list(map(partial(os.path.join, source),os.listdir(source)))
    mapper = partial(analyse_file, target_word)
    
    if parallel:
        import mr4mp
        pool = mr4mp.pool(2*os.cpu_count())
        result = pool.mapreduce(mapper, combine_dict, targets)
    else:

        result = reduce(combine_dict,map(mapper, targets),{})
    return result

def analyse_spark(source, spark_context, target_word):
    from functools import partial
    from io import BytesIO
    zipFiles = spark_context.binaryFiles(source).map(lambda x: BytesIO(x[1]))
    # This makes an RDD, with all the files slurped to the appropriate thread in parallel
    # The binaryFiles function returns pairs of paths and strings. Our analyse file function expects a file-like object
    # so we wrap in BytesIO
    # It doesn't actually run until we dispatch to spark with collect() or reduce()
    mapper = partial(analyse_file, target_word)
    return zipFiles.map(mapper).reduce(combine_dict)
