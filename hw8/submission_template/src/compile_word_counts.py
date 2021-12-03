import pandas as pd
import json
import argparse
import os,sys

def main():
    args = get_args()
    output_file = args.output
    dialog_file = args.dialog

    word_count_dict  = word_count(dialog_file)

    dir = os.path.dirname(output_file)
    if not (os.path.exists(dir)) and not (dir == ''):
        os.makedirs(dir)
    with open(output_file,'w') as f:
        json.dump(word_count_dict,f,indent = 2)


def word_count(dialog_file):
    #load stop words
    stopwords = load_stopwords()

    df = pd.read_csv(dialog_file,header=0, usecols= ['pony','dialog'])
    punctuation = ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']
    dict = {"twilight sparkle": {},
            "applejack": {},
            "rarity": {},
            "pinkie pie": {},
            "rainbow dash": {},
            "fluttershy": {}}
    
    for pony in dict.keys():
        dirty_dict = {}
        df_for_pony = df.loc[df['pony'].str.contains("^" + pony + "$",case = False, regex = True)]
        for line in df_for_pony['dialog']:
            dialog_without_punctuation = ''.join(' ' if c in punctuation else c for c in line)
            words = dialog_without_punctuation.split()
            for word in words:
                if not word.isalpha():
                    continue
                if word.upper() in (sw.upper() for sw in stopwords):
                  continue
                if word.lower() in dirty_dict:
                    dirty_dict[word.lower()] += 1
                else:
                    dirty_dict[word.lower()] = 1
        dict[pony] = dirty_dict
    return clean_word_count(dict)
        
def load_stopwords():
    f = open('data/stopwords.txt')
    stopwords = []
    for line in f:
        if '#' in line:
            continue
        else:
            stopwords.append(line.strip())
    f.close()
    return stopwords
    
def get_args():
    parser = argparse.ArgumentParser();
    parser.add_argument('-o','--output');
    parser.add_argument('-d','--dialog');
    return parser.parse_args()

def clean_word_count(dict):
    #keep words that occur at least 5 times across ALL valid speech acts
    return_dict = {}
    for pony in dict.keys():
        for word,count in dict[pony].items():
            all_count = count
            for other_pony in dict.keys():
                if other_pony == pony:
                    continue
                if word in dict[other_pony].keys():
                    all_count += dict[other_pony][word]
            if all_count < 5:
                dict[pony][word] = -1
        return_dict[pony] = { k:v for k,v in dict[pony].items() if v != -1}
    return return_dict
    


if __name__ == "__main__":
    main()