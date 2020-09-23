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
	path('profile/<username>/', views.get_user_profile,name='profile'),
	path('dashboard/<int:event_id>/update/', views.event_update, name='event-update'),
	path('events/<int:event_id>/delete/', views.event_delete, name='event-delete'),
	path('events/<int:event_id>/event_book/', views.event_book, name='ticket-book'),

]
