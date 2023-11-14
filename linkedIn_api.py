from linkedin_api import Linkedin
from pprint import pprint
import json

# Your LinkedIn API credentials
api = Linkedin('quinocarreteromartinez@gmail.com', 'Quinito98')

# Fetching profile posts
data = api.get_profile_posts(public_id="carrie-beam", post_count=100)

# Pretty print the data
pprint(data)

# Properly formatting the JSON data with indentation
formatted_data = json.dumps(data, indent=4)

# Saving the formatted JSON data to a file
with open('carrie-beamm.json', 'w') as file:
    file.write(formatted_data)
