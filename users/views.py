from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer

@extend_schema_view(
    list=extend_schema(
        description="Retrieve the authenticated user's information",
        summary="Get user details",
        responses=UserSerializer,
    ),
    retrieve=extend_schema(
        description="Retrieve the authenticated user's detailed information",
        summary="Get detailed user information",
        responses=UserSerializer,
    ),
    update=extend_schema(
        request=UserUpdateSerializer,
        description="Update the authenticated user's information",
        summary="Update user details",
        responses=UserSerializer,
    ),
    partial_update=extend_schema(
        request=UserUpdateSerializer,
        description="Partially update the authenticated user's information",
        summary="Partial update user details",
        responses=UserSerializer,
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing the authenticated user's information.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Chỉ hiển thị thông tin của chính người dùng hiện tại
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        # Sử dụng serializer khác khi update
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer
