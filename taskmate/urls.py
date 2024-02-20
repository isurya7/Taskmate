from django.contrib import admin
from django.urls import path, include
from todolist import views as todolist_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', todolist_views.home, name='home'),
    path('todolist/', include('todolist.urls'), name='todolist'),
    path('account/', include('user_app.urls'), name='account'),
    path('about', todolist_views.about, name='about'),  # Add a trailing slash for consistency
    path('contact', todolist_views.contact, name='contact'),  # Add a trailing slash for consistency
    # Other paths as needed for your project
]
