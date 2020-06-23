from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


class CommentPagination(LimitOffsetPagination):
    default_limit = 20

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )
