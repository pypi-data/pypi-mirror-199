#!/usr/bin/python3

from pprint import pprint

import requests


class AlmostRequested:
    def __init__(self, session: requests.Session, url: str):
        self.url = url
        self.s = session

    def get(self, **kwargs) -> requests.Response:
        return self._do_request("get", **kwargs)

    def head(self, **kwargs) -> requests.Response:
        return self._do_request("head", **kwargs)

    def post(self, **kwargs) -> requests.Response:
        return self._do_request("post", **kwargs)

    def put(self, **kwargs) -> requests.Response:
        return self._do_request("put", **kwargs)

    def delete(self, **kwargs) -> requests.Response:
        return self._do_request("delete", **kwargs)

    def options(self, **kwargs) -> requests.Response:
        return self._do_request("options", **kwargs)

    def patch(self, **kwargs) -> requests.Response:
        return self._do_request("patch", **kwargs)

    def _do_request(self, verb, **kwargs) -> requests.Response:
        print(verb, self.url, kwargs)
        if "url" not in kwargs:
            kwargs["url"] = self.url

        print_json = kwargs.pop("print_json", False)

        r: requests.Response = getattr(self.s, verb)(**kwargs)
        r.raise_for_status()

        if print_json:
            pprint(r.json())
        return r

    def __getattr__(self, item, **kwargs):
        return self.append(item, underscore_to_dash=True)

    def append(self, item, underscore_to_dash=False):
        url = self.url

        if underscore_to_dash:
            item = item.replace("_", "-")

        if url[-1] != "/":
            url += "/"

        url += item
        return AlmostRequested(self.s, url)

    def a(self, item, underscore_to_dash=False):
        return self.append(item, underscore_to_dash)
