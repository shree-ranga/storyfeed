from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


class UserItemListPagination(LimitOffsetPagination):
    default_limit = 3

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )