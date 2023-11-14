import argparse
from linkedin_api import Linkedin
import json
import time

def get_linkedin_link(urn):
    post_id = urn.split(':')[-1]
    return f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

def extract_post_details(post, idx):
    post_data = {
        "idx": idx,
        "User": post['actor']['name']['text'],
        "Link to Post": get_linkedin_link(post['updateMetadata']['urn']),
        "Post Description": post['commentary']['text']['text'] if 'commentary' in post else "No posts",
        "Likes": post['socialDetail']['totalSocialActivityCounts']['numLikes'],
        "Shares": post['socialDetail']['totalSocialActivityCounts']['numShares'],
        "Number of Comments": post['socialDetail']['totalSocialActivityCounts']['numComments']
    }

    if 'resharedUpdate' in post:
        original_post = post['resharedUpdate']
        post_data["Repost"] = {
            "Original User": original_post['actor']['name']['text'],
            "Original Link to Post": get_linkedin_link(original_post['updateMetadata']['urn']),
            "Original Post Description": original_post['commentary']['text']['text'] if 'commentary' in original_post else "No posts",
            "Original Likes": original_post['socialDetail']['totalSocialActivityCounts']['numLikes'],
            "Original Shares": original_post['socialDetail']['totalSocialActivityCounts']['numShares'],
            "Original Number of Comments": original_post['socialDetail']['totalSocialActivityCounts']['numComments']
        }

    return post_data

def main(username):
    start_time = time.time()  # Start the timer

    api = Linkedin('quinocarreteromartinez@gmail.com', 'Quinito98')
    posts = api.get_profile_posts(public_id=username, post_count=1000)
    processed_posts = [extract_post_details(post, idx) for idx, post in enumerate(posts, start=1) if extract_post_details(post, idx)]

    file_name = f"{username}.json"
    with open(file_name, 'w') as file:
        json.dump(processed_posts, file, indent=4)

    elapsed_time = time.time() - start_time  # End the timer
    print(f"Retrieved {len(processed_posts)} posts.")
    print(f"Time elapsed: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process LinkedIn user data.')
    parser.add_argument('username', help='LinkedIn username')
    args = parser.parse_args()
    main(args.username)
