import json
import time
from linkedin_api import Linkedin

class LinkedInCompanyFetcher:
    def __init__(self, username, password):
        self.api = Linkedin(username, password)

    def get_company_updates(self, public_id=None, urn_id=None, max_results=None):
        return self.api.get_company_updates(public_id=public_id, urn_id=urn_id, max_results=max_results)

    def format_update_data(self, updates, username, save_raw=False):
        if save_raw:
            with open(f'{username}_raw_updates.json', 'w') as file:
                json.dump(updates, file, indent=4)

        formatted_updates = []
        for idx, update in enumerate(updates, start=1):
            try:
                actions = update['value']['com.linkedin.voyager.feed.render.UpdateV2']['updateMetadata']['updateActions']['actions']
                url = actions[1]['url']  # URL is in the second action item
            except (IndexError, KeyError, TypeError):
                url = 'URL Not Found'

            formatted_update = {
                "idx": idx,
                "link to post": url
            }
            formatted_updates.append(formatted_update)
        
        return formatted_updates

    def fetch_and_process_updates(self, username, public_id=None, urn_id=None, max_results=None, save_to_file=False, save_raw=False):
        updates = self.get_company_updates(public_id=public_id, urn_id=urn_id, max_results=max_results)
        formatted_updates = self.format_update_data(updates, username, save_raw)
        if save_to_file:
            file_name = f'{username}_updates.json'
            with open(file_name, 'w') as file:
                json.dump(formatted_updates, file, indent=4)
        return formatted_updates

if __name__ == "__main__":
    start_time = time.time()  # Start the chronometer

    # LinkedIn API credentials
    api_username = 'your_email'
    api_password = 'your_password'

    # Company identifier (public_id or urn_id)
    public_id = 'meta'  # Replace with actual company public ID

    fetcher = LinkedInCompanyFetcher(api_username, api_password)

    # Retrieve and process company updates
    company_updates = fetcher.fetch_and_process_updates(username=public_id, public_id=public_id, max_results=1, save_to_file=True, save_raw=True)

    end_time = time.time()  # End the chronometer
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
