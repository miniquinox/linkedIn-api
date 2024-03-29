import json
import time
from linkedin_api import Linkedin

class LinkedInCommentsFetcher:
    def __init__(self, username, password):
        self.api = Linkedin(username, password)

    def get_comments_from_post(self, post_urn):
        return self.api.get_post_comments(post_urn, comment_count=1000)

    def format_comment_data(self, comments):
        formatted_comments = []
        for idx, comment in enumerate(comments, start=1):
            commenter = comment.get('commenterForDashConversion', {})
            image = commenter.get('image', {})
            attributes = image.get('attributes', [])
            mini_profile = attributes[0].get('miniProfile', {}) if attributes else {}

            formatted_comment = {
                "idx": idx,
                "Username": mini_profile.get('publicIdentifier', 'Unknown'),
                "Comment": comment.get('commentV2', {}).get('text', 'No text'),
                "Likes": comment.get('socialDetail', {}).get('totalSocialActivityCounts', {}).get('numLikes', 0)
            }
            formatted_comments.append(formatted_comment)
        return formatted_comments

    def get_comments_dict(self, post_urn, username, save_to_file=False):
        comments = self.get_comments_from_post(post_urn)
        formatted_comments = self.format_comment_data(comments)
        if save_to_file:
            with open(f'temp/{username}_comments.json', 'w') as file:
                json.dump(formatted_comments, file, indent=4)
        return formatted_comments

def read_credentials(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        return username, password

if __name__ == "__main__":
    start_time = time.time()  # Start the chronometer

    # Read credentials from file
    username, password = read_credentials('credentials.txt')

    fetcher = LinkedInCommentsFetcher(username, password)

    # Example Post URN and LinkedIn username
    post_urn = '7115455569485840384'  # URN of the LinkedIn post
    linkedin_username = 'williamhgates'  # Replace with the actual username

    # Retrieve formatted comments as a dictionary and save to file
    comments_dict = fetcher.get_comments_dict(post_urn, linkedin_username, save_to_file=True)

    end_time = time.time()  # End the chronometer
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
