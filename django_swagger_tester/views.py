from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from django_swagger_tester.configuration import settings
from django_swagger_tester.utils import safe_validate_response, copy_response


class ResponseValidationView(APIView):
    def finalize_response(self, request: HttpRequest, response: Response, *args, **kwargs) -> Response:
        """
        Overwrites APIView finalize_response to validate response before returning the response.
        """
        response = super(ResponseValidationView, self).finalize_response(request, response, *args, **kwargs)
        if settings.VIEWS.RESPONSE_VALIDATION.DEBUG:
            response.render()
            copied_response = copy_response(response)
            safe_validate_response(
                response=copied_response,
                path=request.path,
                method=request.method,
                func_logger=settings.VIEWS.RESPONSE_VALIDATION.LOGGER,
            )
        return response
