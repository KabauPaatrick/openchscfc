from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Module, Permission, Role, User
from .serializers import ModuleSerializer, PermissionSerializer, RoleSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], url_path='permissions_by_module')
    def permissions_by_module(self, request, pk=None):
        user = self.get_object()
        module_id = request.query_params.get('module_id')  # Get the module_id from query parameters

        if not module_id:
            return Response({"error": "module_id is required."}, status=400)

        try:
            module = Module.objects.get(id=module_id)  # Fetch the module by ID
        except Module.DoesNotExist:
            return Response({"error": "Module not found."}, status=404)

        # Get the user's role and filter permissions through the role's modules
        if user.role:
            permissions = Permission.objects.filter(
                roles=user.role, 
                roles__modules=module  # Correctly filter permissions through the role's modules
            ).distinct()
        else:
            permissions = Permission.objects.none()  # No permissions if the user has no role

        # Serialize and return the permissions
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    @action(detail=True, methods=['get'], url_path='permissions')
    def permissions(self, request, pk=None):
        module = self.get_object()
        # Filter permissions associated with this module
        permissions = Permission.objects.filter(modules=module)
        
        # Serialize and return permissions
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
