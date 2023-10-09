from rest_framework import serializers

from .model.index import *


class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "email",
            "first_name",
            "last_name",
            "oauth_provider",
            "is_authorized",
        ]
