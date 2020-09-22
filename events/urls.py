from django.urls import path
from events import views
from .views import Login, Logout, Signup, home, dashboard
urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('dashboard/',views.dashboard ,name='dashboard'),
	path('events/',views.events ,name='events'),
	path('dashboard/create', views.event_create, name='event-create'),
	path('events/<int:event_id>/', views.event_detail, name='event-detail'),
	path('no-access/', views.no_access, name='no-access'),
	path('dashboard/<int:event_id>/update/', views.event_update, name='event-update'),

]
