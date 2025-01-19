from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from blockchain.chain import Blockchain
from blockchain.block import Block

blockchain = Blockchain()


class BlockchainView(APIView):
    """
    API cho Blockchain Service
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve the entire blockchain",
        summary="Get Blockchain",
        responses={200: "List of blocks in the blockchain"},
        tags=["Blockchain"],
    )
    def get(self, request):
        """
        Trả về toàn bộ chuỗi khối
        """
        chain = [
            {
                "index": block.index,
                "timestamp": block.timestamp,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
                "vote_data": block.vote_data,
                "vote_id": block.vote_id,
                "user_id": block.user_id,
                "nonce": block.nonce,
            }
            for block in blockchain.chain
        ]
        return Response({"blockchain": chain})

    @extend_schema(
        description="Verify the integrity of the blockchain",
        summary="Verify Blockchain",
        responses={
            200: {"description": "Blockchain is valid."},
            400: {"description": "Blockchain is invalid."},
        },
        tags=["Blockchain"],
    )
    def post(self, request):
        """Check the integrity of the blockchain"""
        if blockchain.is_chain_valid():
            return Response({"message": "Blockchain is valid."})
        return Response({"error": "Blockchain is invalid."}, status=400)


class AddBlockView(APIView):
    """Add a block to the blockchain"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Add a block to the blockchain",
        summary="Add Block",
        request=None,
        responses={201: {"description": "Block added successfully."}},
        tags=["Blockchain"],
    )
    def post(self, request):
        """
        Thêm một block mới vào chuỗi khối
        """
        # Dữ liệu giả định cho block (tùy vào ứng dụng thực tế để xử lý)
        vote_data = request.data.get("vote_data", "Default Vote Data")
        vote_id = request.data.get("vote_id", 1)
        user_id = request.user.id

        # Thêm block vào chuỗi khối
        try:
            blockchain.add_block(
                vote_data=vote_data,
                vote_id=vote_id,
                user_id=user_id,
            )
            return Response({"message": "Block added successfully."}, status=201)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
