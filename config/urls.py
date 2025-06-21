from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('', include('notes.urls')),
        path('account/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('admin/', admin.site.urls),
        path('contact/', include('contact.urls'))
    ]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + debug_toolbar_urls() 



  