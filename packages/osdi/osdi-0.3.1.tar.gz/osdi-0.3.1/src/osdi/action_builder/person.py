from __future__ import annotations

import copy

from osdi.action_builder.model import ActionBuilderModel
from osdi.action_builder.tag import walk_tag_schema


class ABPerson(ActionBuilderModel):
    email: str
    phone: str
    address: dict
    taggings: dict
    updates: list

    def __init__(self, service, campaign, data):
        self.taggings_by_field = {}
        self.taggings = {}
        self.tagging_updates = {}
        self.campaign = campaign
        super(ABPerson, self).__init__(service, data, "people")

        if "email_addresses" in data:
            self.email = data["email_addresses"][0]["address"]  # TODO: handle multiple emails
        else:
            self.email = None

        if "phone_numbers" in data:
            self.phone = data["phone_numbers"][0]["number"]  # TODO: handle multiple phones
        else:
            self.phone = None

        if "postal_addresses" in data:
            self.address = data["postal_addresses"][0]
        else:
            self.address = None
        self.updates = []

        self.load_taggings()

    def load_taggings(self):
        taggings = self.get_linked_collection("osdi:taggings")
        for t in taggings:
            tagging = self.campaign.parse_tagging(t)
            if tagging is not None:
                self.taggings[tagging.tag_id] = tagging

                section = tagging.section
                field = tagging.field
                if section not in self.taggings_by_field:
                    self.taggings_by_field[section] = {}
                    if field not in self.taggings_by_field[section]:
                        self.taggings_by_field[section][field] = {}
                self.taggings_by_field[section][field][tagging.name] = tagging

    def add_email(self, email):
        if email:
            self.email = email
            self.updates.append("email")  # TODO: handle multiple emails

    def add_phone(self, phone):
        if phone:
            self.phone = phone
            self.updates.append("phone")  # TODO: handle multiple numbers

    def update(self, refresh_taggings=False):
        # TODO: handle cases where you actually want multiple taggings in the same name
        for (section, field, name) in walk_tag_schema(self.tagging_updates):
            new_tagging = self.tagging_updates[section][field][name]
            existing_tagging = self.taggings_by_field[section][field][name]
            if existing_tagging is None:
                pass
            elif new_tagging is not None and new_tagging.value != existing_tagging.value:
                self.delete_taggings(section, field, name)

        post_updates = self._get_updates()
        put_updates = copy.deepcopy(post_updates["person"])
        del put_updates["identifiers"]
        post_updates["person"] = {"identifiers": post_updates["person"]["identifiers"]}

        if put_updates:
            self.service._put_request(self.link(), data=put_updates)
        if post_updates["add_tags"]:
            self.service._post_request("people", data=post_updates)

        if refresh_taggings:
            self.load_taggings()

    def _get_updates(self):
        identifiers = []
        identifiers.append(f"action_builder:{self.id}")
        person = {"identifiers": identifiers}
        add_tags = []
        for (section, field, name) in walk_tag_schema(self.tagging_updates):
            new_tagging = self.tagging_updates[section][field][name]
            new_value = new_tagging.value
            existing_tagging = self.taggings_by_field[section][field][name]
            if existing_tagging is None:
                add_tags.append(new_tagging.as_data())
            elif new_value is not None and new_value != existing_tagging.value:
                add_tags.append(new_tagging.as_data())
            self.taggings_by_field[section][field][name] = new_tagging

        for update_field in self.updates:
            if update_field == "email":
                person["email_addresses"] = []
                person["email_addresses"].append({"address": self.email, "address_type": "home"})
            elif update_field == "phone":
                person["phone_numbers"] = []
                person["phone_numbers"].append({"number": self.phone, "number_type": "Mobile"})

        return {"person": person, "add_tags": add_tags}

    def get_tagging_value(self, section, field, name=None):
        taggings = self.taggings_by_field[section][field]
        if name is None:
            return [n for n, tagging in taggings.items() if tagging.value]
        else:
            return taggings[name].value

    def delete_taggings(self, section, field, name):
        tagging = self.taggings_by_field[section][field][name]
        if tagging is not None:
            tagging.delete()
            self.taggings_by_field[section][field][name] = None

    def update_tagging(self, section, field, name, value):
        default = self.schema[section][field].default(name)
        default.value = value
        self.tagging_updates[section][field][name] = default

    @classmethod
    def person_model_from_tag_config(cls, tag_schema, class_name=None):
        if class_name is None:
            class_name = "CustomABPerson"

        def init_data(self, data):
            for section, fields in tag_schema.items():
                if section not in self.taggings_by_field:
                    self.taggings_by_field[section] = {}
                    self.tagging_updates[section] = {}
                for field, tag_config in fields.items():
                    if field not in self.taggings_by_field[section]:
                        self.taggings_by_field[section][field] = {}
                        self.tagging_updates[section][field] = {}
                    for name in tag_config.names:
                        self.taggings_by_field[section][field][name] = None
                        self.tagging_updates[section][field][name] = None

        attr_dict = {"schema": tag_schema, "_init_data": init_data}

        for tag_section in tag_schema:
            pass
        return type(class_name, (cls,), attr_dict)
