import snscrape.modules.twitter as sntwitter

username = "elcomerciocom"  # Replace with any Twitter username

# Get user info
user = sntwitter.TwitterUserScraper(username).entity

print(f"Username: {user.username}")
print(f"Display name: {user.displayname}")
print(f"Followers: {user.followersCount}")
print(f"Following: {user.friendsCount}")
print(f"Tweets: {user.statusesCount}")
print(f"Likes: {user.favouritesCount}")
print(f"Account created at: {user.created}")
