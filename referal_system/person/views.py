"""person application View Configuration"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import (api_view, renderer_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (UserAuthorizeSerializer, UserGetCodeSerializer,
                          ImplementInviteSerializer)
from .services import (create_sms_code, authorize,
                       form_profile_data, implement_invite)


User = get_user_model()


class UserGetCodeView(APIView):
    """ API endpoint for getting sms-code by phone number """

    serializer_class = UserGetCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserGetCodeSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        code = create_sms_code(phone)
        return Response({'code': code}, status.HTTP_200_OK)


class UserAuthorizeView(APIView):
    """ API endpoint for checking code and authorization """

    serializer_class = UserAuthorizeSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserAuthorizeSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        result = authorize(phone, code)
        return Response(result)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
@permission_classes((IsAuthenticated,))
def profile(request) -> dict:
    """ API endpoint for viewing user profile  """

    user_data = form_profile_data(request)
    return Response(user_data, status.HTTP_200_OK)


class UserImplementInviteView(APIView):
    """ API endpoint for getting sms-code """
    serializer_class = ImplementInviteSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ImplementInviteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['invite_code']
            result = implement_invite(request, code)
            return Response(result)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
