"""basimilch URL Configuration

The `urlpatterns` list routes URLs to views.
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("juntagrico_custom_sub.urls")),
    path("", include("juntagrico.urls")),
    path("impersonate/", include("impersonate.urls")),
    path("", include("juntagrico_list_gen.urls")),
    path("", include("juntagrico_depot_management.urls")),
    path("", include("juntagrico_assignment_export.urls")),
    path("", include("juntagrico_polling.urls")),
]
