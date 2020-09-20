from django.urls import path
from events import views
from .views import Login, Logout, Signup, home, dashboard
urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('dashboard/',views.dashboard ,name='dashboard'),
]
