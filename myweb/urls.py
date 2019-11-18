from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'my_store.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # ================================用户管理=========================
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index,name='myweb_index'),
    url(r'^index/$',views.index, name='myweb_index'),
    url(r'^login/$', views.login, name='myweb_login'),
    url(r'^do-login/$',views.do_login,name='myweb_dologin'),
    url(r'^shopcart/$',views.shopcart,name='myweb_shopcart'),
    url(r'^list/$',views.list,name='myweb_list'),
    url(r'^register$', views.register, name='myweb_register'),
    url(r'^do-register$',views.do_register,name='myweb_doregister'),
    url(r'^personal$',views.personal,name='myweb_personal'),
    url(r'^peredit$',views.peredit,name='myweb_peredit'),
    url(r'^perupdate$',views.perupdate,name='myweb_perupdate'),
    url(r'^logout$',views.logout,name='myweb_logout'),
    url(r'^goods-detail/(?P<gid>[0-9]+)$',views.detail,name='myweb_detail'),
    # ====================购物车==============================================
    url(r'^shopcart$',views.shopcart,name='myweb_shopcart'),
    url(r'^addshopcart/(?P<gid>[0-9]+)$',views.addshopcart,name='myweb_addshopcart'),
    url(r'^del-shopcart/(?P<sid>[0-9]+)$',views.del_shopcart,name='myweb_delshopcart'),
    url(r'^change-shopcart/$',views.change_shopcart,name='myweb_changeshopcart'),
    url(r'^clear-shopcart/$',views.clear_shopcart,name='myweb_clearshopcart'),
    # ========================订单==============================================
    url(r'^myorder/$',views.myorder,name='myorder'),
    url(r'^myorder-affirm/$',views.myorder_affirm,name='myorder_affirm'),
    url(r'^myorder-add$',views.myorder_add,name='myorder_add'),
    url(r'^myorder-indent(?P<pid>[0-9]*){0,1}$',views.myorder_indent,name='myorder_indent'),
    url(r'^myorder-reset$',views.myorder_reset,name='myorder_reset'),
    url(r'^indent-del/(?P<oid>[0-9]+)$',views.indent_del,name='indent_del'),
]
