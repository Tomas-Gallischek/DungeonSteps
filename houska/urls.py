from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('welcomeapp.urls')),
    path('admin/', admin.site.urls),
    path('hracapp/', include('hracapp.urls')),
    path('itemsapp/', include('itemsapp.urls')),
    path('shopapp/', include('shopapp.urls')),
    path('pvmapp/', include('pvmapp.urls')),

]
