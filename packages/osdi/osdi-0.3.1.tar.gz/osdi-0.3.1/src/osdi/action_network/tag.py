from __future__ import annotations
from osdi.base.model import ActionModel


class ANTagging(ActionModel):
    def __init__(self, service, tag, data):
        super(ANTagging, self).__init__(service, data, "tagging")
        self.tag = tag
        self.name = tag["name"]

    def delete(self):
        self.service._delete_request(self.raw_data["_links"]["self"]["href"], is_full=True)

    @classmethod
    def dummy_tagging(cls, service, tag):
        return cls(service, tag, {})
