from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("order/",include("apps.order.urls")),
    path("machine/",include("apps.machine.urls")),
    path("process/",include("apps.process.urls")),
    path("sample/",include("apps.sample.urls")),
    path("analysis/",include("apps.analysis.urls")),
    path("market/",include("apps.market.urls")),
    path("user/", include("apps.user.urls")),

]
