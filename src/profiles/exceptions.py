from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    default_code = "not_found"
    default_detail = "User not found"
    status_code = 404


class TourNotFoundException(APIException):
    default_code = "not_found"
    default_detail = "Tour not found"
    status_code = 404
