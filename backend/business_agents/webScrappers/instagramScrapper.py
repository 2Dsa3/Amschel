import time
import instaloader


L = instaloader.Instaloader()
L.load_session_from_file("mds787366")


def scrape_instagram_profile(username: str):
    profile = instaloader.Profile.from_username(L.context, username)
    return profile.followers, profile.followees


# for post in profile.get_posts():
#     print(post.url)
#     time.sleep(10) 