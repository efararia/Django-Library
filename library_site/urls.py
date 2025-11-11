from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("books.urls")),
    path("accounts/", include("accounts.urls")),
    path("", RedirectView.as_view(pattern_name="books:list", permanent=False)),
    path('admin_panel/', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),
    path('orders/', include('orders.urls')),
]