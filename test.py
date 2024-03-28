import requests
from opensearchpy import OpenSearch
import json

# Confluence site URL
BASE_URL = "https://your-confluence-site.com"
# Confluence API endpoint for getting page content by ID
PAGE_URL = BASE_URL + "/rest/api/content/{page_id}?expand=body.storage,children.page"

# Your Confluence credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# AWS OpenSearch endpoint
OPENSEARCH_HOST = "your-opensearch-endpoint"
OPENSEARCH_PORT = 443  # or the appropriate port

# AWS OpenSearch credentials
OPENSEARCH_USERNAME = "your_opensearch_username"
OPENSEARCH_PASSWORD = "your_opensearch_password"

# Initialize AWS OpenSearch client
opensearch_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=True,
    connection_class=None,
)

# Function to recursively download page contents and upload to OpenSearch
def download_page_and_upload_to_opensearch(page_id):
    # Get page content
    page_response = requests.get(PAGE_URL.format(page_id=page_id), auth=(USERNAME, PASSWORD))
    if page_response.status_code == 200:
        page_data = page_response.json()
        # Prepare document to index in OpenSearch
        document = {
            "title": page_data["title"],
            "content": page_data["body"]["storage"]["value"],
        }
        # Index document in OpenSearch
        opensearch_client.index(index="confluence_pages", body=document)

        # Check if the page has children
        if "children" in page_data:
            for child in page_data["children"]["page"]["results"]:
                # Recursively upload children to OpenSearch
                download_page_and_upload_to_opensearch(child["id"])
    else:
        print("Failed to download page:", page_response.status_code)

# Main function
def main():
    # Input the root page ID
    root_page_id = input("Enter the root page ID: ")
    download_page_and_upload_to_opensearch(root_page_id)

if __name__ == "__main__":
    main()
