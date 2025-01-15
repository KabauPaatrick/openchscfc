from rest_framework import serializers
from .models import Module, Permission, Role, User


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)
    modules = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all(), many=True)

    class Meta:
        model = Role
        fields = '__all__'

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        modules_data = validated_data.pop('modules', [])
        role = Role.objects.create(**validated_data)

        # Add permissions and modules to the role (permissions and modules are now IDs, not instances)
        role.permissions.set(permissions_data)
        role.modules.set(modules_data)

        return role

    def update(self, instance, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        modules_data = validated_data.pop('modules', [])

        # Update role fields
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update permissions
        instance.permissions.set(permissions_data)

        # Update modules
        instance.modules.set(modules_data)

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'role',
            'date_joined', 'is_staff', 'is_active', 'is_superuser',
            'created_at', 'updated_at', 'groups', 'user_permissions'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Handle password hashing
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password updates securely
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user