from steem import Steem
from steembase import exceptions
import keys
import time

node = ["https://api.steemit.com"]
identifier = []

s = Steem(node,keys=keys.keys)

def get_newest_post(username):
    newest_post = s.get_discussions_by_blog({"limit":1,"tag":username})
    if(newest_post!=[]):
        return newest_post[0]["author"],newest_post[0]["permlink"]
    else:
        return None


def get_voter(default_account,permalink):
    votes = s.get_active_votes(default_account,permalink)
    voter = []
    for i in votes:
        if (i["voter"] != default_account):
            voter.append(i["voter"])
    return voter

def upvote_newest_post(usernames,default_account):
    upvote_post = get_identifier(usernames)
    for i in upvote_post:
        try:
            s.commit.vote(identifier=i, weight=100, account=default_account)
        except exceptions.RPCError:
            pass

def get_identifier(usernames):
    for i in usernames:
        post = get_newest_post(i)
        if (post!=None):
            post = post[1]
            identifier.append(i+"/"+post)
    return identifier


def comment(body,default_account,reply_identifier):
    time.sleep(25)
    s.post("",body,default_account, reply_identifier=reply_identifier)

def comment_on_newest_post(body,default_account,usernames):
    reply_identifier = get_identifier(usernames)
    for i in reply_identifier:
        comment(body,default_account,i)
