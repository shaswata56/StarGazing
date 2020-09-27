import os
import json
import requests

# User Credes for Auth
USERNAME = "yourusername"
PASSWORD = "y0urp455w0rd"

# Your Personal Access Token for Auth
ACCESS_TOKEN = "ed086f8c40e47410498551c08dfe56feaef046df"

# Usernames to starred
REPO_OWNERS = ["torvalds", "shaswata56"]

def main():
    session = select_auth()
    starring_all(sess=session, owners=REPO_OWNERS)

def select_auth():
    selection = input('Select an Authentication:\n1 - Password\n2 - Access Token\n: ')
    if selection == '1':
        session = auth(token=False)
        return session
    elif selection == '2':
        session = auth(token=True)
        return session
    else:
        return select_auth()

def auth(token: bool):
    sess = requests.Session()
    sess.headers.update({'Accept': 'application/vnd.github.v3+json'})
    if token:
        sess.headers.update({'Authorization': 'token %s' % ACCESS_TOKEN})
    else:
        sess.auth = (USERNAME, PASSWORD)
    return sess

def isStarred(res: requests.Response):
    if res.status_code == 204:
        return True
    else:
        return False

def starring_all(sess: requests.Session, owners=REPO_OWNERS):
    for owner in owners:
        repos = get_repositories(sess=sess, owner=owner)
        for repo in repos:
            give_a_star_on(sess=sess, owner=owner, repo=repo)

def get_repositories(sess: requests.Session, owner=None):
    repositories = []
    remaining = True
    params = {'page': 1, 'per_page': 100}
    url = 'https://api.github.com/users/%s/repos' % (owner)
    while remaining:
        res = sess.get(url, params=params)
        for repo in res.json():
            repositories.append(repo['name'])
        if 'next' in res.links:
            url = res.links['next']['url']
            params = None
        else:
            remaining = False
    return repositories

def give_a_star_on(sess: requests.Session, owner, repo):
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

if __name__ == "__main__":
    main()