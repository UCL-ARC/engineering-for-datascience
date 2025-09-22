from argparse import ArgumentParser
import os
import json
from .analysis import combine_dict

def combine_entry():
    parser = ArgumentParser(description="Process a collection or individual zip file")

    parser.add_argument('path')

    arguments = parser.parse_args()
    print(combiner(arguments.path))

def combiner(source):
    from functools import reduce, partial
    targets = list(map(partial(os.path.join, source),os.listdir(source)))
    def load_and_parse(path):
        return json.load(open(path))
    mapper = load_and_parse
    result = reduce(combine_dict,map(mapper, targets),{})
    return result