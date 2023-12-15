import requests
import pickle

target_date = "1402-08-29 11:59:00"


# Elasticsearch configuration
index_name = "logs"
with open("./../data/config_variables/BASE_URL.pkl", "rb") as f:
    elasticsearch_url = pickle.load(f)


# Elasticsearch Scroll API endpoint
scroll_endpoint = f"{elasticsearch_url}{index_name}/_search?scroll=1m"
delete_endpoint = f"{elasticsearch_url}{index_name}/_delete_by_query"


# Define the initial query to match documents before the target date
initial_query = {
    "query": {"range": {"timestamp": {"lt": target_date}}},
    "size": 1000,  # Number of documents to retrieve per scroll
}

# Send the initial search request
response = requests.post(scroll_endpoint, json=initial_query)
response_json = response.json()

# Get the scroll ID and the total number of matching documents
scroll_id = response_json.get("_scroll_id")
total_docs = response_json["hits"]["total"]["value"]

# Delete documents in batches until all matching documents are deleted
while total_docs > 0:
    # Extract the list of document IDs from the response
    doc_ids = [hit["_id"] for hit in response_json["hits"]["hits"]]

    # Define the delete by query request
    delete_query = {"query": {"terms": {"_id": doc_ids}}}

    # Send the delete by query request
    delete_response = requests.post(delete_endpoint, json=delete_query)
    delete_response_json = delete_response.json()

    # Check the delete response for errors
    if "deleted" not in delete_response_json:
        print("Error deleting documents:", delete_response_json)
        break

    # Update the total number of documents
    total_docs -= delete_response_json["deleted"]

    # Scroll to the next batch of documents
    scroll_query = {"scroll": "1m", "scroll_id": scroll_id}
    scroll_response = requests.post(
        f"{elasticsearch_url}_search/scroll", json=scroll_query
    )
    response_json = scroll_response.json()
    scroll_id = response_json.get("_scroll_id")
