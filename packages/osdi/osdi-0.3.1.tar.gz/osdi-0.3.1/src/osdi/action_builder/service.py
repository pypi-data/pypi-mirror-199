from __future__ import annotations

from collections import defaultdict
from typing import Dict

from osdi.action_builder.model import ActionBuilderModel
from osdi.action_builder.person import ABPerson
from osdi.action_builder.tag import ABTag, ABTagging, parse_tag_schema
from osdi.base.service import ActionError, ActionService
from osdi.base.utils import parse_embedded_id


class ActionBuilderService(ActionService):
    campaigns: dict

    def __init__(self, uri, api_key):
        super(ActionService, self).__init__(uri, api_key)
        camps = self.get_model("campaigns", "action_builder:campaigns", model=Campaign)
        self.campaigns = {c.name: c for c in camps}


class Campaign(ActionBuilderModel):
    tags: Dict[str, Dict[str, ABTag]]
    name: str
    model: ABPerson
    config: dict

    def __init__(self, service, data):
        super(Campaign, self).__init__(service, data, "campaign")
        uri = f"{service.uri}/campaigns/{self.id}"
        self.service = ActionService(uri, service.api_key)
        self.tags = self.get_linked_collection("osdi:tags", ABTag)
        self.tags_by_value = defaultdict(dict)
        self.tags_by_id = {}
        for t in self.tags:
            self.tags_by_value[t.field][t.name] = t
            self.tags_by_id[t.id] = t
        self.name = data["name"]
        self.config = self.get_config()
        self.model = ABPerson.person_model_from_tag_config(
            self.config, f"{self.name.replace(' ', '')}Person"
        )

    def find_person(self, ab_id=None, email=None, phone=None, model=None):
        if model is None:
            model = self.model
        if ab_id:
            return self.retrieve_person_by_id(ab_id, model)
        if email:
            per = self.service.get_person({"email_address": email})
            if per:
                return model(self.service, self, per)

        if phone:
            per = self.service.get_person({"phone_number": phone})
            if per:
                return model(self.service, self, per)
        return None

    def _get_updates(self):
        raise ActionError("Campaigns cannot be updated directly")

    def retrieve_person_by_id(self, ab_id, model=None):
        if model is None:
            model = self.model
        return model(self.service, self, self.service._get_request(f"/people/{ab_id}"))

    def create_person(self, first_name, last_name, email, custom_fields={}, model=None):
        if model is None:
            model = self.model
        for val in [first_name, last_name, email]:
            if val is None:
                raise ActionError(
                    "Cannot create AB Person without all of first name, last name, and email"
                )

        member_object = {
            "given_name": first_name,
            "family_name": last_name,
            "email_addresses": [{"address": email, "address_type": "home"}],
            "languages_spoken": ["en"],
        }
        if custom_fields:
            member_object["custom_fields"] = custom_fields
        data = {"person": member_object}

        res = self.service._post_request("people", data)
        if model is not None:
            return model(self.service, self, res)
        else:
            return res

    def retrieve_person_by_identifier(self, identifier_type, ak_id, model=None):
        if model is None:
            model = self.model
        per = self.service.get_person({"identifier": f"{identifier_type}:{ak_id}"})
        if per:
            return model(self.service, per[0])
        return None

    def parse_tagging(self, tagging_data):
        tag_id = parse_embedded_id(tagging_data, "osdi:tag")
        if tag_id not in self.tags_by_id:
            self.logger.warning(f"Tag {tagging_data} is not in {self.name} tags")
            return None
        matching_tag = self.tags_by_id[tag_id]
        return ABTagging(self.service, matching_tag, tagging_data)

    def construct_tagging(self, tag_field, tag_name, value=None):
        tag = self.tags_by_value[tag_field][tag_name]
        tag_update = {
            "action_builder:section": tag.section,
            "action_builder:field": tag.field,
            "action_builder:name": tag_name,
        }
        if value is not None:
            tag_update["action_builder:date_response"] = value
        return tag_update

    def get_config(self):
        return parse_tag_schema(self.tags)
