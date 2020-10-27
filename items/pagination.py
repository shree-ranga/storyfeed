from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status


class FeedPagination(LimitOffsetPagination):
    default_limit = 30

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )


class ExploreItemListPagination(LimitOffsetPagination):
    default_limit = 30

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )


class HashTagItemListPagination(LimitOffsetPagination):
    default_limit = 30

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )


class UserItemListPagination(LimitOffsetPagination):
    default_limit = 30

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )

class PostLikedUserPagination(LimitOffsetPagination):
    default_limit = 30

    def get_paginated_response(self, data):
        return Response(
            {"count": self.count, "results": data}, status=status.HTTP_200_OK
        )
