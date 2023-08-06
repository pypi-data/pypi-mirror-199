from django.conf import settings


def generate_datatable(*args, **kwargs):
    self = kwargs["self"]
    metabootstrap_parameters = kwargs["metabootstrap_parameters"]
    if not metabootstrap_parameters.get("url"):
        raise NameError(
            "You need to define following url that responses wlist for each datatable"
        )

    return {
        "columns": get_columns(self, metabootstrap_parameters["list_fields"]),
        "url": getattr(settings, "MASTER_URL", "MASTER_URL:8000")
        + kwargs["request"].viewset_url
        + metabootstrap_parameters["url"],
        "id": f"{self.queryset.model.__name__}".lower(),
    }


def get_columns(self, fields):
    columns = []
    for field in fields:
        field_object = getattr(self.queryset.model, field)
        field_class = field_object.__class__.__name__

        if field_class == "property":
            verbose_name = field
        elif field_class == "DeferredAttribute":
            verbose_name = getattr(
                getattr(self.queryset.model, field), "field"
            ).verbose_name
        else:
            raise TypeError("Fields have to be either properties or django fields.")
        columns.append({"id": field, "header": verbose_name})
    return columns
