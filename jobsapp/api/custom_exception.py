from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Override drf default validation error message response and sends as a list
    :param exc:
    :param context:
    :return: response obj
    """

    response = exception_handler(exc, context)
    if response is not None:
        data = response.data
        response.data = {}
        errors = []
        for field, value in data.items():
            if type(value) is list:
                my_dict = {field: value[0]}
                # errors.append("{}: {}".format(field, value[0]))
                errors.append(my_dict)
            else:
                errors.append({field: value})
                # errors.append("{}: {}".format(field, value))

        response.data["errors"] = errors
        response.data["status"] = False

        if type(exc) is ValidationError:
            response.data["message"] = ""
            for field, value in data.items():
                response.data["message"] += value[0] + " "
        else:
            response.data["message"] = str(exc)

    return response


"""
# to work with this custom error handler, save this file in your project,
#add this in settings.py 
 REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.api.custom_exception.custom_exception_handler', #location for your file
}
# and add raise_exception=True in is_valid() method
if serializer.is_valid(raise_exception=True):
"""
