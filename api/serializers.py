from rest_framework import serializers
from events.models import Event, Booking
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		new = User(username=username, first_name=first_name, last_name=last_name)
		new.set_password(password)
		new.save()
		return validated_data


class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'


class AddEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'date', 'time','location','description']


class BookingSerializer(serializers.ModelSerializer):
	event = serializers.SerializerMethodField()

	class Meta:
		model= Booking
		exclude=['guest']

	def get_event(self, obj):
		return (obj.event.title)


class EventUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ['title', 'description','location','datetime']


class OrganizerSerializer(serializers.ModelSerializer):
	organizer= serializers.SerializerMethodField()
	class Meta:
		model= Event
		fields=['organizer','title', 'description', 'location', 'datetime', 'seats',]


class EventGuestSerializer(serializers.ModelSerializer):
		guests = serializers.SerializerMethodField()
		class Meta:
			model=Event
			fields=['title', 'datetime', 'guests',]

		def get_guests(self,obj):
			event = obj.guestevent.all()
			return GuestSerializer(event, many=True).data


class GuestSerializer(serializers.ModelSerializer):
	guest = serializers.SerializerMethodField()

	class Meta:
		model= Booking
		fields=['guest']

	def get_guest(self, obj):
		return (obj.guest.first_name + "," + obj.guest.last_name)
