from __future__ import annotations

from enum import Enum
from typing import Generator

from osdi.action_builder.model import ActionBuilderModel
from osdi.base.service import ActionService


class ABTagType(Enum):
    STANDARD = "standard"
    DATE = "date"
    NUMBER = "number"
    NOTE = "note"
    SHIFT = "shift"
    ADDRESS = "address"

    def __str__(self):
        return f"{self.value}"


class ABTagging(ActionBuilderModel):
    # Taggings inherit section, field(_key), name, and field_type from tag
    # Then have their own value
    value: str

    def __init__(self, service, tag, data):
        uri = f"{service.uri}/tags/{tag.id}"
        tag_service = ActionService(uri, service.api_key)
        super(ABTagging, self).__init__(tag_service, data, "tagging")
        self.tag = tag
        if tag.field_type == ABTagType.DATE:
            self.value = data.get("action_builder:date_response")
        elif tag.field_type == ABTagType.STANDARD:
            self.value = True
        else:
            raise NotImplementedError(f"ABTagging type {tag.field_type} not implemented yet!")

    @property
    def section(self):
        return self.tag.section

    @property
    def field(self):
        return self.tag.field

    @property
    def field_type(self):
        return self.tag.field_type

    @property
    def name(self):
        return self.tag.name

    @property
    def tag_id(self):
        return self.tag.id

    def as_data(self):
        data = {
            "action_builder:name": self.name,
            "action_builder:section": self.section,
            "action_builder:field": self.field,
        }
        if self.field_type == ABTagType.DATE:
            data["action_builder:date_response"] = self.value

        return data

    def delete(self):
        if self.service is None:
            raise NotImplementedError("Can't delete default tagging")
        self.service._delete_request(f"taggings/{self.id}")

    def _get_updates(self):
        raise NotImplementedError("Tagging update not yet implemented")

    def __str__(self):
        return f"Tagging<{self.tag.field} {self.tag.name}:{self.value}>"

    def __repr__(self):
        return self.__str__()


class ABTag(ActionBuilderModel):
    section: str
    field: str
    name: str
    field_type: ABTagType
    # Hierarchy of values is section -> field -> name (-> value, in ABTagging)

    def __init__(self, service, data):
        super(ABTag, self).__init__(service, data, "tag")
        self.name = data["name"]
        self.field_type = ABTagType(data["action_builder:field_type"])
        self.section = data["action_builder:section"]
        self.field = data["action_builder:field"]

    def _get_updates(self):
        raise NotImplementedError("Tag update not yet implemented")

    def __str__(self):
        return f"Tag<{self.section}:{self.field}; value:{self.name}>"

    def __repr__(self):
        return self.__str__()


# TODO: split these into different subclasses
class ABTagConfig:
    names: object
    field_type: ABTagType

    def __init__(self, tag):
        self.field_type = tag.field_type
        if tag.field_type == ABTagType.DATE:
            self.names = {}
        elif tag.field_type == ABTagType.STANDARD:
            self.names = {}
        else:
            raise NotImplementedError(f"ABTagConfig type {tag.field_type} not implemented yet!")

    def default(self, name):
        tag = self.names[name]
        default = ABTagging(tag.service, tag, tag.raw_data)
        if self.field_type == ABTagType.STANDARD:
            default.value = False
        return default

    def add_name(self, tag):
        self.names[tag.name] = tag

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def __getattr(self, name):
        return self.names[name]


def parse_tag_schema(tags_list: list) -> dict:  # TODO: create config type
    config = {}
    for t in tags_list:
        if t.section not in config:
            config[t.section] = {}

        if t.field not in config[t.section]:
            config[t.section][t.field] = ABTagConfig(t)
        config[t.section][t.field].add_name(t)

    return config


def walk_tag_schema(schema: dict) -> Generator[tuple]:
    for section in schema:
        for field in schema[section]:
            for name in schema[section][field]:
                if schema[section][field][name] is not None:
                    yield (section, field, name)
