from posixpath import split
import pandas as pd
import argparse
import os
import json

def main():
    args = get_args()
    output_file = args.output
    input_file = args.input
    stop_words = ["others", "ponies", "and", "all",]
    df = pd.read_csv(input_file, header = 0, usecols= ['title','pony'])
    char_network_dict = find_most_frequent_characters(df, stop_words)
    char_network_dict = build_network(df, char_network_dict)

    dir = os.path.dirname(output_file)
    if not (os.path.exists(dir)) and not (dir == ''):
        os.makedirs(dir)
    with open(output_file,'w') as f:
        json.dump(char_network_dict,f,indent = 2)


def build_network(df, char_network_dict):
    title = df['title'][0]
    char_speak_from = ""

    for index, row in df.iterrows():
        if row['title'] != title:
            title = row['title']
            char_speak_from = ""
            continue
            
        if row['pony'].lower() not in char_network_dict.keys():
            char_speak_from = ""
            continue

        if row['pony'].lower() == char_speak_from:
            continue

        if char_speak_from == "":
            char_speak_from = row['pony'].lower()
        else:
            char_network_dict[char_speak_from][row['pony'].lower()] += 1
            char_network_dict[row['pony'].lower()][char_speak_from] += 1
            char_speak_from = row['pony'].lower()
        
    return char_network_dict

def find_most_frequent_characters(df, stop_words):
    chars = {}
    for char in df['pony']:
        has_stop_words = False
        for word in stop_words:
            if word in char.lower().split(" "):
                has_stop_words = True
        
        if has_stop_words:
            continue

        if char.lower() not in chars.keys():
            chars[char.lower()] = 1
        else:
            chars[char.lower()] += 1
    sorted_chars = {k: v for k, v in sorted(chars.items(), key=lambda item: item[1],reverse= True)}
    char_list = list(sorted_chars.keys())[:101]

    #build dict base on the character list
    char_dict = {}
    for char in char_list:
        char_dict[char] = {}
        for other_char in char_list:
            if other_char == char:
                continue
            else:
                char_dict[char][other_char] = 0
    return char_dict

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output')
    parser.add_argument('-i','--input')
    return parser.parse_args()

if __name__ == "__main__":
    main()