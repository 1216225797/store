from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin.models import Goods,Types,Orders,Users,Order_detail
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
import hashlib
# Create your views here.

def index(request):
    return render(request,'myweb/index.html')
# 登录
def login(request):
    return render(request,'myweb/login.html')

def do_login(request):
    if request.POST['veri'].lower() == request.session['verification']:
        try:
            login_user = Users.objects.get(username=request.POST['username'])
            if login_user.status == 0:
                md5 = hashlib.md5()
                md5.update(bytes(request.POST['password'],encoding='utf-8'))
                if login_user.password == md5.hexdigest():
                    request.session['user'] = {'id':login_user.id,'username':login_user.username,'name':login_user.name,
                                               'mobile':login_user.mobile,'status':login_user.status,'state':login_user.state,'address':login_user.address}
                    return JsonResponse({'msg':'success'})
                else:
                    return JsonResponse({'msg':'error_password'})
            else:
                return JsonResponse({'msg':'no_account'})
        except:
            return JsonResponse({'msg':'no_account'})
    else:
        return JsonResponse({'msg':'eroor_veri'})

# 注册
def register(request):
    return render(request,'myweb/register.html')

def do_register(request):

    if request.POST['password'] != request.POST['repassword']:
        return JsonResponse({'msg':'passwd_error'})
    elif Users.objects.filter(username=request.POST['username']):
        return JsonResponse({'msg':'account_error'})
    else:
        users = Users()
        users.username = request.POST['username']
        md5 = hashlib.md5()
        md5.update(bytes(request.POST['password'],encoding='UTF-8'))
        # 十六进制保存到数据库
        users.password = md5.hexdigest()
        users.name = request.POST['name']
        users.mobile = request.POST['mobile']
        users.address = request.POST['address']
        users.save()
        return JsonResponse({'msg':'success'})

    # except Exception as e:
    #     print(e)
    #     context = {'info':"注册失败！"}
    #     return render(request,'myweb/info.html',context)


def shopcart(request):
    if 'shopcart' not in request.session:
        request.session['shopcart'] = {}
    return render(request,'myweb/shopcart.html')

def list(request):
    type_id = request.GET.get('tid')
    if type_id:
        tid = Types.objects.get(id=type_id)
        goods = Goods.objects.filter(state=0,type_id=tid)
    else:
        goods = Goods.objects.filter(state=0)
    types = Types.objects.filter(status=0)
    context = {"goods":goods,"typelist":types}
    return render(request,'./myweb/list.html',context)

def detail(request,gid):
    goods = Goods.objects.get(id=gid)
    context = {"goods":goods}
    return render(request,'myweb/detail.html',context)


def shopcart(request):
    if 'shoplist' not in request.session:
        request.session['shoplist']={}
    return render(request,'myweb/shopcart.html')

def addshopcart(request,gid):
    goods = Goods.objects.get(id=gid)
    goods_msg = {'id':goods.id,'name':goods.name,'price':goods.price,
                 'describe':goods.describe,'stock':goods.stock,'picture':goods.picture}
    # 购买商品数量
    goods_msg['num'] = int(request.POST.get('m'))

    # 从session中获取购物车信息
    if 'shoplist' in  request.session:
        shoplist = request.session['shoplist']
    else:
        # 创建以商品ID为键，商品信息为值的字典
        shoplist = {}

    # 如果商品ID存在，则只用增加数量
    if gid in shoplist:
        shoplist[gid]['num'] += goods_msg['num']
    else:
        shoplist[gid] = goods_msg


    # 把购物车信息放回session
    request.session['shoplist'] = shoplist

    return render(request,'myweb/shopcart.html')


def del_shopcart(request,sid):
    try:
        sp = request.session['shoplist']
        # 删除元素两种方法,删除键为sid的元素
        # del sp[sid]
        sp.pop(sid)
        request.session['shopcart'] = sp
        return redirect(reverse('myweb_shopcart'))
    except:
        context = {"info":"删除失败！"}
        return render(request,'myweb/info.html',context)

def change_shopcart(request):
    sid = request.GET.get('sid')
    num = request.GET.get('num')
    try:
        sp = request.session['shoplist']
        sp[sid]['num'] = num
        request.session['shoplist'] = sp
        return redirect(reverse('myweb_shopcart'))
    except:
        context = {"info":"系统异常！"}

def clear_shopcart(request):

    del request.session['shoplist']
    return redirect(reverse('myweb_shopcart'))


