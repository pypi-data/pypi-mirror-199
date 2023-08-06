from functools import wraps
from .data_generation.data_factory import generate_data
from .metatypes import METABOOTSTRAP_TYPES
from .data_generation.data_factory import METHOD_DICTIONARY


def metaview(metatype, field_list=None, url=None, serializer=None, search_folder=None):
    """Add metabootstrap_data to your arguments to be able to access it from the endpoint."""
    def decorator(function):
        # Validate bootstrap type
        if metatype.lower() not in METABOOTSTRAP_TYPES:
            raise TypeError(
                "Metabootstrap type is not valid, only: ", METABOOTSTRAP_TYPES.values()
            )

        @wraps(function)
        def wrapper(self, request, *args, **kwargs):
            if not field_list and not serializer:
                raise ValueError(
                    "You need to pass a list_fields or serializer parameter"
                )
            if not list_fields_are_valid(
                model_attributes=self._get_model_attributes(),
                needed_attributes=field_list,
            ):
                raise AttributeError(
                    "One of the attributes does not belong to the model."
                )

            metabootstrap_parameters = {
                "list_fields": field_list,
                "type": metatype,
                "url": url,
                "serializer": serializer,
            }

            request.viewset_url = request.path.replace(f"/{function.url_path}/", "")
            metabootstrap_data = generate_data(self, request, metabootstrap_parameters)
            # Call the endpoint
            return function(
                self, request, metabootstrap_data=metabootstrap_data, *args, **kwargs
            )

        # Add properties to method so that the _get_bootstrap_functions can find it
        wrapper.metabootstrap_type = metatype
        wrapper.search_folder = search_folder if search_folder else METHOD_DICTIONARY[metatype][2]
        wrapper.is_metabootstrap = True

        return wrapper

    return decorator


def list_fields_are_valid(model_attributes, needed_attributes):
    if needed_attributes:
        for attribute in needed_attributes:
            # If the needed attribute does not belong to the model, the parameter is not valid
            if attribute not in model_attributes:
                return False

        return True
    return True
