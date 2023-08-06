from functools import wraps
from rest_framework.exceptions import ValidationError
from .log_storage import store_log


def metalog(model):
    def decorator(function):
        @wraps(function)
        def wrapper(self, request, *args, **kwargs):
            succeeded = True
            user = (
                "Anonymous"
                if request.user.get_username() == ""
                else request.user.get_username()
            )

            try:
                return function(self, request, *args, **kwargs)
            except ValidationError as error:
                succeeded = False
                store_log(
                    succeed=succeeded,
                    error_detail=error.detail["non_field_errors"][0],
                    model=self.queryset.model,
                    user=user,
                    request=request,
                    log_model=model,
                )
                raise error
            finally:
                store_log(
                    succeed=succeeded,
                    model=self.queryset.model,
                    user=user,
                    request=request,
                    log_model=model,
                )

        return wrapper

    return decorator
