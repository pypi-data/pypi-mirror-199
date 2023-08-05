# Almost Requested

This module provides a simple wrapper around [requests](https://requests.readthedocs.io/en/latest/) to make accessing
APIs a little more simple.

You start off by providing a requests.session, pre-configured with the required headers, then AlmostRequested will
construct the URL you are accessing by taking the dotted path of the AlmostRequested instance, converting it into
a URL, and returning a new AlmostRequested object, ready to call get, put, post or delete on, which themselves return
a `requests.Response`.

```python
class Github(AlmostRequested):
    def __init__(self) -> None:
        s = requests.session()
        self.GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
        s.headers["Authorization"] = f"Bearer {self.GITHUB_TOKEN}"
        s.headers["Content-Type"] = "application/vnd.api+json"
        base_url = "https://api.github.com"

        super().__init__(s, base_url)

    def get_asset(self, asset: dict[str, str]) -> None:
        s = requests.session()
        s.headers["Authorization"] = f"Bearer {self.GITHUB_TOKEN}"
        s.headers["Accept"] = "application/octet-stream"

        if os.path.exists(asset["name"]):
            return

        print("downloading", asset["name"], asset["url"])

        with s.get(url=asset["url"], stream=True) as r:
            r.raise_for_status()
            with open(asset["name"], "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
def main():
    gh = Github()
    splitpolicies = gh.repos.octoenergy.terraform_provider_splitpolicies
    
    # Get Releases from https://github.com/octoenergy/terraform-provider-splitpolicies - by default
    # we convert underscores to dashes in paths
    releases = splitpolicies.releases.latest.get()
    
    # pretty print the JSON decoded response
    releases = splitpolicies.releases.latest.get(print_json=True)
    
    # Insert something into the URL that we can't type as a python variable name
    gh.a("some$endpoint").get()  # Will raise an exception - this endpoint doesn't exist

    # The above is the same as
    gh.append("some$endpoint").get()  # Won't work, but with clearer code

    # Avoid URL magic, just want the headers and response code checking
    gh.get(url="https://github.com/octoenergy/terraform-provider-splitpolicies").get()
```
