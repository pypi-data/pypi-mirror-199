import logging
from abc import ABCMeta

from osdi.base.service import ActionService
from osdi.base.utils import parse_embedded_id


class ActionModel(object, metaclass=ABCMeta):
    service: ActionService
    model_type: str
    data: dict
    id: str

    def __init__(self, service, data, model_type):
        self.raw_data = data
        self.model_type = model_type
        self.service = service
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        try:
            self.id = [i for i in self.raw_data["identifiers"] if "action" in i][0].split(":")[-1]
        except (IndexError, KeyError):
            # Sometimes there's not an identifier. Try parsing url
            try:
                self.id = parse_embedded_id(data, "self")
            except KeyError:
                # This model is local only
                # TODO: come up with a better idea for this
                self.id = "local"

        self._init_data(data)

    def get_linked_collection(self, model_type, model_class=None):
        links = self.raw_data["_links"]
        model_link = links[model_type]["href"]
        raw_results = self.service._get_all(model_type, model_link)
        if model_class is not None:
            return [model_class(self.service, r) for r in raw_results]
        else:
            return raw_results

    def link(self, full=False):
        if full:
            prefix = self.service.uri + "/"
        else:
            prefix = ""
        return f"{prefix}{self.model_type}/{self.id}"

    # Overwrite this function in a subclass to handle initialization
    # Make sure super() is ahead of any data editing in subclass __init__
    def _init_data(self, data):
        pass
