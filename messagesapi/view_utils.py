from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


def checkAndReturn(serializer):
    """Utility method to check if a serialier is valid, and if not, throw the correct error"""
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def findByPk(model, pk):
    """Utility method to check if the request object exists, and if not, throw the correct error"""
    try:
        return model.objects.get(pk=pk)
    except:
        raise Http404('The {} does not exist'.format(model.__name__))
