from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Module, Permission, Role, User
from .serializers import ModuleSerializer, PermissionSerializer, RoleSerializer, UserSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def permissions_by_module(self, request, pk=None):
        user = self.get_object()
        module_id = request.query_params.get('module_id')
        if module_id:
            permissions = user.get_permissions_by_module(module_id)
            serializer = PermissionSerializer(permissions, many=True)
            return Response(serializer.data)
        return Response({"error": "Module ID not provided"}, status=400)
