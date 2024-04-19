import tiktoken
import requests
import pytz
from datetime import datetime, timezone


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def convert_unix_to_local_time(timestamp, tz):
    """
    Converts a Unix timestamp to a datetime object in the specified timezone.

    Args:
    timestamp (int): Unix timestamp, the number of seconds since January 1, 1970, UTC.
    tz (str): Timezone string, e.g., 'America/New_York' for Eastern Time.

    Returns:
    datetime: A datetime object representing the time in the specified timezone.
    """
    # Create a timezone-aware UTC datetime object from a timestamp
    utc_date_object = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    # Define the target timezone
    target_timezone = pytz.timezone(tz)

    # Convert UTC datetime object to target timezone
    local_date_object = utc_date_object.astimezone(target_timezone)

    return local_date_object


def handle_calendar_api_data(data):
    text = ""
    upcoming_days = data["events"]
    for _, event_list in upcoming_days.items():
        for single_event in event_list:
            if "ts_start" in single_event and "tz" in single_event:
                start_at = str(
                    convert_unix_to_local_time(
                        single_event["ts_start"], single_event["tz"]
                    )
                )
            else:
                start_at = ""  # Default value if start time or timezone isn't specified

            if "ts_end" in single_event and "tz" in single_event:
                end_at = str(
                    convert_unix_to_local_time(
                        single_event["ts_end"], single_event["tz"]
                    )
                )
            else:
                end_at = ""  # Default value if end time or timezone isn't specified

            # Append href if exists
            if "href" in single_event:
                text += single_event["href"] + " "

            # Append title if exists
            if "title" in single_event:
                text += single_event["title"] + " "

            # Append location if exists
            if "location" in single_event:
                text += "location: " + single_event["location"] + " "

            # Append custom room number if exists
            if "custom_room_number" in single_event:
                text += "Room " + single_event["custom_room_number"] + " "

            # Append start and end times
            text += f"start at {start_at} end at {end_at} "

            # Append online URL if it exists and is not empty
            if single_event.get("Attend virtually with online_url", ""):
                text += "online URL: " + single_event["online_url"]
    return text


def turn_text_into_embeddings(model, text, endpoint_url, openai_headers):
    payload = {"model": model, "input": text}
    # Make the POST request to the OpenAI API
    response = requests.post(endpoint_url, headers=openai_headers, json=payload)
    if response.status_code == 200:
        # Extract the embeddings from the response
        data = response.json().get("data", [])
        embedding = [item["embedding"] for item in data if "embedding" in item][0]
        # print("Embeddings:", embedding)
        return embedding
    else:
        print("Failed to generate embeddings:", response.text)
        return None
