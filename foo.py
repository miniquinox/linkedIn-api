import json
import time
from linkedin_api import Linkedin

def fetch_linkedin_posts(username, num_posts, email, password):
    # Initialize the LinkedIn API
    api = Linkedin(email, password)

    # Fetching posts logic using the correct method
    posts = api.get_profile_posts(public_id=username, post_count=num_posts)

    processed_posts = []
    for idx, post in enumerate(posts):
        # Inline logic to get LinkedIn link
        post_urn = post['updateMetadata']['urn']
        link_to_post = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_urn.split(':')[-1]}/"

        # Inline logic to extract post details
        post_data = {
            "idx": idx,
            "User": post['actor']['name']['text'],
            "Link to Post": link_to_post,
            "Post Content": post.get('commentary', {}).get('text', {}).get('text', ''),
            "Likes": post['socialDetail']['totalSocialActivityCounts']['numLikes'],
            "Comments": post['socialDetail']['totalSocialActivityCounts']['numComments'],
            # Include other relevant fields as needed
        }
        processed_posts.append(post_data)

    return processed_posts

username = "williamhgates"
num_posts = 1000
email = "quinocarreteromartinez@gmail.com"
password = "Quinito98"
data = fetch_linkedin_posts(username, num_posts, email, password)
print(data)