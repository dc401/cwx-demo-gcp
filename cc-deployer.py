#!/usr/bin/env python3

import json
import subprocess
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python cc_deployer.py <buildspec_json>")
        sys.exit(1)

    buildspec_path = sys.argv[1]
    if not os.path.exists(buildspec_path):
        print(f"Buildspec file not found: {buildspec_path}")
        sys.exit(1)

    with open(buildspec_path, 'r') as f:
        buildspec = json.load(f)

    for policy_path in buildspec.get('detection', []):
        print(f"Processing policy: {policy_path}")

        # Dry run
        print("Performing dry run...")
        subprocess.run(['custodian', 'run', '-d', '-s', '.', policy_path, '-v'], check=True)

        # Full run
        print("Performing full run...")
        subprocess.run(['custodian', 'run', '-s', '.', policy_path, '-v'], check=True)

        # Integration test
        print("Running integration test...")
        pull_result = subprocess.run(
            ['gcloud', 'pubsub', 'subscriptions', 'pull', '--auto-ack', '--limit=1', 
             'github-actions-detection-tests-sub', '--format=json'],
            capture_output=True, text=True, check=True
        )
        
        subprocess.run(
            ['python3', './gcp-cc-integration-test.py', policy_path],
            input=pull_result.stdout, text=True, check=True
        )

        print(f"Completed processing for {policy_path}")
        print("-" * 40)

if __name__ == "__main__":
    main()