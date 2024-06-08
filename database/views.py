from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
)

from database.models import Problem
from database.serializer import ProblemSerializer


class ProblemViewSet(viewsets.ViewSet):
    def retrieve(self, request, problem_id):
        try:
            problem = Problem.objects.get(id=problem_id)

        # Raise exception if sequence does not exist
        except Problem.DoesNotExist:
            raise NotFound(
                detail="Object does not exist",
                code="not_found",
            )

        # Raise exception if user try to call other user's sequence
        if request.user != problem.project.user:
            raise PermissionDenied(
                detail="You do not have permission to access this object",
                code="permission_denied",
            )

        serializer = ProblemSerializer(problem)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def list_problems(self, request):
        problem_list = Problem.objects.all()
        serializer = ProblemSerializer(problem_list, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
