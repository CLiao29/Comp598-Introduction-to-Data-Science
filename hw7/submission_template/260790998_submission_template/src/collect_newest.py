import requests
import json
import os,sys
import argparse

def main():
    args = getArgs()
    subreddit_name = args.subreddit
    outputfile_name = args.output
    dir = os.path.dirname(outputfile_name)
    if not (os.path.exists(dir)):
        os.makedirs(dir)
    
    headers = {'User-Agent': 'CollectScript/0.0.1'}
    app_id = 'MeNSlVvAx4UpGHsuBYIUkQ'
    secret = 'm60dC6VfeDFhTXzs5fm-l-HjNwCCAQ'
    headers = auth(app_id,secret,headers) 
    
    collectPosts(headers,outputfile_name, subreddit_name)

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-s', '--subreddit')
    return parser.parse_args()

def collectPosts(headers,outputFilename,subreddit):
    first_write = True
    api = 'https://oauth.reddit.com'
    link = '{}/r/' + subreddit + '/new'
    r = requests.get(link.format(api), headers=headers, params={'limit': '100'})
    root_element = r.json()
    posts = root_element['data']['children']
    for post in posts:
        if first_write == True:
            with open(outputFilename, 'w', newline='\r\n') as json_file:
                json.dump(post, json_file)
                json_file.write("\n")
                first_write = False;
        else:
            with open(outputFilename, 'a', newline='\r\n') as json_file:
                json.dump(post, json_file)
                json_file.write("\n")

def auth(app_id,secret,headers):
    auth = requests.auth.HTTPBasicAuth(app_id, secret)
    reddit_username = 'TomorrowCrafty2996'
    reddit_password = '199904231cm'
    data = {
    'grant_type': 'password',
    'username': reddit_username,
    'password': reddit_password
    }
    res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    headers['Authorization'] = 'bearer {}'.format(token)
    r = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    return headers
    

if __name__ == '__main__':
    main()

