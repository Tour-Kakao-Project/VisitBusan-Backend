from rest_framework import serializers

from .model.index import *


class MemberSerializers(serializers.ModelSerializer):
    oauth_provider = serializers.SerializerMethodField()

    def get_oauth_provider(self, obj):
        return obj.get_oauth_provider_display()

    class Meta:
        model = Member
        fields = [
            "email",
            "first_name",
            "last_name",
            "oauth_provider",
            "is_authorized",
        ]
