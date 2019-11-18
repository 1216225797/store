from django.conf.urls import include, url
from django.contrib import admin
# 导入静态包
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'my_store.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^myweb/', include('myweb.urls')),
    url(r'^myadmin/', include('myadmin.urls')),
    url(r'^', include('myweb.urls')),
]
