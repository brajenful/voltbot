import praw
import random

reddit = praw.Reddit(client_id='JJrbtPLCsJtlUg',
					 client_secret='vG5yd1MZU-3IQydAlRJFd-Bmdt4',
					 user_agent='windows:voltbot:v1.0 (by /u/Volt69)')

time_filters = ['week','month','year', 'all']
subreddits = ['unethicallifeprotips', 'lifeprotips']

def get_top_posts(subreddit, time_filter):
	submissions = []
	for submission in reddit.subreddit(subreddit).top(time_filter):
		submissions.append(submission)
	return submissions

def get_tip():
	index = random.randint(0, len(time_filters)-1)
	time_filter = time_filters[index]
	subreddit = random.randint(0, len(subreddits)-1)
	posts = get_top_posts(subreddits[subreddit], time_filter)
	index = random.randint(0, len(posts)-1)
	post = posts[index]
	return post.title[5:]

def get_user(name:str)->object:
	return reddit.redditor(name)

def get_user_comments(name:str, limit)->list:
	return [comment.body for comment in get_user(name).comments.new(limit=limit)]

def get_random_comment(user:object)->str:
	comments = [comment.body for comment in user.comments.new(limit=None)]
	return random.choice(comments)

def get_random_user_comment(username:str)->str:
	return get_random_comment(get_user(username))
