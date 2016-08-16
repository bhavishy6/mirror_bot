import praw
import re
import config_bot

def mirrors_requested(c):
    text = c.body
    if text.find("find mirrors") > -1 or text.find("all mirrors") > -1:
        print text
        print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        return True


def bot_action(c, respond=True):
    print "bot_action"
    links = []
    target_submission = r.get_submission(submission_id=c.submission.id)
    print "Submission: " + target_submission.short_link

    target_submission.replace_more_comments(limit=None, threshold=0)

    flat_comments = praw.helpers.flatten_tree(target_submission.comments)

    print "comments in submission", len(flat_comments)

    for comment in flat_comments:
        found_links = check_comment_for_mirrors(comment)
        if found_links > 0:
            for link in found_links:
                links.append(link)
        else:
            print "no links in this: " + comment.body

    if respond:
        for l in links:
            print l
    # for c in praw.helpers.flatten_tree(submission.comments):
    #     for link in check_comment_for_mirrors(c):
    #         print "[bot_action]: mirror_found: " + link
    #         links.append(link)
    #
    # if len(links) > 0:
    #     for link in links:
    #         print link
    #     # reply(links, verbose ,respond)



def reply(links, verbose=True, respond=False):
    if verbose:
        print c.body.encode("UTF-8")
        print "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"

    if respond:
        print "Mirrors Found:\n"
        for link in links:
            print link + "\n"


def check_comment_for_mirrors(c):
    text = c.body
    links = []

    if text.find("mirror") > 0:
        print "[MIRROR FOUND?]: " + text
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

        # pattern = re.compile('href="(.*?)"')
        # links = pattern.findall(text)

    return links


if __name__ == '__main__':
    user_agent = ("Mirror Finder 1.0 by u/bhavishy6")
    r = praw.Reddit(user_agent=user_agent,client_id=config_bot.CLIENT_ID,
                        client_secret=config_bot.CLIENT_SECRET,
                        redirect_url=config_bot.REDIRECT_URL)

    # r.login(REDDIT_USERNAME, REDDIT_PASS)
    subreddit = r.get_subreddit('hiphopheads')

    for c in praw.helpers.comment_stream(r, 'hiphopheads'):
        if mirrors_requested(c):
            # print c.body
            bot_action(c, respond=True)
