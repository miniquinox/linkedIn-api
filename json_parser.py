import json

def get_linkedin_link(urn):
    # Extract the unique identifier from the urn and create a LinkedIn post link
    post_id = urn.split(':')[-1]
    return f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

def extract_post_details(post, idx):
    # Extract basic post details
    post_data = {
        "idx": idx,
        "User": post['actor']['name']['text'],
        "Link to Post": get_linkedin_link(post['updateMetadata']['urn']),
        "Post Description": post['commentary']['text']['text'] if 'commentary' in post else "No posts",
        "Likes": post['socialDetail']['totalSocialActivityCounts']['numLikes'],
        "Shares": post['socialDetail']['totalSocialActivityCounts']['numShares'],
        "Number of Comments": post['socialDetail']['totalSocialActivityCounts']['numComments']
    }

    # Check for repost and add details if present
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

# Read the original JSON data
with open('carrie-beam.json', 'r') as file:
    data = json.load(file)

# List to store processed post details
processed_posts = []

# Process each post
for idx, post in enumerate(data, start=1):
    processed_post = extract_post_details(post, idx)
    if processed_post:  # Only add if post data is valid
        processed_posts.append(processed_post)

# Write the processed data to a new JSON file
with open('processed_data.json', 'w') as file:
    json.dump(processed_posts, file, indent=4)
