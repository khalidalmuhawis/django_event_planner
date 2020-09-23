from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import UserSignup, UserLogin, EventForm, BookingForm, UserProfile
from .models import Event, Booking
from django.contrib.auth.models import User
import datetime
from django.db.models import Q

def get_user_profile(request, username):
	user = User.objects.get(username=username)
	return render(request, 'user_profile.html', {"user":user})


def home(request):
	context = {
		"events":Event.objects.all()
	}
	return render(request, 'home.html', context)

class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				if Event.objects.filter(organizer=auth_user).exists():
					return redirect('dashboard')
				messages.success(request, "Welcome Back!")
				return redirect('home')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")


class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")


def dashboard(request):
	if not request.user.is_staff:
		return redirect("no-access")
	context = {
		"events":Event.objects.filter(organizer=request.user)
	}
	return render(request, 'dashboard.html', context)


def previous_event(request):
	guests = Booking.objects.filter(guest=request.user)
	context = {
		"guests":guests,
	}
	return render(request, 'previous_events.html', context)


def events(request):
	if not request.user.is_authenticated:
		return redirect("no-access")
	events = Event.objects.filter(datetime__gte=datetime.datetime.now())
	query = request.GET.get('q')
	if query:
		events = events.filter(
			Q(organizer__username__icontains=query)|
			Q(title__icontains=query)|
			Q(description__icontains=query)
			   ).distinct()
	context = {
		"events":events,
	}
	return render(request, 'events.html', context)


def event_create(request):
	form = EventForm()
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('dashboard')
	context = {
	"form": form,
	}
	return render(request, 'event_create.html', context)


def event_detail(request, event_id):
	event = Event.objects.get(id=event_id)
	guests = Booking.objects.filter(event=event)
	context = {
		"event": event,
		"guests":guests,
	}
	return render(request, 'event_detail.html', context)


def no_access(request):
	return render(request, "no_access.html")


def event_update(request, event_id):
	event = Event.objects.get(id=event_id)
	form = EventForm(instance=event)
	if request.method == "POST":
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			return redirect('dashboard')
	context = {
			"event": event,
			"form":form,
			}
	return render(request, 'event_update.html', context)


def event_delete(request,event_id):
	event = Event.objects.get(id=event_id)
	if request.user != event.organizer:
		return redirect('login')
	event.delete()
	return redirect('dashboard')


def event_book(request, event_id):
	if not request.user.is_authenticated:
		return redirect('login')
	event_obj = Event.objects.get(id=event_id)
	form = BookingForm()
	if request.method == "POST":
		form = BookingForm(request.POST)
		if form.is_valid():
			book = form.save(commit=False)
			book.event = event_obj
			book.guest = request.user
			if event_obj.seats == 0:
				messages.success(request, "No More Tickets!")
				return redirect('events')
			event_obj.seats -= book.seats
			if event_obj.seats >= 0:
				seat = event_obj.seats - book.seats
				event_obj.save()
				book.save()
				return redirect('events')
			else:
				return redirect('ticket-book',event_obj.id)
	context = {
	"form": form,
	"event": event_obj
	}
	return render(request, 'ticket_book.html', context)
