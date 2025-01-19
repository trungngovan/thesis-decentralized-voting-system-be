from django.utils import timezone
from rest_framework import serializers
from .models import Vote, VoteEntry
from blockchain import Blockchain
from rest_framework.exceptions import ValidationError

blockchain = Blockchain()

class VoteSerializer(serializers.ModelSerializer):
    entries_count = serializers.IntegerField(read_only=True, source="entries.count")

    class Meta:
        model = Vote
        fields = ["id", "title", "description", "created_by", "created_at", "modified_at", "end_at", "entries_count"]

class VoteEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteEntry
        fields = ["id", "vote", "user", "choice", "created_at", "modified_at"]
        extra_kwargs = {
            "user": {"read_only": True},
            "vote": {"read_only": True},
        }
class CastVoteSerializer(serializers.Serializer):
    choice = serializers.CharField()

    def validate(self, data):
        vote = self.context.get("vote")
        user = self.context.get("user")

        if vote.end_at < timezone.now():
            raise ValidationError("This vote has already ended.")

        if VoteEntry.objects.filter(vote=vote, user=user).exists():
            raise ValidationError("You have already voted.")

        return data

    def create(self, validated_data):
        vote = self.context.get("vote")
        user = self.context.get("user")
        return VoteEntry.objects.create(vote=vote, user=user, **validated_data)