from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination


class WebixPagination(LimitOffsetPagination):
    limit_query_param = "count"
    offset_query_param = "start"
    max_limit = None
    default_limit = 10

    def get_paginated_response(self, data):
        return OrderedDict(
            [
                ("total_count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("pos", self.offset),
                ("data", data),
            ]
        )


def generate_wlist_data(*args, **kwargs):
    self = kwargs["self"]
    request = kwargs["request"]
    queryset = self.get_queryset()
    fields = kwargs["metabootstrap_parameters"]["list_fields"]
    paginator = WebixPagination()
    queryset = paginator.paginate_queryset(queryset, request, self)
    wlist = create_metabootstrap_list(self, queryset, fields)
    return paginator.get_paginated_response(wlist)


def create_metabootstrap_list(self, records, fields):
    """Creates the list for the json."""
    metabootstrap_list = []
    for record in records:
        metabootstrap_object = {}
        for field_name in fields:
            field_object = getattr(self.queryset.model, field_name)
            field_type = type(field_object).__name__

            if field_type not in ["property", "function"]:
                field_object = field_object.field
            field_choices = getattr(field_object, "choices", None)
            if field_choices:
                display = f"get_{field_name}_display"
                display_method = getattr(record, display)
                metabootstrap_object.update({field_name: display_method()})
            else:
                value = getattr(record, field_name) or "-"
                if field_object.__class__.__name__ == "function":
                    value = value()
                metabootstrap_object.update({field_name: value})
        metabootstrap_list.append(metabootstrap_object)
    return metabootstrap_list
