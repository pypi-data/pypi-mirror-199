from __future__ import annotations

import osdi.base.utils as utils
from osdi.base.service import ActionError, ActionService


class ActionNetworkService(ActionService):
    tags: dict
    tags_by_name: dict
    config: dict

    def __init__(self, uri, api_key):
        super(ActionService, self).__init__(uri, api_key)
        self.tags = {}
        tags = self.get_model_raw("tags", "osdi:tags")
        self.model = None
        self.tags_by_name = {}
        for t in tags:
            tag_id = utils.parse_embedded_id(t, "self")
            t["id"] = tag_id
            self.tags[tag_id] = t
            self.tags_by_name[t["name"]] = t

    def parse_tagging(self, tagging):
        tag_id = utils.parse_embedded_id(tagging, "osdi:tag")
        if tag_id not in self.tags:
            self.tags[tag_id] = self._get_request(f"tags/{tag_id}")
        return self.tags[tag_id]

    def add_tagging(self, person, tag_name):
        tag = self.tags_by_name[tag_name]
        payload = {"_links": {"osdi:person": {"href": person.link(full=True)}}}
        return self._post_request(
            f"{utils.parse_link(tag, 'self')}/taggings", payload, is_full=True
        )

    def create_person(self, first_name, last_name, email, custom_fields={}, model=None):
        for val in [first_name, last_name, email]:
            if val is None:
                raise ActionError(
                    "Cannot create ActionNetwork Person without all of first name, last name, and email"
                )

        member_object = {
            "given_name": first_name,
            "family_name": last_name,
            "email_addresses": [{"address": email}],
            "languages_spoken": ["en"],
        }
        if custom_fields:
            member_object["custom_fields"] = custom_fields
        data = {"person": member_object}

        res = self._post_request("people", data)
        if model is not None:
            return model(self, res)
        else:
            return res

    def person_by_id(self, an_id, model=None):
        person = self._get_request(f"people/{an_id}")
        if model:
            return model(self, person)
        else:
            return person

    def find_person(self, an_id=None, email=None, phone=None, model=None):
        if model is None:
            model = self.model

        if an_id:
            try:
                return self.person_by_id(an_id, model)
            except ActionError:
                self.logger.warning(f"Invalid an_id {an_id}!")

        if email:
            per = self.get_person({"email_address": email})
            if per:
                return model(self, per)

        if phone:
            per = self.get_person({"phone_number": phone})
            if per:
                return model(self, per)
        return None
