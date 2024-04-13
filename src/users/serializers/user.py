from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    access_level = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "access_level", "groups", "permissions"]
        extra_kwargs = {"password": {"write_only": True}}
    
    def get_access_level(self, obj: User):
        """ Assuming `access_level` is a custom method or a property that summarizes user's permissions """ 
        if not obj.is_active:
            return "inactive"
        if obj.is_superuser:
            return "admin"
        if obj.is_staff:
            return "staff"
        return "basic"
    
    def get_permissions(self, obj: User):
        """ Assuming `permissions` is a custom method or a property that summarizes user's permissions """ 
        return [perm for perm in obj.get_all_permissions()]