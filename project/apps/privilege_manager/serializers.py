from rest_framework import serializers

from apps.privilege_manager.models import Team


# Serializers define the API representation.
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]
