import praw
user_agent = "Mirror Finder 1.0 by u/bhavishy6"
r = praw.Reddit(user_agent=user_agent);

r.login()

for c in praw.helpers.comment_stream(r, 'hiphopheads'):
    if mirrors_requested(c):
        do(c)


def mirrors_requested(c):
    text = c.body()
    if text.find("find mirrors") or text.find("all mirros"):
        return True

def reply(c, verbose=True, respond=False):

    if verbose:
        print c.body.encode("UTF-8")
        print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"

    if respond:
        print ""
