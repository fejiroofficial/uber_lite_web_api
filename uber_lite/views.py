from rest_framework.views import APIView
from rest_framework.response import Response


class BaseView(APIView):
    @staticmethod
    def get(request):
        return Response({
            'message': 'Uber-Lite!'
        })
