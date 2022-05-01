from datetime import datetime
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
from django.db.transaction import atomic

from published_events_deploy.apps.events.models import Event, Category
from published_events_deploy.apps.events.serializers import CategorySerializer, EventInfoSerializer, EventCreateSerializer, \
    CreateTicketTypeSerializer, TicketTypeSerializer
from published_events_deploy.apps.multimedia.models import Image
from published_events_deploy.apps.multimedia.serializers import ImageSerializer
from published_events_deploy.apps.utils import get_binary_content
from published_events_deploy.utils.all import get_point_distance


class EventView(ViewSet):
    serializer_class = EventInfoSerializer
    model = Event
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]

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
        #first_data = request.data
        #images:dict = request.data.get("images")
        #tickets:list = request.data.get("tickets")

        print("ENTRADA NUMEROS")

        #if not images.get("mainImage"):
        #    print("ENTRADA DOS")
        #    return Response({
        #        "message": ["La imagen pricipal es requerida"]
        #    }, status=status.HTTP_400_BAD_REQUEST)

        #serialized_data = EventCreateSerializer(data=first_data, context={"request": request})
        #serialized_data.is_valid(raise_exception=True)
        #event:Event = serialized_data.save()

        print("ENTRADA 3")

        #if not event:
        #    return Response({"message": ["No se pudo crear el evento"]}, status=status.HTTP_400_BAD_REQUEST)
        
        ##file = get_binary_content(images.get("mainImage"))

        #if not file:
        #        return Response({"message": ["La imagén no es válida"]}, status=status.HTTP_400_BAD_REQUEST)

        ###main_image = Image()
        ###main_image.image.save(event.slug + "_main.jpg", file, save=False)
        ###main_image.save()

        ###event.image = main_image
        ####event.save()

        #for ticket in tickets:
        #    ticket["event"] = event.id
        #    ticket["availables"] = ticket.get("quantity", 0)
        #    ticket_type = CreateTicketTypeSerializer(data=ticket, context={"request": request})
        #    ticket_type.is_valid(raise_exception=True)
        #    ticket_type.save()

        
        #new_event_serialized = EventInfoSerializer(instance=event, many=False, context={"request": request}).data

        return Response({"message":["Evento creado satisfactoriamente"],"data": "Hello"}, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], url_name="create new event", url_path="new", detail=False)
    def create_event(self, request, *args, **kwargs): 
 

        return Response({"message":["Evento creado satisfactoriamente"],"data": "Hello"}, status=status.HTTP_201_CREATED)


    @action(methods=["POST"], url_name="add-ticket-to-event", url_path="set_main_image", detail=True, )
    def set_main_image(self, request, *args, **kwargs):
        files = self.request.FILES
        pk = kwargs.get("pk")
        try:
            event = Event.objects.get(id=pk)
            if not files.get('image'):
                return Response({"image": ["Este campo es requerido"]}, status=status.HTTP_400_BAD_REQUEST)
            image = files.get('image')
            if image.size > 1024000:
                return Response({"message": ["El tamaño del archivo excede el maximo permitido(1MB)"]},
                                status=status.HTTP_400_BAD_REQUEST)

            if not image.content_type.split("/")[0] == "image":
                return Response({"message": ["Imagen no válida, revisa el formato del archivo"]},
                                status=status.HTTP_400_BAD_REQUEST)

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
            image = files.get('image')
            if image.size > 1024000:
                return Response({"message": ["El tamaño del archivo excede el maximo permitido(1MB)"]},
                                status=status.HTTP_400_BAD_REQUEST)

            if not image.content_type.split("/")[0] == "image":
                return Response({"message": ["Imagen no válida, revisa el formato del archivo"]},
                                status=status.HTTP_400_BAD_REQUEST)

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

    @action(methods=["GET"], url_name="get assistants by event", url_path="assistants", detail=True)
    def get_assistants_by_event(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        event = Event.objects.get_assistants(id=pk)

        if event is None:
            return Response({"message": "Este evento no ha sido encontrado"}, status.HTTP_404_NOT_FOUND)

        return Response({"data": ""}, status=status.HTTP_200_OK)


class ListEvents(ViewSetMixin, ListAPIView):
    serializer_class = EventInfoSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        search = self.request.query_params.get("search", None)
        status = self.request.query_params.get("status", "all") #active #expired #all
        queryset = self.queryset
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(
                created_by__first_name__icontains=search))

        if status == "active":
            queryset = queryset.filter(sell_limit_date__gte=datetime.now()) 
        elif status == "expired":
            queryset = queryset.filter(sell_limit_date__lt=datetime.now())

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by("-sell_limit_date")
        serialized_data = self.get_serializer_class()(instance=queryset, many=True, context={"request": request})
        return Response({"data": serialized_data.data}, status=status.HTTP_200_OK)


class NearEvents(ViewSetMixin, ListAPIView):
    serializer_class = EventInfoSerializer
    queryset = Event.objects.all()

    def get_queryset(self):
        current_latitude = self.request.query_params.get('latitude', 0.0)
        current_longitude = self.request.query_params.get('longitude', 0.0)

        events = Event.objects.all().filter(sell_limit_date__gte=datetime.now()) .order_by("start_date")
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

    # params latitude longitude
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



class CategoriesView(ViewSetMixin, ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.get_serializer_class()(instance=queryset, many=True, context={"request": request})
        return Response({"data": serialized_data.data}, status=status.HTTP_200_OK)