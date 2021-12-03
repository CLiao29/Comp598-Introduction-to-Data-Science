import argparse
import pandas as pd
import json
import os

def main():
    args = getArgs()
    inputfile_name = args.input
    outputfile_name = args.output

    df = pd.read_csv(inputfile_name,header = 0, sep = '\t')
    
    json_dict = make_json(df)
    if outputfile_name == None:
        print(json_dict)
    else:
        dir = os.path.dirname(outputfile_name)
        if not (os.path.exists(dir)):
            os.makedirs(dir)
        with open (outputfile_name,'w') as f:
            json.dump(json_dict,f,indent=2)

def make_json(df):
    course = len(df[df['coding'] == 'c'])
    food = len(df[df['coding'] == 'f'])
    residence = len(df[df['coding'] == 'r'])
    other = len(df[df['coding'] == 'o'])
    dict = {'course-related': course, 'food-related': food, 'residence-related': residence, 'other': other}
    return dict
    


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input')
    parser.add_argument('-o','--output')
    return parser.parse_args()

if __name__ == '__main__':
    main()
