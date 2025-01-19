from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import Vote, VoteEntry
from .serializers import VoteSerializer, VoteEntrySerializer, CastVoteSerializer


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all votes",
        summary="List all votes",
        responses=VoteSerializer(many=True),
    ),
    retrieve=extend_schema(
        description="Retrieve details of a specific vote",
        summary="Get vote details",
        responses=VoteSerializer,
    ),
    create=extend_schema(
        description="Create a new vote",
        summary="Create vote",
        request=VoteSerializer,
        responses=VoteSerializer,
    ),
    update=extend_schema(
        description="Update a specific vote",
        summary="Update vote",
        request=VoteSerializer,
        responses=VoteSerializer,
    ),
    partial_update=extend_schema(
        description="Partially update a vote",
        summary="Partial update vote",
        request=VoteSerializer,
        responses=VoteSerializer,
    ),
    destroy=extend_schema(
        description="Delete a vote",
        summary="Delete vote",
        responses=None,
    ),
)
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        description="Cast a vote for a specific voting instance",
        summary="Cast a vote",
        request=CastVoteSerializer,
        responses={
            200: {"description": "Vote cast successfully."},
            400: {"description": "Validation error."},
        },
    )
    @action(detail=True, methods=["post"])
    def cast_vote(self, request, pk=None):
        vote = get_object_or_404(Vote, pk=pk)
        serializer = CastVoteSerializer(data=request.data, context={"vote": vote, "user": request.user})
        serializer.is_valid(raise_exception=True)
        vote_entry = serializer.save()
        return Response({"message": "Vote cast successfully!", "entry_id": vote_entry.id})

    @extend_schema(
        description="Retrieve all vote entries for a specific vote",
        summary="List vote entries",
        responses=VoteEntrySerializer(many=True),
    )
    @action(detail=True, methods=["get"])
    def entries(self, request, pk=None):
        vote = get_object_or_404(Vote, pk=pk)
        entries = vote.entries.all()
        serializer = VoteEntrySerializer(entries, many=True)
        return Response(serializer.data)
