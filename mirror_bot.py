import re

def mirrors_requested(c):
    text = c.body()
    if text.find("find mirrors") or text.find("all mirros"):
        return True


def bot_action(c, verbose=True, respond=False):
    links = []
    submission = c.submission
    for c in praw.helpers.flatten_tree(submission.comments):
        for link in check_comment_for_mirrors(c.body):
            links.append(link)

    if len(links) > 0:
        reply(links, verbose ,respond)


def reply(links, verbose=True, respond=False):
    if verbose:
        print c.body.encode("UTF-8")
        print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"

    if respond:
        print "Mirrors Found:\n"
        for link in links:
            print link + "\n"


def check_comment_for_mirrors(text):
    if text.find("mirror"):
        pattern = re.compile('href="(.*?)"')
        links = pattern.findall(text)

    return links


if __name__ is '__main__':
    import praw
    r = praw.Reddit(user_agent);
    user_agent = "Mirror Finder 1.0 by u/bhavishy6"

    r.login()
    for c in praw.helpers.comment_stream(r, 'hiphopheads'):
        if mirrors_requested(c):
            bot_action(c)
