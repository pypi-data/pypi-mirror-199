from .form_factory import generate_form_data
from .detail_factory import generate_detail_data
from .wlist_factory import generate_wlist_data
from .datatable_factory import generate_datatable
from .edit_factory import generate_edit
from .filters_factory import generate_filters

METHOD_DICTIONARY = {
    "detail": ("elements", generate_detail_data, "/sidebar/"),
    "form": ("form_fields", generate_form_data, "/"),
    "datatable": ("columns", generate_datatable, "/"),
    "list": ("data", generate_wlist_data, "/"),
    "edit": ("form_fields", generate_edit, "/actions/"),
    "filters": ("filters", generate_filters, "/sidebar/")
}


def generate_data(self, request, metabootstrap_parameters):
    """Calls the method that will generate the necessary data depending on the bootstrap type."""
    key, method, _ = METHOD_DICTIONARY[metabootstrap_parameters["type"]]

    metabootstrap_data = method(
        self=self,
        metabootstrap_parameters=metabootstrap_parameters,
        request=request,
    )
    if not metabootstrap_parameters["type"] == "detail":
        metabootstrap_data.update({"view": metabootstrap_parameters["type"]})
    return metabootstrap_data
