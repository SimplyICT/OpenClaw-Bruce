import os
import requests

def get_digest(site_url, fed_auth, rtfa):
    endpoint = f"{site_url}/_api/contextinfo"
    headers = {
        "Accept": "application/json;odata=verbose",
        "Cookie": f"FedAuth={fed_auth}; rtFa={rtfa}"
    }
    response = requests.post(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()['d']['GetContextWebInformation']['FormDigestValue']
    else:
        print(f"Digest Fetch Failed: {response.status_code}")
        print(response.text)
    return None

def upload_to_sharepoint_rest(file_path, site_url, folder_url, fed_auth, rtfa):
    file_name = os.path.basename(file_path)
    digest = get_digest(site_url, fed_auth, rtfa)
    
    if not digest:
        print("Failed to get X-RequestDigest. Cookies might be expired or incomplete.")
        return

    endpoint = f"{site_url}/_api/web/GetFolderByServerRelativeUrl('{folder_url}')/Files/add(url='{file_name}',overwrite=true)"
    
    with open(file_path, 'rb') as f:
        file_content = f.read()

    headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/octet-stream",
        "X-RequestDigest": digest,
        "Cookie": f"FedAuth={fed_auth}; rtFa={rtfa}"
    }

    print(f"Attempting upload to: {endpoint}")
    response = requests.post(endpoint, data=file_content, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        print(f"Successfully uploaded {file_name}!")
    else:
        print(f"Upload failed. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    SITE_URL = "https://cccex1.sharepoint.com/sites/bhelc-admin"
    FOLDER_URL = "/sites/bhelc-admin/Shared Documents/Audit reports"
    
    # UPDATED AUTH TOKENS - May 8, 2026
    FED_AUTH = "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE1LDBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwM2ZkNmEzYjZlQGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHxzeXNhZG1pbkBjY2NleC5jb20uYXUsMTM0MjI3NDcxMzIwMDAwMDAwLDEzMzc2MTA0MjIwMDAwMDAwMCwxMzQyMjgzMzYzMjMzNjU3NDcsMjAzLjIyMS44NC4yMTAsNjYsOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyLCwwMDRkOGJhYS02MjNmLTk1MTktNDJiMS04ZmJiYTJhOTFhZmIsYjFiODExYTItMTA3ZS03MDAwLTljZTEtNWYxMjFiMDNkYTMzLGIxYjgxMWEyLTEwN2UtNzAwMC05Y2UxLTVmMTIxYjAzZGEzMywsMCwxMzQyMjgzMzYzMjMxMDYyOTQsMTM0MjMwMDY0MzIzMTA2Mjk0LCwsZXlKNGJYTmZZMk1pT2lKYlhDSkRVREZjSWwwaUxDSjRiWE5mYzNOdElqb2lNU0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNkluTjVjMkZrYldsdVFHTmpZMlY0TG1OdmJTNWhkU0lzSW5WMGFTSTZJbTR6UW1WQ05teHFSMFV5WmxWbmRrTlNlV3R2UVVFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpReU1qYzBOekV6TWpBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDIyNzQ3MjMxMDAwMDAwMCw5ZmM5MmFhYi03MmMzLTRiZjgtODEwNC1mNzU3MmY2ZDE5MGMsLCwsLCwxMTUyOTIxNTA0NjA2ODQ5NTQzLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLCwwLCxDc042NmRwSHkxWjdxT1hYWFZJZkZZTENrVjFsZzgyRi9qb1FtQVZzU2RwT0tXM1NZc1JFVnA3eExSUHBnSXFCcDB1M2t0Q1NEZmV0SGRGMFhkanNNYjBaYU01OWxJbFJKTDhlT3E4SWJhTFlsYk9ZSzQ0b29sU2wxVUpYNDlTVW9ITFFERGJteGJEMGZiYXIyK0NXVGxJR1BpZmFrQnljTm1Kak50VGszUDZOMjNSbFhYNXRCWUcvOFBIVDFlVE5YQU9IYmQ1ZFFCWTBYRU53TVg0cVlDMnUzamVqRXRxV0FSM0FvZmdpWENxbVhYdjFkdUk5WTNSUDVRZ3hqUkV4YTJseUxKaW56YnFYbnY3Y21XcFpCL1ZER05JMEdTK0IzREFWc0h1aGJiWS9GR0dWSVdabkZFWUx3bDVxaHlTUzJDNis2M3QzbW0vZXpTQjZIMVVEa0E9PTwvU1A+"
    RTFA = "7BVn6LiNrnRxTtibuYlsEngYqghUTvBEJg0fFrMthOEmOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyIzEzNDIyNzQ3MjMyMzU2MTU3MSNiMWI4MTFhMi0xMDdlLTcwMDAtOWNlMS01ZjEyMWIwM2RhMzMjc3lzYWRtaW4lNDBjY2NleC5jb20uYXUsMTM0MjI3NDcxMzIwMDAwMDAwLDEzMzc2MTA0MjIwMDAwMDAwMCwxMzQyMjgzMzYzMjMzNjU3NDcsMjAzLjIyMS44NC4yMTAsNjYsOGJlMjAyMmUtYjk3OS00NTM2LTkzNWItMjY4YTQ2OGU3M2EyLCwwMDRkOGJhYS02MjNmLTk1MTktNDJiMS04ZmJiYTJhOTFhZmIsYjFiODExYTItMTA3ZS03MDAwLTljZTEtNWYxMjFiMDNkYTMzLGIxYjgxMWEyLTEwN2UtNzAwMC05Y2UxLTVmMTIxYjAzZGEzMywsMCwxMzQyMjgzMzYzMjMxMDYyOTQsMTM0MjMwMDY0MzIzMTA2Mjk0LCwsZXlKNGJYTmZZMk1pT2lKYlhDSkRVREZjSWwwaUxDSjRiWE5mYzNOdElqb2lNU0lzSW5CeVpXWmxjbkpsWkY5MWMyVnlibUZ0WlNJNkluTjVjMkZrYldsdVFHTmpZMlY0TG1OdmJTNWhkU0lzSW5WMGFTSTZJbTR6UW1WQ05teHFSMFV5WmxWbmRrTlNlV3R2UVVFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpReU1qYzBOekV6TWpBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDIyNzQ3MjMxMDAwMDAwMCw5ZmM5MmFhYi03MmMzLTRiZjgtODEwNC1mNzU3MmY2ZDE5MGMsLCwsLCwxMTUyOTIxNTA0NjA2ODQ5NTQzLCwxOTU1NzUsNHEtWjh4QWZRN1VLMXI0alRnOVBic2M1cG1VLCwwLCxDc042NmRwSHkxWjdxT1hYWFZJZkZZTENrVjFsZzgyRi9qb1FtQVZzU2RwT0tXM1NZc1JFVnA3eExSUHBnSXFCcDB1M2t0Q1NEZmV0SGRGMFhkanNNYjBaYU01OWxJbFJKTDhlT3E4SWJhTFlsYk9ZSzQ0b29sU2wxVUpYNDlTVW9ITFFERGJteGJEMGZiYXIyK0NXVGxJR1BpZmFrQnljTm1Kak50VGszUDZOMjNSbFhYNXRCWUcvOFBIVDFlVE5YQU9IYmQ1ZFFCWTBYRU53TVg0cVlDMnUzamVqRXRxV0FSM0FvZmdpWENxbVhYdjFkdUk5WTNSUDVRZ3hqUkV4YTJseUxKaW56YnFYbnY3Y21XcFpCL1ZER05JMEdTK0IzREFWc0h1aGJiWS9GR0dWSVdabkZFWUx3bDVxaHlTUzJDNis2M3QzbW0vZXpTQjZIMVVEa0E9PTwvU1A+"

    import sys
    
    file_to_send = sys.argv[1] if len(sys.argv) > 1 else "report_Benowa_Hills_ELC_2026-05-08.docx"
    
    if os.path.exists(file_to_send):
        upload_to_sharepoint_rest(file_to_send, SITE_URL, FOLDER_URL, FED_AUTH, RTFA)
    else:
        print(f"File {file_to_send} not found.")
