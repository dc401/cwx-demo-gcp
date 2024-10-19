#!/usr/bin/env python3

import base64
import zlib
import sys
import json
import yaml

def get_policy_name_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_content = yaml.safe_load(file)
    return yaml_content['policies'][0]['name']

# Get the YAML file path from command line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <policy_yaml_file>")
    sys.exit(1)

policy_yaml_file = sys.argv[1]
yaml_policy_name = get_policy_name_from_yaml(policy_yaml_file)

# Read the JSON from stdin
input_json = json.loads(sys.stdin.read())

# Process each message
for message in input_json:
    try:
        # Extract the encoded data
        encoded_data = message['message']['data']
        
        # Decode and decompress
        padded_data = encoded_data + '=' * (-len(encoded_data) % 4)
        decompressed = zlib.decompress(base64.urlsafe_b64decode(padded_data))
        decoded_message = json.loads(decompressed)
        
        # Extract policy name from the decoded message
        pubsub_policy_name = decoded_message['policy']['name']

        # Compare policy names
        if pubsub_policy_name == yaml_policy_name:
            print(f"Policy name match found: {pubsub_policy_name}")
        else:
            print(f"No match: PubSub policy '{pubsub_policy_name}' doesn't match YAML policy '{yaml_policy_name}'")

        # Commented out print statements for troubleshooting
        # print(json.dumps(decoded_message, indent=2))
        # print("\n---\n")  # Separator between messages
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        print(json.dumps(message, indent=2))
        print("\n---\n")