from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView,RetrieveUpdateAPIView
from events.models import Event, Booking
from .serializers import SignUpSerializer, RegisterSerializer, EventSerializer, AddEventSerializer, OrganizerSerializer, BookingSerializer, EventUpdateSerializer, EventGuestSerializer, GuestSerializer
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .permissions import IsOwner


class SignUp(CreateAPIView):
	serializer_class = RegisterSerializer


class Events(ListAPIView):
    queryset = Event.objects.filter(datetime__gte=datetime.today()).order_by('-datetime')
    serializer_class = EventSerializer


class CreateEventView(CreateAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = AddEventSerializer
	def perform_create(self, serializer):
		serializer.save(organizer=self.request.user)


class GuestEvent(ListAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		query = Booking.objects.filter(guest=self.request.user)
		return query


class BookingView(CreateAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated,]
	def perform_create(self,serializer):
		serializer.save(guest=self.request.user, event_id=self.kwargs['event_id'])


class UpdateEventView(RetrieveUpdateAPIView):
	queryset =  Event.objects.all()
	serializer_class = EventUpdateSerializer
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'


class OrganizerView(ListAPIView):
	serializer_class = OrganizerSerializer
	queryset = Event.objects.all()


class GuestView(RetrieveAPIView):
	serializer_class = EventGuestSerializer
	permission_classes = [IsAuthenticated, IsOwner]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	queryset = Event.objects.all()
