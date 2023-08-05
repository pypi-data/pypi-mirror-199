from abc import abstractmethod

from osdi.base.model import ActionModel


class ActionBuilderModel(ActionModel):
    campaign_id: str

    def __init__(self, service, data, model_type):
        super(ActionBuilderModel, self).__init__(service, data, model_type)
        if self.model_type == "campaign":
            self.campaign_id = self.id
        else:
            campaign_link = data["_links"]["action_builder:campaign"]["href"]
            self.campaign_id = campaign_link.split("/")[-1]

    def update(self):
        updates = self._get_updates()
        url = self.model_type
        res = self.service._post_request(url, data=updates)
        return res

    @abstractmethod
    def _get_updates(self):
        pass
