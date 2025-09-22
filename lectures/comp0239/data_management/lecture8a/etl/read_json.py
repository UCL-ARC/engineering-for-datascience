from chemistry import DeSerialiseStructure
import json

if __name__ == '__main__':
    system = DeSerialiseStructure()
    with open('serialised.json') as json_file:
        json_struct = json.load(json_file)
        s = system.parse_system(json_struct)
        print(s.to_struct())