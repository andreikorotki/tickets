from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


from . import views

urlpatterns = [path('menu', views.menu),
               path('', views.menu),
               path('get_ticket/change_oil', views.change_oil),
               path('get_ticket/inflate_tires', views.inflate_tires),
               path('get_ticket/diagnostic', views.diagnostic),
               path('processing', views.processing),
               path('next', views.next_ticket),
               path('processing/', RedirectView.as_view(url='/processing'))
              ]

urlpatterns += static(settings.STATIC_URL)
