import json
import time

import requests

from django_http_model.models import fields


class HTTPModelManager:

    meta = None
    model = None

    def __init__(self, model) -> None:
        super().__init__()
        self.model = model
        self.meta = model.HTTPMeta

    def all(self):
        response = requests.get(self.meta.url)
        result = []
        if response.ok:
            for item_dict in json.loads(response.text):
                instance = self.model()
                import ipdb; ipdb.set_trace()
                for attribute, value in item_dict.items():
                    if hasattr(instance, attribute):
                        setattr(instance, attribute, value)
                result.append(instance)
        return result

    def __create_instance(self, instance_attributes_dict):
        instance = self.model()
        for attribute, value in self.model.__dict__.items():
            if isinstance(value, fields.HTTPField):
                instance_attr = getattr(instance, attribute)
                field_name = getattr(instance_attr, "field_name")

                if field_name is None:
                    field_name = attribute

                if field_name in instance_attributes_dict:
                    instance_attribute_value = instance_attributes_dict[field_name]

                    if isinstance(value, fields.HTTPDateField):
                        date_fmt = getattr(instance_attr, "date_fmt")
                        instance_attribute_value = time.strptime(instance_attribute_value, date_fmt)

                    setattr(instance, attribute, instance_attribute_value)

        return instance
