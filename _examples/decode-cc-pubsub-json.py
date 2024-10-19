#!/usr/bin/env python3

import base64
import zlib
import sys
import json

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
        
        # Print the decoded message
        print(json.dumps(decoded_message, indent=2))
        print("\n---\n")  # Separator between messages
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        print(json.dumps(message, indent=2))
        print("\n---\n")