from abc import abstractmethod, ABC

import re
from typing import Any, Dict, List

from ..utils import root_logger
from ..utils.constants import BASE_UUID_PATTERN, HTTP_GET


class Element(ABC):
    """Base class of all SOIL elements.



    """
    UUID_PATTERN = re.compile(BASE_UUID_PATTERN)

    def __init__(self, uuid: str, name: str, description: str, ontology: str = None):
        if not isinstance(name, str) or name == '':
            raise Exception('{}: Name is no string or the empty string!'.format(uuid))
        if not isinstance(description, str) or description == '':
            raise Exception('{}: Description is no string or the empty string!'.format(uuid))
        if ontology is not None and not isinstance(ontology, str):
            raise Exception('{}: Onthology is no string!'.format(uuid))
        if not isinstance(uuid, str) or not Element.UUID_PATTERN.match(uuid):
            raise Exception('Cannot use uuid {}. Wrong format!'.format(uuid))
        else:
            self._uuid = uuid
        self._name = name
        self._description = description
        self._ontology = ontology

    @property
    def uuid(self):
        return self._uuid

    def __getitem__(self, item: str, method: int = HTTP_GET) -> Any:
        if item == "uuid":
            return self._uuid
        if item == "name":
            return self._name
        if item == "description":
            return self._description
        if item == "ontology":
            return self._ontology
        raise KeyError("{}: Key error. No attribute is named '{}'".format(self.uuid, item))

    def __setitem__(self, key: str, value: Any):
        if key == "name":
            if not isinstance(value, str) or value == '':
                raise Exception('{}: Name is no string or the empty string!'.format(self.uuid))
            self._name = value
        elif key == "description":
            if not isinstance(value, str) or value == '':
                raise Exception('{}: Description is no string or the empty string!'.format(self.uuid))
            self._description = value
        elif key == "ontology":
            if value is not None and not isinstance(value, str):
                raise Exception('{}: Ontology is no string!'.format(self.uuid))
            self._ontology = value
        else:
            raise KeyError(
                "{}: Key error. No attribute is named '{}' or it should not be changed".format(self.uuid, key))

    def serialize(self, keys: List[str], legacy_mode: bool, method: int = HTTP_GET) -> Dict:
        res = {'uuid': self._uuid}
        for key in keys:
            res[key] = self.__getitem__(key, method)
        if not keys:  # list is empty => serialize complete component
            res['name'] = self._name
            res['description'] = self._description
            res['ontology'] = self._ontology
        return res

    @staticmethod
    @abstractmethod
    def deserialize(dictionary: Dict):
        ...
