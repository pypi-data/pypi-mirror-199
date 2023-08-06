from release_finder.github import GitHubAPI


def latest_release(repo_url, access_token=None):
    api = GitHubAPI(access_token)
    release = api.get_latest_release(repo_url)
    return release["tag_name"]


def latest_release_date(repo_url, access_token=None):
    api = GitHubAPI(access_token)
    release = api.get_latest_release(repo_url)
    return release["published_at"]
