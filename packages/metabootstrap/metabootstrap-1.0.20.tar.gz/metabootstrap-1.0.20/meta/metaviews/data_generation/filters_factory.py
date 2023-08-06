from .form_factory import generate_form_data


def generate_filters(*args, **kwargs):
    form_data = generate_form_data(*args, **kwargs)
    search_dict = {
        "search": {
            "field": {
                "view": "text_field",
                "name": "search",
                "label": "Consulta",
                "placeholder": "Consulta",
                "required": False,
                "disabled": False
            }
        },
        "name": "search",
        "type": "CharField",
        "max_length": None
    }
    form_data["form_fields"].update(search_dict)
    return form_data
