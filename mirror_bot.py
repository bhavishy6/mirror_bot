import praw
import re

def mirrors_requested(c):
    text = c.body()
    if text.find("find mirrors") or text.find("all mirrors"):
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


if __name__ == '__main__':
    user_agent = ("Mirror Finder 1.0 by u/bhavishy6")
    r = praw.Reddit(user_agent=user_agent,client_id='Mpv45Va9NRiFJQ',
                        client_secret='tbk0w4c0chto1YVHYW7Tch0EmaM',
                        redirect_url='http://127.0.0.1:65010/authorize_callback')

    r.login()
    while True:
        for c in praw.helpers.comment_stream(r, 'hiphopheads'):
            if check_comment_for_mirrors(c.body):
                print "Mirror Found..."
                bot_action(c)
