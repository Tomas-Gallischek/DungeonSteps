from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('welcomeapp.urls')),
    path('admin/', admin.site.urls),
    path('hracapp/', include('hracapp.urls')),
    path('itemsapp/', include('itemsapp.urls')),
    path('shopapp/', include('shopapp.urls')),
    path('pvmapp/', include('pvmapp.urls')),

]

# Toto se používá POUZE ve vývojovém prostředí (DEBUG=True)!
# Umožňuje Django servírovat soubory z MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)