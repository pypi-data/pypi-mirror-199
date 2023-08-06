from datetime import datetime
from .models import Log
from .models import SimpleLog


def store_log(succeed, model, user, request, log_model, error_detail=None):
    succeed_value = 1
    failure_value = 2
    status = succeed_value if succeed else failure_value
    if log_model == Log:
        Log.objects.create(
            status=status,
            error=error_detail,
            object_type=model.__name__,
            user=user,
            method=getattr(Log, request.method),
            path=request.path,
        )
    else:
        log = (
            f"{datetime.now()}: method {request.method} - {request.path}"
            f" on object type {model} by user {user}. Status: {status}"
        )
        SimpleLog.objects.create(message=log)
