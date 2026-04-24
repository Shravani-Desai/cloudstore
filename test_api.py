import requests
import json

API_URL = "https://zp8cwztyy5.execute-api.us-east-1.amazonaws.com/prod"

def test_upload():
    print("\n--- Test 1: Upload file ---")
    response = requests.post(f"{API_URL}/upload", json={
        "filename": "demo.txt",
        "size": 256,
        "owner": "shravani"
    })
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"File ID: {data['file_id']}")
    print(f"Upload URL: {data['upload_url'][:60]}...")
    return data['file_id']

def test_list():
    print("\n--- Test 2: List all files ---")
    response = requests.get(f"{API_URL}/files")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total files: {len(data)}")
    for item in data:
        print(f"  - {item['filename']} (owner: {item['owner']})")

def test_list_by_owner():
    print("\n--- Test 3: List files by owner ---")
    response = requests.get(f"{API_URL}/files?owner=shravani")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Files owned by shravani: {len(data)}")

def test_download(file_id):
    print("\n--- Test 4: Download file ---")
    response = requests.get(f"{API_URL}/file/{file_id}")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Filename: {data['filename']}")
    print(f"Download URL: {data['download_url'][:60]}...")

def test_not_found():
    print("\n--- Test 5: File not found ---")
    response = requests.get(f"{API_URL}/file/non-existent-id")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("Starting CloudStore API tests...")
    file_id = test_upload()
    test_list()
    test_list_by_owner()
    test_download(file_id)
    test_not_found()
    print("\nAll tests complete!")