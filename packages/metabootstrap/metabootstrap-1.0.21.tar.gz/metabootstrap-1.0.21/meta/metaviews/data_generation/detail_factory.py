def generate_detail_data(*args, **kwargs):
    self = kwargs["self"]
    list_fields = kwargs["metabootstrap_parameters"]["list_fields"]
    field_list = []
    model = self.queryset.model
    database_object = self.get_object()

    for field in list_fields:
        field_object = getattr(model, field)
        value = getattr(database_object, field) or "-"
        if field_object.__class__.__name__ == "function":
            value = value()
        if field_object.__class__.__name__ == "DeferredAttribute":
            verbose_name = field_object.field.verbose_name or field
        else:
            verbose_name = field
        field_list.append(
            {
                "label": verbose_name,
                "type": "text",
                "id": field,
                "value": value,
            }
        )
    metabootstrap_data = {
        "elements": field_list,
        "view": "property",
        "id": self.kwargs["pk"],
    }
    return metabootstrap_data
