from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class UserSearchListPagination(LimitOffsetPagination):
    default_limit = 2

    # TODO: - customize the paginated response
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)