import requests
import pandas as pd
import time

page = 1
issues = []
users = []
labels = []
users_set = set()

while True:
        
    URL = "https://api.github.com/repos/apache/airflow/issues"

    headers = {
        "Authorization": "Bearer Token"
    }

    params = {
        "per_page": 100,
        "page": page
    }

    for i in range(3):
        response = requests.get(URL, headers = headers, params = params, timeout = 10)

        if response.status_code == 200:
            print(f"Request successful: Loading page {page}")
            break
        elif response.status_code == 429:
            print("Too many requests: Waiting....")
            time.sleep(5)
            continue
        else:
            print("Bad Request. Trying again")

    if response.status_code != 200:
        raise Exception("Request Failed after multiple retries")  

    data = response.json()

    if not data:
        break

    for issue in data:

        if "pull_request" in issue:
            continue

        label = issue.get("labels", [])
        user = issue.get("user", {})
        issue_id = issue.get("id")

        issues.append({
            "issue_id": issue_id,
            "issue_title": issue.get("title"),
            "state": issue.get("state"),
            "user_id": user.get("id"),
            "created_at": issue.get("created_at")
        })

        if user and user.get("id") not in users_set:
            users.append({
                "user_id": user.get("id"),
                "login": user.get("login"),
                "user_type": user.get("type")
            })

            users_set.add(user.get("id"))

        for l in label:

            labels.append({
                "label_id": l.get("id"),
                "issue_id": issue_id,
                "label_name": l.get("name")
            })

    page += 1
    time.sleep(1)

print(f"{len(issues)} rows loaded to issues")
print(f"{len(users)} rows loaded to users")
print(f"{len(labels)} rows loaded to labels")

issues_df = pd.DataFrame(issues)
users_df = pd.DataFrame(users)
labels_df = pd.DataFrame(labels)

print(issues_df.head())
print(users_df.head())
print(labels_df.head())