import json
import time
from linkedin_api import Linkedin

class LinkedInDataFetcher:
    def __init__(self, username, password):
        self.api = Linkedin(username, password)

    def get_linkedin_link(self, urn):
        post_id = urn.split(':')[-1]
        return f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

    def extract_post_details(self, post, idx):
        post_data = {
            "idx": idx,
            "User": post['actor']['name']['text'],
            "Link to Post": self.get_linkedin_link(post['updateMetadata']['urn']),
            "Post Description": post['commentary']['text']['text'] if 'commentary' in post else "No posts",
            "Likes": post['socialDetail']['totalSocialActivityCounts']['numLikes'],
            "Shares": post['socialDetail']['totalSocialActivityCounts']['numShares'],
            "Number of Comments": post['socialDetail']['totalSocialActivityCounts']['numComments']
        }
        if 'resharedUpdate' in post:
            original_post = post['resharedUpdate']
            post_data["Repost"] = {
                "Original User": original_post['actor']['name']['text'],
                "Original Link to Post": self.get_linkedin_link(original_post['updateMetadata']['urn']),
                "Original Post Description": original_post['commentary']['text']['text'] if 'commentary' in original_post else "No posts",
                "Original Likes": original_post['socialDetail']['totalSocialActivityCounts']['numLikes'],
                "Original Shares": original_post['socialDetail']['totalSocialActivityCounts']['numShares'],
                "Original Number of Comments": original_post['socialDetail']['totalSocialActivityCounts']['numComments']
            }
        return post_data

    def fetch_and_process_posts(self, username, post_count, save_to_file=False):
        data = self.api.get_profile_posts(public_id=username, post_count=post_count)
        processed_posts = [self.extract_post_details(post, idx) for idx, post in enumerate(data, start=1)]
        if save_to_file:
            with open(f'temp/{username}_posts.json', 'w') as file:
                json.dump(processed_posts, file, indent=4)
        return processed_posts

def read_credentials(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password

if __name__ == "__main__":
    start_time = time.time()

    # Read credentials from file
    username, password = read_credentials('credentials.txt')

    fetcher = LinkedInDataFetcher(username, password)
    username_to_fetch = 'miniquinox'
    post_count = 100

    posts_data = fetcher.fetch_and_process_posts(username_to_fetch, post_count, save_to_file=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
