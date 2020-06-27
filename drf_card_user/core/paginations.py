from rest_framework.pagination import CursorPagination


class IDPagination(CursorPagination):
    ordering = '-id'