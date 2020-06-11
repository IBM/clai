import requests
import json

####
# inputs
####
username = 'TathagataChakraborti'

# from https://github.com/user/settings/tokens
token = 'afea48b59c3f41ad64380a39781e59d27498f85d'

url = "https://api.github.com/repos/IBM/clai/pulls"

# create a re-usable session object with the user creds in-built
gh_session = requests.Session()
gh_session.auth = (username, token)


open_pr_url = "https://api.github.com/repos/IBM/clai/pulls"
payload = { "title" : "Amazing new feature", 
            "body"  : "Please pull these awesome changes in!",
            "head"  : "github-bot",
            "base"  : "dummy"
}

comment_url = "https://api.github.com/repos/IBM/clai/issues/72/comments"
payload = { "body" : "Dummy PR" }


# get the list of repos belonging to me
repos = json.loads(gh_session.post(comment_url, json=payload).text)



# print the repo names
# for repo in repos:
#     print(repo)
 
# make more requests using "gh_session" to create repos, list issues, etc.
