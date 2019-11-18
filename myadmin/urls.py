from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'my_store.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    # 用户管理
    url(r'^$', views.index, name="myadmin_index"),
    url(r'^login$', views.login, name="myadmin_login"),
    url(r'^do_login$', views.do_login, name="myadmin_dologin"),
    url(r'^useradd$', views.useradd, name="useradd"),
    url(r'^do_useradd', views.do_useradd, name="douseradd"),
    url(r'^userdel/(?P<uid>[0-9]+)$', views.userdel, name='userdel'),
    url(r'^useredit/(?P<uid>[0-9]+)$', views.useredit, name='useredit'),
    url(r'^do_useredit/(?P<uid>[0-9]+)$', views.do_useredit, name='douseredit'),
    url(r'^userlist$', views.userindex, name='userlist'),
    url(r'^userlist(?P<pindex>[0-9]*)$', views.userindex, name='userindex'),
    url(r'^logout$', views.logout, name='myadmin_logout'),
    url(r'^verify$',views.verify,name='myadmin_verify'),


    # 商品类别管理
    url(r'^typeindex(?P<pindex>[0-9]*){0,1}$',views.typeindex,name='myadmin_typeindex'),
    url(r'^typeadd/(?P<tid>[0-9]+){0,1}$',views.typeadd,name='myadmin_typeadd'),
    url(r'^do_typeadd$',views.do_typeadd,name='myadmin_dotypeadd'),
    url(r'^typeedit/(?P<tid>[0-9]+)$',views.typeedit,name='myadmin_typeedit'),
    url(r'^do_typeedit/(?P<tid>[0-9]+)$',views.do_typeedit,name='myadmin_dotypeedit'),
    # url(r'^typedel/(?P<tid>[0-9]+)$',views.typedel,name='myadmin_typedel'),
    url(r'^do_typedel/(?P<tid>[0-9]+)$',views.do_typedel,name='myadmin_dotypedel'),
    url(r'^type_select$',views.type_select,name='myadmin_type_select'),


    # 商品信息管理
    url(r'^goods-index(?P<gindex>[0-9]*){0,1}$',views.goods_index,name="myadmin_goods_index"),
    url(r'^goods-add$',views.goods_add,name="myadmin_goods_add"),
    url(r'^goods-doadd$',views.goods_doadd,name='myadmin_goods_doadd'),
    url(r'^goods-edit/(?P<gid>[0-9]+)$',views.goods_edit,name="myadmin_goods_edit"),
    url(r'^goods-doedit/(?P<gid>[0-9]+)$',views.goods_doedit,name="myadmin_goods_doedit"),
    url(r'^goods-del/(?P<gid>[0-9]+)$',views.goods_del,name="myadmin_goods_del"),


    # 订单管理
    url(r'^order-index(?P<oindex>[0-9]*){0,1}$',views.order_index,name='myadmin_order_index'),
    url(r'^order-edit(?P<oid>[0-9]+)$',views.order_edit,name='myadmin_order_edit'),
    url(r'^order-doedit(?P<oid>[0-9]+)$',views.order_doedit,name='myadmin_order_doedit'),
]
