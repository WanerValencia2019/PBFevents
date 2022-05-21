from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotFound

from published_events_deploy.apps.events.models import Assistant, Category, TicketType, Event
from published_events_deploy.apps.users.serializers import UserSerializer, PublicUserSerializer

from published_events_deploy.apps.multimedia.serializers import ImageSerializer

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        exclude = ["created_at", "updated_at"]
class EventInfoSerializer(serializers.ModelSerializer):
    created_by = PublicUserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    image = ImageSerializer(many=False, read_only=True)
    other_images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["id", "created_at", "created_by", "title", "description", "address", "image","other_images", "slug",
                  "space_available",
                  "sell_limit_date",
                  "start_date",
                  "end_date", "latitude", "longitude", "categories"]



class ShortEventInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "description", "address", "sell_limit_date","start_date","end_date",]
class ShortTicketTypeSerializer(serializers.ModelSerializer):
    event = ShortEventInfoSerializer(read_only=True)
    class Meta:
        model = TicketType
        exclude = ["created_at", "updated_at", "ticket_sales","availables"]

class EventCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150, required=True)
    description = serializers.CharField(required=True)
    space_available = serializers.IntegerField(required=True)
    address = serializers.CharField(required=True, max_length=150)
    longitude = serializers.CharField(max_length=100, required=True)
    latitude = serializers.CharField(max_length=100, required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    sell_limit_date = serializers.DateTimeField(required=True)
    categories = serializers.ListField(required=True)

    def create(self, validated_data):
        user = self.context.get("request").user
        categories = validated_data.get("categories")
        new_event = Event(
            created_by=user,
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            space_available=validated_data.get("space_available"),
            start_date=validated_data.get("start_date"),
            end_date=validated_data.get("end_date"),
            address=validated_data.get("address"),
            longitude=validated_data.get("longitude"),
            latitude=validated_data.get("latitude"),
            sell_limit_date=validated_data.get("sell_limit_date"),
        )
        new_event.save()

        for category in categories:
            new_event.categories.add(Category.objects.get(id=category))

        new_event.save()

        return new_event

    def validate(self, data):
        categories = data.get("categories")

        for category in categories:
            try:
                founded_category = Category.objects.get(id=category)
            except ObjectDoesNotExist as e:
                raise ValidationError({"categories": "La categoría no es válida"})
        return data


class CreateTicketTypeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120, required=True)
    description = serializers.CharField(max_length=150, required=True)
    unit_price = serializers.FloatField(required=True)
    availables = serializers.IntegerField(required=True)
    event = serializers.CharField(max_length=36)

    def create(self, validated_data):
        event_id = validated_data.get("event")
        event = Event.objects.get(id=event_id)
        ticket_type = TicketType(
            name=validated_data.get("name"),
            description=validated_data.get("description"),
            unit_price=validated_data.get("unit_price"),
            availables=validated_data.get("availables"),
            event=event
        )
        ticket_type.save()

        return ticket_type

    def validate(self, data):
        user = self.context.get("request").user
        event_id = data.get("event")
        availables = data.get("availables")
        event = None
        try:
            event = Event.objects.get(created_by=user, id=event_id)
        except ObjectDoesNotExist as e:
            raise ValidationError({"message": "El evento no es válido"})

        if availables > event.space_available:
            raise ValidationError(
                {"message": "La cantidad de entradas supera los tickets disponibles en el evento ({} > {})".format(
                    availables, event.space_available)})
        return data


class AssistantSerializer(serializers.ModelSerializer):
    ticket = ShortTicketTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Assistant
        fields = ['id', "full_name","email", "phone","identification","ticket","ticket_quantity","security_code"]

