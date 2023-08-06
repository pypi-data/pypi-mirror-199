from django.db import models


class SimpleLog(models.Model):
    message = models.TextField(max_length=255, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Simple log"
        verbose_name_plural = "Simple logs"


class Log(models.Model):
    FAILURE = 1
    SUCCEED = 2

    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5
    CONNECT = 6
    OPTIONS = 7
    HEAD = 8

    STATUS = ((FAILURE, "FAILURE"), (SUCCEED, "SUCCEED"))

    METHODS = (
        (GET, "GET"),
        (POST, "POST"),
        (PUT, "PUT"),
        (PATCH, "PATCH"),
        (DELETE, "DELETE"),
        (CONNECT, "CONNECT"),
        (OPTIONS, "OPTIONS"),
        (HEAD, "HEAD"),
    )

    status = models.SmallIntegerField(choices=STATUS, editable=False)
    error = models.TextField(max_length=255, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    object_type = models.CharField(max_length=255, editable=False)
    user = models.CharField(max_length=255, editable=False)
    method = models.SmallIntegerField(choices=METHODS, editable=False)
    path = models.CharField(max_length=255, editable=False)

    def __str__(self):
        return f"{self.path} - By {self.user} - Status: {self.get_status_display()}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
