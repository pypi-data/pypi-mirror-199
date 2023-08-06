from .form_factory import get_response_with_model_fields


def generate_edit(*args, **kwargs):
    metabootstrap_parameters = kwargs["metabootstrap_parameters"]
    self = kwargs["self"]
    instance = self.get_object()
    return get_response_with_model_fields(
        metabootstrap_parameters["serializer"],
        model=self.queryset.model,
        list_fields=metabootstrap_parameters["list_fields"],
        instance=instance,
    )
