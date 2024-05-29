from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('sell/<int:spare_part_id>/', views.sell_spare_part, name='sell_spare_part'),  # Include spare part ID in URL
    path('purchase/<int:spare_part_id>/', views.purchase_spare_part, name='purchase_spare_part'),  # Include spare part ID in URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
