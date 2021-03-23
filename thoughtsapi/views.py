
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        '/api/token': reverse('token_obtain_pair', request=request, format=format),
        '/api/token/refresh': reverse('token_refresh', request=request, format=format),
        '/api/users': reverse('user-list', request=request, format=format),
        '/api/thoughts': reverse('thought-list', request=request, format=format)
    })
