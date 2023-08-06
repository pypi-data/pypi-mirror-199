import os
from django.urls import reverse

#  TODO: Add datepicker_iso
FIELD_TYPE = {
    "BigAutoField": "number_field",
    "ChoiceField": "choice_field",
    "DateField": "date_field",
    "DecimalField": "decimal_field",
    "ManyToManyField": "multi_server_autocomplete",
    "IntegerField": "number_field",
    "WebixForeignKey": "server_autocomplete",
    "CharField": "text_field",
    "TextField": "textarea_field",
    "EmailField": "text_field",
    "SmallIntegerField": "choice_field",
}


def generate_form_data(*args, **kwargs):
    """Make a dict with each field's data."""
    metabootstrap_parameters = kwargs["metabootstrap_parameters"]
    serializer = metabootstrap_parameters["serializer"]
    self = kwargs["self"]

    if serializer and "Meta" not in vars(serializer):
        return get_response_with_declared_fields(metabootstrap_parameters["serializer"])
    else:
        return get_response_with_model_fields(
            metabootstrap_parameters["serializer"],
            model=self.queryset.model,
            list_fields=metabootstrap_parameters["list_fields"],
        )


def get_response_with_declared_fields(serializer):
    form_fields = {}
    for field in serializer._declared_fields:
        field_object = serializer._declared_fields[field]
        placeholder = field_object.help_text or field.replace("_", " ").capitalize()
        view = FIELD_TYPE[field_object.__class__.__name__]
        label = (
            field_object.label
            if getattr(field_object, "label", None)
            else field.replace("_", " ")
        ).capitalize()

        inner_json_field = {
            "name": field,
            "placeholder": placeholder,
            "view": view,
            "label": label,
            "required": field_object.required or False,
            "disabled": field_object.read_only or False
        }

        json_field = {
            "field": inner_json_field,
            "max_length": getattr(field_object, "max_length", None),
            "name": field,
            "type": field_object.__class__.__name__,
        }

        if view == "choice_field":
            json_field.update(
                {
                    "choices": get_choices_from_declared(
                        serializer._declared_fields, field
                    )
                }
            )

        form_fields.update({field: json_field})
    return {"form_fields": form_fields}


def get_response_with_model_fields(serializer, model, list_fields, instance=None):
    form_model = serializer.Meta.model if serializer else model
    fields = serializer.Meta.fields if serializer else list_fields
    form_fields = {}

    for field in fields:
        is_declared = (
            field in serializer._declared_fields.keys() if serializer else False
        )
        field_kwargs = (
            serializer.Meta.extra_kwargs.get(field)
            if serializer and getattr(serializer.Meta, "extra_kwargs", None)
            else None
        )

        field_object = (
            serializer._declared_fields[field]
            if is_declared
            else getattr(form_model, field)
        )
        if type(field_object).__name__ in ["property", "function"]:
            continue
        field_object = field_object.field
        view = FIELD_TYPE[field_object.__class__.__name__]
        placeholder = get_placeholder(
            field_kwargs, serializer, field, field_object, form_model
        )

        label = getattr(field_object, "label", None) or getattr(
            field_object, "verbose_name", None
        )
        max_length = getattr(field_object, "max_length", None) or getattr(
            field_object, "max_length", None
        )
        required = (
            getattr(field_object, "required", None)
            if is_declared
            else not getattr(field_object, "null", None)
        )
        readonly = getattr(field_object, "readonly", False)

        inner_json_field = {
            "name": field,
            "placeholder": placeholder,
            "view": view,
            "label": label,
            "required": required,
            "disabled": readonly
        }

        if instance:
            inner_json_field.update({"value": getattr(instance, field)})

        json_field = {
            "field": inner_json_field,
            "max_length": max_length,
            "name": field,
            "type": field_object.__class__.__name__,
        }

        if view == "choice_field":
            json_field.update({"choices": get_choices_from_model(model, field)})

        form_fields.update({field: json_field})
    return {"form_fields": form_fields}


def get_placeholder(field_kwargs, serializer, field, field_object, form_model):
    if field_kwargs:
        return field_kwargs.get("placeholder")
    elif field_object.help_text:
        return field_object.help_text
    elif serializer and field not in serializer._declared_fields:
        return (
            getattr(form_model, field).field.help_text
            or getattr(form_model, field).field.verbose_name
        )
    else:
        return field.replace("_", " ").capitalize()


def get_choices_from_model(model, field):
    return [
        {"id": value, "value": display_name}
        for value, display_name in getattr(model, field).field.choices
    ]


def get_choices_from_declared(attributes, field):
    return [
        {"id": key, "value": attributes[field].choices[key]}
        for key in attributes[field].choices.keys()
    ]
