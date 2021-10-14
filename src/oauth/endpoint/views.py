from rest_framework import viewsets, parser, permissions

from .. import serializer


class UserView(viewsets.ModelViewSet):
    """Просмотр и редактирование данных пользователя
    """
    parser_classes = (parser.MultiPartParser,)
    serislizer_classes = serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()