def myorder(request):
    gids = request.GET.get('gids')
    if not gids :
        context = {"info":"请选择你要购买的商品!"}
        return render(request,'myweb/info.html',context)
    gids_list = gids.split(',')
    total = 0
    sl = request.session['shoplist']
    order_list = {}
    for gid in gids_list:
        total += sl[gid]['price']
        order_list[gid] = sl[gid]
        request.session['order_list'] = order_list
    request.session['total'] = total
    return render(request,'myweb/myorder.html')

def myorder_affirm(request):
    try:
        request.session['user']['name'] = request.POST.get('name')
        request.session['user']['address'] = request.POST.get('address')
        request.session['user']['phone'] = request.POST.get('phone')
        request.session['user']['code'] = request.POST.get('code')
        # 删除结算过的购物车商品信息
        shoplist = request.session['shoplist']
        for goods in request.session['order_list']:
            del shoplist[goods]
        request.session['shoplist'] = shoplist
    except Exception as e:
        print(e)
        context = {"info":"请登录！"}
        return render(request,'myweb/info.html',context)
    return render(request,'myweb/myorderaffirm.html')

def myorder_add(request):
    orders = Orders()
    try:
        user = Users.objects.get(id=request.session['user']['id'])
        orders.uid = user
    except:
        context = {"info":"请重新登录！"}
        return render(request,'myweb/info.html',context)
    # try:
    #     for goods in request.session['order_gids']:
    #         order_goods = Goods.objects.get(id = goods)
    #         orders.goods.add(order_goods)
    # except Exception as e:
    #     print(e)
    #     return render(request,'myweb/info.html',{'info':'订单商品不存在！'})
    orders.linkman = request.POST.get('linkman')
    orders.address = request.POST.get('address')
    orders.code = request.POST.get('code')
    orders.phone = request.POST.get('phone')
    orders.price = request.POST.get('total')
    orders.save()

    order_list = request.session['order_list']
    for og in order_list:
        od = Order_detail()
        od.order_id = orders.id
        od.goods_id = og
        od.goods_num = order_list[og]['num']
        print('order_id:'+str(od.order_id)+'goods_id:'+str(od.goods_id)+'goods_num:'+str(od.goods_num))
        od.save()


    return redirect(reverse('myorder_indent'))

def myorder_indent(request,pid):
    # 注意这里取"不等于"值的写法：~Q()
    from django.db.models import Q
    user = Users.objects.get(id=request.session['user']['id'])
    orders = Orders.objects.filter(~Q(status = '3'),Q(uid=user))

    # 或者下面写法也可以
    # orders = Orders.objects.exclude(status = '3').filter(uid=user)
    for order in orders:
        detail = Order_detail.objects.filter(order_id = order.id)
        # 以后的作用是为了把订单信息表里的商品数量查询出来；
        # 然后封装到商品对象里，再把商品对象添加到列表，封装到订单对象里
        o_goods = []
        for d in detail:
            order_goods = Goods.objects.get(id=d.goods_id)
            order_goods.num = d.goods_num
            o_goods.append(order_goods)
        order.goods = o_goods

        # 分页
        if pid == '':
            pid = 1
        p = Paginator(orders, 4)
        # 返回p对象的页码列表
        p_num = p.page_range
        # 返回第pid页的数据
        orderlist = p.page(pid)

    context = {'orders':orderlist,'p_num':p_num}
    return render(request,'myweb/indent.html',context)

def indent_del(request,oid):
    try:
       order = Orders.objects.get(id=oid)
       order.status = '3'
       order.save()
       return redirect(reverse('myorder_indent'))
    except Exception as e:
        print(e)
        return render(request,'myweb/info.html',{'info':'删除失败！'})


def myorder_reset(request):
    return render(request,'myweb/myorder.html')

def personal(request):
    login_user = Users.objects.get(id=request.session['user']['id'])
    return render(request,'myweb/personal.html',{'users':login_user})

def peredit(request):
    login_user = Users.objects.get(id=request.session['user']['id'])
    context = {"user":login_user}
    return render(request,'myweb/peredit.html',context)

def perupdate(request):
    if request.method == 'POST':
        try:
            login_user = Users.objects.get(id=request.session['user']['id'])
            login_user.username = request.POST.get('username')
            login_user.gender = request.POST.get('gender')
            login_user.address = request.POST.get('address')
            login_user.mobile = request.POST.get('mobile')
            login_user.save()
            context = {'info':'修改成功'}
        except:
            context = {"info": "修改失败"}

        return render(request, 'myweb/info.html', context)


def logout(request):
    del request.session['user']
    return redirect(reverse('myweb_index'))