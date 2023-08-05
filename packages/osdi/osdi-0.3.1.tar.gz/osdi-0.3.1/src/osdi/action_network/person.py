from __future__ import annotations

from osdi.action_network.tag import ANTagging
from osdi.base.model import ActionModel


class ANPerson(ActionModel):
    email: str
    phone: str
    addresses: list
    updates: dict

    def __init__(self, service, data):
        self.taggings_by_field = {}
        self.taggings = {}
        self.tagging_updates = {}
        super(ANPerson, self).__init__(service, data, "people")
        if data.get("email_addresses"):
            self.email = data["email_addresses"][0].get("address")  # TODO: handle multiple emails
        else:
            self.email = None

        if data.get("phone_numbers"):
            self.phone = data["phone_numbers"][0].get("number")  # TODO: handle multiple phones
        else:
            self.phone = None
        self.custom_fields = data["custom_fields"]

        self.taggings = self.get_linked_collection("osdi:taggings")
        self.tags = {}
        for t in self.taggings:
            tag = ANTagging(self.service, self.service.parse_tagging(t), t)
            self.tags[tag.name] = tag

        self.fields_to_update = {}
        self.taggings_to_remove = {}
        self.taggings_to_add = {}

    def update_address(self, line1, line2, state, country, zipcode):
        # print("update address not implemented yet")
        pass

    def update_tag(self, tag_name, set_val):
        if tag_name in self.tags:
            if not set_val:
                self.taggings_to_remove[tag_name] = self.tags[tag_name]
                del self.tags[tag_name]
                if tag_name in self.taggings_to_add:
                    del self.taggings_to_add[tag_name]
        elif set_val:
            self.taggings_to_add[tag_name] = set_val
            tag = self.service.tags_by_name[tag_name]
            self.tags[tag_name] = ANTagging.dummy_tagging(self.service, tag)
            if tag_name in self.taggings_to_remove:
                del self.taggings_to_remove[tag_name]

    def update_field(self, field_name, value):
        if self.custom_fields.get(field_name) != value:
            self.custom_fields[field_name] = value
            self.fields_to_update[field_name] = True

    def update(self):
        updates = self._get_updates()
        url = self.link()
        if updates:
            self.service._put_request(url, data=updates)
        for _, tagging in self.taggings_to_remove.items():
            tagging.delete()
        for tag_name, tagging in self.taggings_to_add.items():
            self.service.add_tagging(self, tag_name)

    def _get_updates(self):
        updates = {"custom_fields": {k: self.custom_fields[k] for k in self.fields_to_update}}
        self.fields_to_update = {}
        return updates

    def get_tagging_value(self, section, field, name=None):
        taggings = self.taggings_by_field[section][field]
        if name is None:
            return [n for n, tagging in taggings.items() if tagging.value]
        else:
            return taggings[name].value

    def delete_taggings(self, section, field, name=None):
        for tagging in self.taggings_by_field.get(section, {}).get(field, []):
            if name is None or tagging.name == name:
                tagging.delete()
