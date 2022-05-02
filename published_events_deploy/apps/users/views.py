from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

# jwt - AUTH
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# custom serializers
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from ..utils import get_binary_content, get_tokens_for_user


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

    @action(detail=False, methods=["GET"], name="profile", url_path="profile", url_name="profile")
    def profile(self, request):
        user = self.get_queryset()
        serializer = UserSerializer(user, context={"request": request})
        return Response({"data": {"user": serializer.data}}, status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], name="update_image_profile", url_path="update_image_profile")
    def update_image_profile(self, request, *args, **kwargs):
        image_base_64 = request.data.get("image", None)
        image = get_binary_content(image_base_64)
        user = self.get_queryset()
        dir(image)
        try:
            if image_base_64 is None:
                return Response({"message": ["El campo imagen es requerido"]}, status=status.HTTP_400_BAD_REQUEST)

            if not image:
                return Response({"message": ["La imagén no es válida"]}, status=status.HTTP_400_BAD_REQUEST)

            """ if image.size > 1024000:
                return Response({"message": ["El tamaño del archivo excede el maximo permitido(1MB)"]},
                                status=status.HTTP_400_BAD_REQUEST)

            if not image.content_type.split("/")[0] == "image":
                return Response({"message": ["Imagen no válida, revisa el formato del archivo"]},
                                status=status.HTTP_400_BAD_REQUEST)"""

            user.image.save(user.first_name + ".jpg", image, save=False)
            user.save()
            print(user.image)
            user_serialized = UserSerializer(user, context={"request": request}).data
            print(user_serialized)
            return Response(
                {"data": {"message": "Imagen actualiza correctamente", "image": user_serialized.get("image")}},
                status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Error al actualizar la imagen, intenta más tarde"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["PUT", "POST"], name="update profile", url_path="update_profile")
    def update_user_profile(self, request, *args, **kwargs):
        user: CustomUser = self.get_queryset()
        data: dict = request.data
        print(data)
        if data.get("identification", None) is not None:
            identification_exist = CustomUser.objects.filter(
                identification__exact=data.get("identification")).distinct().exists()
            if user.identification == data.get("identification"):
                pass
            elif identification_exist and user.identification != data.get("identification"):
                return Response({"message": "La identificación ya existe"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.identification = data.get("identification")

        elif data.get("description", None) is not None:
            print(data.get("description"))
            user.description = data.get("description")

        elif data.get("first_name", None) is not None:
            print(data.get("first_name"))
            user.first_name = data.get("first_name")

        elif data.get("last_name", None) is not None:
            print(data.get("last_name"))
            user.last_name = data.get("last_name")

        user.save()
        user_data = UserSerializer(user, context={"request": request}).data

        return Response({"data": {"user": user_data}}, status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], name="change profile", url_path="change_password")
    def change_password(self, request, *args, **kwargs):
        user: CustomUser = self.get_queryset()
        data: dict = request.data

        old_password = data.get("old_password", None)
        new_password = data.get("new_password", None)
        confirm_password = data.get("confirm_password", None)

        if not old_password:
            return Response({"message": ["old_password es requerido"]}, status=status.HTTP_400_BAD_REQUEST)

        elif not new_password:
            return Response({"message": ["new_password es requerido"]}, status=status.HTTP_400_BAD_REQUEST)

        elif not confirm_password:
            return Response({"message": ["confirm_password es requerido"]}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password == confirm_password:
            return Response({"message": ["La nueva contraseñas debe coincidir con la confirmación"]}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"message": ["La contraseña anterior no es correcta"]},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": ["Contraseña actualizada correctamente"]}, status=status.HTTP_200_OK)
