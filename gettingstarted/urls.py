from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import covid19.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", covid19.views.index, name="index"),
    path("home", covid19.views.index, name="index"),
    path("Maps/", covid19.views.defaultMap, name=""),
    path("Maps/<dataPointName>", covid19.views.heatMap, name="chorplethmap"),
    path("Dashboard1/", covid19.views.dashboard1, name="Dashboard1"),  
    path("Dashboard2/", covid19.views.dashboard2, name="Dashboard2"), 
    path("Dashboard3/", covid19.views.dashboard3, name="Dashboard3"), 
    path("Dashboard4/", covid19.views.dashboard4, name="Dashboard4"),       
    path("BarGraphs/", covid19.views.grades, name="bargraph"),    
    path("admin/", admin.site.urls),
]
