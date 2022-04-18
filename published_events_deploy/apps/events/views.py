from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet, ViewSetMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from django.db.models import Q

from published_events_deploy.apps.events.models import Event, Category
from published_events_deploy.apps.events.serializers import EventInfoSerializer, EventCreateSerializer, \
    CreateTicketTypeSerializer, TicketTypeSerializer
from published_events_deploy.apps.multimedia.models import Image
from published_events_deploy.apps.multimedia.serializers import ImageSerializer
from published_events_deploy.utils.all import get_point_distance


class EventView(ViewSet):
    serializer_class = EventInfoSerializer
    model = Event
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        data = self.model.objects.filter(created_by=user)
        return data

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        events = EventInfoSerializer(instance=data, many=True, context={"request": request})

        return Response({
            "data": events.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serialized_data = EventCreateSerializer(data=data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        event = serialized_data.save()

        if not event:
            return Response({"message": ["No se pudo crear el evento"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": self.serializer_class(instance=event).data}, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], url_name="add-ticket-to-event", url_path="set_main_image", detail=True, )
    def set_main_image(self, request, *args, **kwargs):
        files = self.request.FILES
        pk = kwargs.get("pk")
        try:
            event = Event.objects.get(id=pk)
            if not files.get('image'):
                return Response({"image": ["Este campo es requerido"]}, status=status.HTTP_400_BAD_REQUEST)

            image_serialized = ImageSerializer(data=files)
            image_serialized.is_valid(raise_exception=True)
            new_image = image_serialized.save()

            previous_image = None
            if event.image:
                previous_image = event.image.id

            event.image = new_image
            event.save()

            Image.objects.filter(id=previous_image).delete()

            return Response({"message": "Imagen agregada correctamente"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"message": "Este evento no está disponible"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], url_name="add-ticket-to-event", url_path="add_other_image", detail=True, )
    def add_other_image(self, request, *args, **kwargs):
        files = self.request.FILES
        pk = kwargs.get("pk")
        try:
            event = Event.objects.get(id=pk)
            if not files.get('image'):
                return Response({"image": ["Este campo es requerido"]}, status=status.HTTP_400_BAD_REQUEST)

            image_serialized = ImageSerializer(data=files)
            image_serialized.is_valid(raise_exception=True)
            new_image = image_serialized.save()

            event.other_images.add(new_image)
            event.save()

            return Response({"message": "Imagen agregada correctamente"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"message": "Este evento no está disponible"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["POST"], url_name="add-ticket-to-event", url_path="add_ticket", detail=False, )
    def add_ticket_type(self, request, *args, **kwargs):
        data = request.data
        serialized_data = CreateTicketTypeSerializer(data=data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)

        ticket_type = serialized_data.save()

        if not ticket_type:
            return Response({"message": ["No se pudo agregar tipo de entrada a el evento"]},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": data}, status=status.HTTP_200_OK)




class ListEvents(ViewSetMixin, ListAPIView):
    serializer_class = EventInfoSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        search = self.request.query_params.get("search", None)
        if search:   
            queryset = self.queryset.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(created_by__first_name__icontains=search))
            return queryset
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.get_serializer_class()(instance=queryset, many=True, context={"request": request})
        return Response({"data": serialized_data.data}, status=status.HTTP_200_OK)


class NearEvents(ViewSetMixin, ListAPIView):
    serializer_class = EventInfoSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        current_latitude = self.request.query_params.get('latitude', 0.0)
        current_longitude = self.request.query_params.get('longitude', 0.0)

        print(current_latitude, current_longitude)
        
        events = Event.objects.all()
        near_events = []
        minimun_distance = 50
        for event in events:
            distance = get_point_distance(current_latitude, current_longitude, event.latitude, event.longitude)
            print("==========================")
            print("distance", distance)
            print("==========================")
            if distance <= minimun_distance:
                near_events.append(event)
        return near_events
        
    #params latitude longitude
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.get_serializer_class()(instance=queryset, many=True, context={"request": request})
        return Response({"data": serialized_data.data}, status=status.HTTP_200_OK)

    

class DetailEvent(ViewSetMixin, RetrieveAPIView):
    serializer_class = EventInfoSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        try: 
            event = Event.objects.get(id=pk)
            return event
        except ObjectDoesNotExist as e:
            return None

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print("Hello")
        serialized_data = self.get_serializer_class()(instance=queryset, context={"request": request})
        return Response({"data": serialized_data.data}, status=status.HTTP_200_OK)