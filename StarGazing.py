import os
import time
import json
import requests

# User Credes for Auth
USERNAME = "yourusername"
PASSWORD = "y0urp455w0rd"

# Usernames to starred
REPO_OWNERS = ["shaswata56", "torvalds"]

def auth():
    sess = requests.Session()
    sess.auth = (USERNAME, PASSWORD)
    return sess

def isStarred(res: requests.Response):
    if res.status_code == 204:
        return True
    else:
        return False

def starring_all(sess: requests.Session, owners=REPO_OWNERS):
    for owner in owners:
        repos = get_repositories(sess=session, owner=owner)
        for repo in repos:
            give_a_star_on(sess=sess, owner=owner, repo=repo)

def get_repositories(sess: requests.Session, owner=None):
    repositories = []
    url = 'https://api.github.com/users/%s/repos' % (owner)
    res = sess.get(url).json()
    for repo in res:
        repositories.append(repo['name'])
    return repositories

def give_a_star_on(sess: requests.Session, owner, repo):
    time.sleep(1)
    url = 'https://api.github.com/user/starred/%s/%s' % (owner, repo)
    starred = isStarred(sess.get(url))

    if starred:
        print('You\'ve Already Starred {}/{} !'.format(owner, repo))
    else:
        res = sess.put(url)
        if res.status_code == 204:
            print('Starred {}/{} successfully!'.format(owner, repo))
        else:
            print('Could not starred {}/{} :('.format(owner, repo))
            print('Response:', res.content)

session = auth()
starring_all(sess=session, owners=REPO_OWNERS)