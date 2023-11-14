import json
from linkedin_api import Linkedin

def get_comments_from_post(api, post_urn):
    comments = api.get_post_comments(post_urn)
    return comments

def format_comment_data(comments):
    formatted_comments = []
    for idx, comment in enumerate(comments, start=1):
        formatted_comment = {
            "idx": idx,
            "Username": comment.get('publicIdentifier', 'Unknown'),
            "Comment": comment.get('commentV2', {}).get('text', 'No text'),
            "Likes": comment.get('totalSocialActivityCounts', {}).get('numLikes', 0)
        }
        formatted_comments.append(formatted_comment)
    print(comments[0])
    return formatted_comments

def get_comments_dict(post_urn):
    # Credentials for LinkedIn API
    username = 'quinocarreteromartinez@gmail.com'
    password = 'Quinito98'

    # Initialize LinkedIn API with credentials
    api = Linkedin(username, password)

    # Retrieve comments
    comments = get_comments_from_post(api, post_urn)

    # Format comments
    formatted_comments = format_comment_data(comments)

    return formatted_comments

if __name__ == "__main__":
    # Example Post URN
    post_urn = '7105018421649580033'  # URN of the LinkedIn post

    # Retrieve formatted comments as a dictionary
    comments_dict = get_comments_dict(post_urn)

    # Optionally, save comments to a JSON file
    with open('comments_data.json', 'w') as file:
        json.dump(comments_dict, file, indent=4)
