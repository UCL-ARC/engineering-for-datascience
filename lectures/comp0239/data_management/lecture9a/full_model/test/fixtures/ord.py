import os
from ord_schema.proto.reaction_pb2 import Reaction

fixtures = os.path.dirname(__file__)
small = os.path.join(fixtures, 'ord', '00','ds_fix_1.pb.gz')
folder = os.path.join(fixtures, 'ord')

repeated = os.path.join(fixtures, 'repeated_input.pb')
both = os.path.join(fixtures, 'both_sides.pb')

from google.protobuf import text_format
repeated_input = Reaction()
text_format.Parse(text = open(repeated).read(), message=repeated_input)

both_sides = Reaction()
text_format.Parse(text = open(both).read(), message=both_sides)