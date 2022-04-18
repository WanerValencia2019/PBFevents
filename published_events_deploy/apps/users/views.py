from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# jwt - AUTH
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# custom serializers
from .serializers import RegisterSerializer, UserSerializer
from ..utils import get_tokens_for_user


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data

        del data["password"]

        token = get_tokens_for_user(user)

        return Response({"data": {"user": data, "token": token}}, status.HTTP_201_CREATED)


class UserView(ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return self.request.user

    @action(detail=False, methods=["GET"], name="profile", url_path="profile")
    def profile(self, request):
        user = self.get_queryset()
        serializer = UserSerializer(user, context={"request": request})
        return Response({"data": { "user": serializer.data}}, status.HTTP_200_OK)
