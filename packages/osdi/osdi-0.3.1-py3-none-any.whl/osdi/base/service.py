from __future__ import annotations

import json
import logging
import math
import random
import time
from typing import Callable, Mapping, TypeVar

from requests import request

T = TypeVar("T")


def retry_with_backoff(fn: Callable[[], T], retries=10, backoff_in_seconds=1) -> T:
    x = 0
    while True:
        try:
            return fn()
        except:
            if x == retries:
                raise
            else:
                sleep = backoff_in_seconds * 2**x + random.uniform(0, 1)
                time.sleep(sleep)
                x += 1


class ActionError(Exception):
    pass


class OSDIService:
    headers: Mapping
    api_key: str
    uri: str

    @property
    def headers(self):
        return {"Content-Type": "application/json", "OSDI-API-TOKEN": self.api_key}

    def __init__(self, uri, api_key):
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.uri = uri
        self.api_key = api_key

    def set_api_key(self, key):
        self.api_key = key

    def _request(self, url, req_type, data=None, params=None, is_full=False):
        if not is_full:
            full_url = f"{self.uri}/{url}"
        else:
            full_url = url

        self.logger.debug("{} {} {}".format(full_url, data, params))

        def make_request():
            res = request(
                req_type, full_url, headers=self.headers, data=json.dumps(data), params=params
            )
            if res.status_code in [502, 500]:
                self.logger.error("{} {} {} {}".format(self.uri, url, data, params))
                raise ActionError(f"Status code {res.status_code}")
            return res

        return retry_with_backoff(make_request)

    def _get_request(self, url, data=None, params=None, is_full=False):
        r = self._request(url, "GET", data, params, is_full)
        if r.status_code in [200, 201, 204]:
            try:
                return r.json()
            except json.decoder.JSONDecodeError:
                self.logger.error(r.text)
                raise ActionError("{}/{} failed to decode".format(self.uri, url))
        else:
            self.logger.error(r.text)
            self.logger.error("{} {} {} {}".format(self.uri, url, data, params))
            raise ActionError(
                f"Received status code {r.status_code} when querying {url}, full {is_full}"
            )

    def _delete_request(self, url, data=None, params=None, is_full=False):
        r = self._request(url, "DELETE", data, params, is_full)
        if r.status_code in [200, 201, 204]:
            return r.json()
        else:
            self.logger.error(r.text)
            raise ActionError(f"Received status code {r.status_code} when deleting {url}")

    def _post_request(self, url, data=None, params=None, is_full=False):
        r = self._request(url, "POST", data, params, is_full)
        if r.status_code in [200, 201, 204]:
            return r.json()
        else:
            self.logger.error(r.text)
            raise ActionError(f"Received status code {r.status_code} when posting {url}")

    def _put_request(self, url, data=None, params=None):
        r = self._request(url, "PUT", data, params)
        if r.status_code in [200, 201, 204]:
            return r.json()
        else:
            if "error" in r.text:
                self.logger.error(r.text)
            else:
                self.logger.error("{} {} {} {}".format(self.uri, url, data, params))
            raise ActionError(f"Received status code {r.status_code} when putting {url}")

    def _get_all(
        self, object_type, url=None, object_domain=None, data=None, is_full=None, params=None
    ):
        if url is None:
            url = object_type
            if is_full is None:
                is_full = False
        elif is_full is None:
            is_full = True
        if object_domain is not None:
            full_obj_name = f"{object_domain}:{object_type}"
        else:
            full_obj_name = object_type

        response = self._get_request(url, data=data, params=params, is_full=is_full)
        if response.get("total_pages") == 0:
            return []
        all_res = response["_embedded"][full_obj_name]
        while (
            len(response["_embedded"][full_obj_name]) >= response["per_page"]
            and len(all_res) < response.get("total_records", math.inf)
            and "next" in response["_links"]
        ):
            if len(all_res) % 1000 == 0:
                self.logger.info(f"Retrieved {len(all_res)} {object_type}, still retrieving...")
            url = response["_links"]["next"]["href"]
            response = self._get_request(url, is_full=True)
            try:
                new_res = response["_embedded"][full_obj_name]
            except TypeError:
                self.logger.warning("{} {}".format(response, response.json))
            all_res += new_res
        return all_res

    def get_model_raw(self, url, model_type, data=None, params=None, is_full=False):
        return self._get_all(model_type, url=url, data=data, params=params, is_full=is_full)

    def get_model(self, url, model_type, model, data=None, params=None, is_full=False):
        results = self._get_all(model_type, url=url, data=data, params=params, is_full=is_full)
        return [model(self, r) for r in results]


class ActionService(OSDIService):
    def __init__(self, uri, api_key):
        super(ActionService, self).__init__(uri, api_key)

    def get_people(self, params, model=None):
        query_str = "and".join(f"{k} eq '{v}'" for k, v in params.items())
        if model is None:
            return self.get_model_raw("people", "osdi:people", params={"filter": query_str})
        else:
            return self.get_model("people", "osdi:people", model, params={"filter": query_str})

    def get_person(self, params, model=None):
        people = self.get_people(params, model)
        if len(people) > 1:
            raise ActionError(
                f"Tried to retrieve single person matching {params} but found {len(people)}"
            )
        elif people:
            return people[0]
        else:
            return None
