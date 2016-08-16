import praw
import re
import config_bot
import os

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
        comment_links = []
        comment_links = check_comment_for_mirrors(comment)

        if len(comment_links) > 0:
            for link in comment_links:
                print "LINK FOUND" + link
                links.append(link)


    if respond:
        reply(c, links, respond=True)

def check_comment_for_mirrors(c):
    text = c.body
    links = []

    if text.find("mirror") > -1:
        print "[MIRROR FOUND?]: " + text
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

        # pattern = re.compile('href="(.*?)"')
        # links = pattern.findall(text)

    return links

def reply(c, links, respond=False):
    target_submission = r.get_submission(submission_id=c.submission.id)


    reply_header = "Mirrors Found:\n"
    reply_body = ",".join(links)

    print reply_header + reply_body
    if respond:
        c.reply(reply_header + reply_body)


if __name__ == '__main__':

    user_agent = ("Auto Mirror Finder 1.0 by u/bhavishy6")
    r = praw.Reddit(user_agent=user_agent,client_id=config_bot.CLIENT_ID,
                        client_secret=config_bot.CLIENT_SECRET,
                        redirect_url=config_bot.REDIRECT_URL)

    r.login(config_bot.REDDIT_USERNAME, config_bot.REDDIT_PASS)
    subreddit = r.get_subreddit('hiphopheads')



    for c in praw.helpers.comment_stream(r, 'hiphopheads'):
        if mirrors_requested(c):
            bot_action(c, respond=True)
