import json
import os
import argparse
import math

def main():
    args = get_args()
    pony_count = args.pony_counts
    num_words  = args.num_words

    with open(pony_count) as f:
        dict = json.load(f)
    
    json_dict = compute_json_dict(dict,num_words,)
    print(json.dumps(json_dict,indent = 2))

    
def compute_json_dict(dict,num_words):
    json_dict = {"twilight sparkle": [],
                 "applejack": [],
                 "rarity": [],
                 "pinkie pie": [],
                 "rainbow dash": [],
                 "fluttershy": []}
    
    for pony in dict.keys():
        pony_list = []
        pony_stats = {}
        for word in dict[pony]:
            n = tf_idf(word,pony,dict)
            pony_stats[word] = n
        
        pony_stats = sorted(pony_stats.items(), key=lambda x : x[1], reverse=True)
        if num_words >= len(pony_stats):
            for (word,tfidf) in pony_stats:
                pony_list.append(word)
            json_dict[pony] = pony_list
        else:
            count = 0
            for (word,tfidf) in pony_stats:
                if count >= num_words:
                    break
                pony_list.append(word)
                count += 1
            json_dict[pony] = pony_list
    
    return json_dict

    
def tf_idf(w,pony,script):
    return tf(w,script[pony]) * idf(w,script)

def tf(w,pony):
    for key,count in pony.items():
        if key == w:
            return count
    return 0
    
def idf(w, script):
    pony_count = 0
    for pony,pony_dict in script.items():
        if w in pony_dict.keys():
            pony_count += 1
    return math.log10( len(script.keys()) / pony_count) 
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--pony_counts')
    parser.add_argument('-n','--num_words',type= int)
    return parser.parse_args()


if __name__ == "__main__":
    main()