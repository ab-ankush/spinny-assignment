from django.shortcuts import render

from .models import Box
from .serializers import *
from .utils import check_constraints, apply_filters

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


# Create your views here.

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class CreateBoxView(APIView):
    serializer_class = CreateBoxSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsStaffUser]

    def post(self, request):
        try:

            valid, message = check_constraints(request.user)
            if not valid:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(creator=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UpdateBoxView(APIView):
    serializer_class = UpdateBoxSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsStaffUser]

    def patch(self, request, pk):
        try:

            valid, message = check_constraints(request.user)
            if not valid:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            box = Box.objects.get(pk=pk)
            serializer = self.serializer_class(
                instance=box, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.validated_data.pop('creator', None)
                serializer.validated_data.pop('created_at', None)
                serializer.save(last_modified_by=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Box.DoesNotExist:
            return Response('Box does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ListAllBoxesView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            Boxes = Box.objects.all()

            Boxes = apply_filters(Boxes, request, False)

            res = []
            for box in Boxes:
                temp = {}
                temp['length'] = box.length
                temp['breadth'] = box.breadth
                temp['height'] = box.height
                temp['area'] = box.area
                temp['volume'] = box.volume
                if (request.user.is_staff):
                    temp['created_at'] = box.created_at
                    temp['updated_at'] = box.updated_at
                    temp['creator'] = box.creator.username
                    temp['last_modified_by'] = box.last_modified_by and box.last_modified_by.username or 'None'
                res.append(temp)
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ListUserBoxesView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request):
        try:
            Boxes = Box.objects.filter(creator=request.user)

            Boxes = apply_filters(Boxes, request, True)

            res = []
            for box in Boxes:
                temp = {}
                temp['length'] = box.length
                temp['breadth'] = box.breadth
                temp['height'] = box.height
                temp['area'] = box.area
                temp['volume'] = box.volume
                temp['created_at'] = box.created_at
                temp['updated_at'] = box.updated_at
                temp['creator'] = box.creator.username
                temp['last_modified_by'] = box.last_modified_by and box.last_modified_by.username or 'None'
                res.append(temp)
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class DeleteBoxView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsStaffUser]

    def delete(self, request, pk):
        try:
            box = Box.objects.get(pk=pk)
            if box.creator != request.user:
                return Response('You are not authorized to delete this box.', status=status.HTTP_401_UNAUTHORIZED)
            box.delete()
            return Response('Box deleted successfully', status=status.HTTP_200_OK)
        except Box.DoesNotExist:
            return Response('Box does not exist.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
