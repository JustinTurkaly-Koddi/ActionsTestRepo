import requests

def merge_branches(base, head, repo_owner, repo_name, github_token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/merges"
    payload = {
        "base": base,
        "head": head
    }
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Merge successful")
    elif response.status_code == 409:
        print("Merge conflict")
    else:
        print(f"Failed to merge: {response.content}")

# You can fetch these from the environment variables in GitHub Actions
github_token = "YOUR_PERSONAL_ACCESS_TOKEN"
repo_owner = "JustinTurkaly-Koddi"
repo_name = "ActionsTestRepo"

# The branches you want to merge
base = "version-202309"
head = "main"

merge_branches(base, head, repo_owner, repo_name, github_token)