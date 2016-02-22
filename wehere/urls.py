from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [

    # url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^freedrink/', include('freedrink.urls')),
    url(r'^core/', include('core.urls')),
    # url(r'^', view.start),

]