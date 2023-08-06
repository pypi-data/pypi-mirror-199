import inspect
from django.db.models.query_utils import DeferredAttribute
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class MetabootstrapViewSet:
    """Inherit your views from this class."""

    def _get_model_attributes(self):
        model_attributes = []
        for attribute_name, attribute_object in inspect.getmembers(self.queryset.model):
            # Check if the attribute is a Django model
            if (
                type(attribute_object) in [DeferredAttribute, property]
                or type(attribute_object).__name__ == "function"
            ):
                # Append the name of the field or the field with its attributes.
                model_attributes.append(attribute_name)

        return model_attributes

    @staticmethod
    def _get_url_path(request):
        """Gets the absolute path for the given endpoint."""
        return request.path.replace("metabootstrap/", "")

    def _get_metabootstrap_functions(self, request):
        """Returns a list of dicts that contain the function name, path and view type
        of every function that has the bootstrap decorator."""
        metabootstrap_functions = []
        master_url = getattr(settings, "MASTER_URL", "MASTER_URL:8000")
        for view_name, function_object in inspect.getmembers(self, inspect.ismethod):
            if "is_metabootstrap" in vars(function_object):
                function_vars = vars(function_object)
                detail = "${pk}/" if function_vars["detail"] else ""
                metabootstrap_functions.append(
                    {
                        "url": f"{master_url}{self._get_url_path(request)}{detail}{view_name}/",
                        "methods": [method for method in function_vars["mapping"]],
                        "metabootstrap_type": function_vars["metabootstrap_type"],
                        "metabootstrap_folder": function_vars["search_folder"]
                    }
                )

        return metabootstrap_functions

    @action(detail=False, methods=["GET"])
    def metabootstrap(self, request):
        """Endpoint which returns to the frontend all the methods that use the bootstrap
        decorator."""
        model = self.queryset.model
        model_name = model.__name__
        verbose_name = model._meta.verbose_name

        module = verbose_name or model_name

        return Response(
            status=status.HTTP_200_OK,
            data={
                "module": module,
                "url_module": f"{getattr(settings, 'MASTER_URL', 'MASTER_URL:8000')}"
                              f"{self._get_url_path(request)}",
                "views": self._get_metabootstrap_functions(request),
            },
        )
