import pandas as pd
import argparse
import random
import json
import os

def main():
    args = getArgs()
    outputfile_name = args.output
    json_file = args.json_file
    num_posts = args.num_posts_to_output
    dir = os.path.dirname(outputfile_name)
    if not (os.path.exists(dir)):
        os.makedirs(dir)

    # check num_posts and file length
    num_lines = sum(1 for line in open(json_file))
    num_posts = min(num_lines, num_posts)

    # building dataframe 
    selected_posts_indices = random.sample(range(num_lines),num_posts) 
    df = build_dataframe(json_file, selected_posts_indices)
    df.to_csv(outputfile_name, sep="\t",index= False,header=True)



def build_dataframe(json_file, indices):
    i = 0
    name = []
    title = []
    with open(json_file) as f:
        for line in f:
            try:
                post = json.loads(line)
            except:
                i += 1
                continue
            if i in indices:
                title.append(post['data']['title'])
                name.append(post['data']['name'])
            else:
                i += 1
                continue
            i += 1
    f.close()
    dict = {'Name': name, 'title': title,}
    df = pd.DataFrame(data=dict)
    df['coding'] = ""
    return df
            
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output')
    parser.add_argument('json_file')
    parser.add_argument('num_posts_to_output',type=int)
    return parser.parse_args()

if __name__ == '__main__':
    main()