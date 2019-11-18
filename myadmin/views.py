from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,JsonResponse
from myadmin.models import Users,Types,Goods,Orders
from django.core.paginator import Paginator
from my_store import settings
import random
from PIL import Image, ImageDraw, ImageFont
import os
import time
import json
# 获取密码并md5加密
import hashlib

# Create your views here.

# 用户管理------------------------------------------------------------------------------

# 分页显示
def userindex(request,pindex=1):
    if pindex == '':
        pindex == '1'
    list = Users.objects.all()
    # 按照每页4条数据分页
    p = Paginator(list,4)
    pindex = int(pindex)
    # 返回分页后的页码列表
    p_num = p.page_range
    # 返回第pindex页的page类实例对象
    page = p.page(pindex)
    context = {"p_num":p_num, "userlist":page}
    return render(request,'myadmin/users/index.html',context)


def index(request):
    try:
        if request.session["adminuser"]:
            return render(request,'myadmin/index.html')

    except:
        # context = {'info': '请登录'}
        # return render(request, 'myadmin/info.html', context)
        return redirect(reverse('myadmin_login'))

def login(request):
    return render(request,'myadmin/login.html')

# 登录
def do_login(request):
    verify_code = request.POST['code']
    if verify_code.lower() == request.session["verification"]:
        try:
            login_user =  Users.objects.get(username=request.POST["username"])
            md5 = hashlib.md5()
            md5.update(bytes(request.POST['password'],encoding="utf-8"))
            if login_user.password == md5.hexdigest():
                if login_user.state == 1:
                    request.session["adminuser"] = {"id":login_user.id,"name":login_user.name}
                    return JsonResponse({'msg':'success'})
                else:
                    return JsonResponse({'msg':'no_admin'})
            else:
                return JsonResponse({'msg':'failed_passwd'})
        except Exception as e:
            print(e)
            return JsonResponse({'msg':'no_account'})
    else:
        return JsonResponse({'msg':'failed_code'})


def useradd(request):
    return render(request,'myadmin/users/add.html')

# 添加用户
def do_useradd(request):
    # 添加try的原因：
    # 防止发生内部错误：例如外键冲突，字段唯一性等
    try:
        us = Users()
        us.username = request.POST['username']
        # 实例化md5实例
        md5 = hashlib.md5()
        # python3中md5只能加密字节型数据，所以要用bytes强制转换
        md5.update(bytes(request.POST['password'],encoding="utf-8"))
        us.password = md5.hexdigest()
        us.name = request.POST['name']
        us.gender = request.POST['sex']
        us.mobile = request.POST['mobile']
        us.address = request.POST['address']
        us.state = 0
        us.status = 0
        us.save()
        context = {"info":"添加成功"}
    except:
        context = {"info": "添加失败"}
    return render(request, "myadmin/info.html", context)

# 用户删除(逻辑删除)
def userdel(request,uid):
    try:
        user_info = Users.objects.get(id=uid)
        user_info.status = 1
        user_info.save()
        context = {"info":"删除成功"}

    except:
        context = {"info":"删除失败"}
    return render(request,"myadmin/info.html",context)


def useredit(request,uid):
    try:
        ud = Users.objects.get(id=uid)
        context = {"user":ud}
        return render(request,'myadmin/users/edit.html',context)
    except:
        context = {"info":"修改信息发生异常！"}
        return render(request,"myadmin/info.html")

# 修改用户信息
def do_useredit(request,uid):
    try:
       ud = Users.objects.get(id=uid)
       ud.name = request.POST["name"]
       ud.gender = request.POST["gender"]
       ud.mobile = request.POST["mobile"]
       ud.address = request.POST["address"]
       ud.state = request.POST["state"]
       ud.status = request.POST["status"]
       ud.save()
       context = {"info":"修改成功"}
    except Exception as e:
        context = {"info":"修改失败"}
    return render(request,"myadmin/info.html",context)

# 会员信息展示页面(此函数可以忽略，直接使用上面分页函数)
def userlist(request):
    ul = Users.objects.all()
    context = {"userlist":ul}
    return render(request,'myadmin/users/index.html', context)

def logout(request):
    try:
        del request.session['adminuser']
        return redirect(reverse('myadmin_login'))
    except:
        context = {'info':'请登录'}
        return render(request,'myadmin/info.html',context)

def verify(request):
    # 设置背景颜色
    # 第一个参数表示三原色，第二参数图片宽高，第三个参数表示三原色的值
    width = 100
    height = 25
    bg = Image.new('RGB',(width,height),(150,154,194))
    # 设置噪点
    draw = ImageDraw.Draw(bg)
    for i in range(0,100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        color = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        draw.point=(xy,color)
    # 设置随机选取的字符串
    str1 = 'ABC987DEFGHIJK654LMNOPQRST321UVWXYZ0'
    rand_str = ''
    for j in range(4):
        rand_str += str1[random.randrange(0,len(str1))]
    # 设置字体
    font = ImageFont.truetype('static/myadmin/font/STXIHEI.TTF', 21)
    # 构造字体颜色
    for i in range(0, 4):
        # 构造字体颜色
        fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        # 绘制4个字
        draw.text((5 + i * 24, -4), rand_str[i], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 将生成的验证码存入到session中
    request.session['verification'] = rand_str.lower()

    # 将背景颜色放到内存中
    import io
    f = io.BytesIO()
    bg.save(f,'png')
    return HttpResponse(f.getvalue(),'image/png')
# --------------------------------------------------------------------------------------------


# 商品类型管理--------------------------------------------------------------------------------
def typeindex(request,pindex):
    if not pindex:
        pindex = '1'

    pindex = int(pindex)
    # extra()：添加复杂的where子句，至少要有一个参数，例如select,where或tables等
    # select: 可以在从句中添加其他字段信息，必须是一个字典
    # where：必须是一个字符串列表
    # 拼接：\\
    typelist = Types.objects.extra(select={"p_name_id":"path || id"},where=["status=0"]).order_by("p_name_id")
    # typelist = Types.objects.order_by("path")
    # 为每一个实例添加一个pname属性，主要是为了使层级关系看上去比较直观
    for ob in typelist:
        ob.pname = '...'*(ob.path.count(',')-1)
    p = Paginator(typelist,6)
    # 返回分页之后的页码列表
    p_num = p.page_range
    # 返回第pindex页的实例
    types = p.page(pindex)

    context = {"p_num":p_num,"types":types,}
    return render(request,'myadmin/type/index.html',context)


def typeadd(request,tid):
    if not tid:
        context = {"pid":0,"path":"0,","name":"根类别"}
    else:
        try:
            t = Types.objects.get(id=tid)
            context = {"pid":t.id,"path":t.path+str(tid)+",","name":t.name}
        except:
            context={"info":"父节点ID未找到"}
            return render(request,"myadmin/info.html",context)

    return render(request,"myadmin/type/add.html",context)



def do_typeadd(request):
    try:
        type = Types()
        type.name = request.POST['name']
        type.pid = request.POST['pid']
        type.path = request.POST['path']
        type.save()
        context = {"info":"添加成功"}
    except:
        context = {"info":"内部异常"}

    return render(request,'myadmin/info.html', context)


def typeedit(request,tid):
    try:
        t = Types.objects.get(id=tid)
        context = {"type":t}
        return render(request, 'myadmin/type/edit.html', context)
    except:
        context = {"info":"系统异常"}
        return render(request,'myadmin/info.html',context)


def do_typeedit(request,tid):
    try:
        t = Types.objects.get(id=tid)
        t.name = request.POST['name']
        t.save()
        context = {"info":"修改成功"}
    except:
        context = {"info","修改失败"}
    return render(request,'myadmin/info.html',context)



def do_typedel(request,tid):
    t = Types.objects.get(id=tid)
    t.status = 1
    t.save()

    context = {"info":"删除成功"}
    return render(request,'myadmin/info.html',context)


def type_select(request):
    try:
        tv = int(request.POST.get('tv'))
        t = Types.objects.filter(pid=tv,status=0)
        t_name = []
        t_id = []
        for i in t:
            t_name.append(i.name)
            t_id.append(i.id)
    except:
        context = {"info":"类型不存在！"}
        return render(request,"myadmin/info.html",context)

    return JsonResponse({"type_name":t_name,"type_id":t_id})
# --------------------------------------------------------------------------------------------


# 商品信息管理---------------------------------------------------------------------------------
def goods_index(request,gindex):
    if  gindex == '':
        gindex = '1'

    goods = Goods.objects.all()
    for t in goods:
        type_obj = t.type_id
        t.type_name = type_obj.name

    p = Paginator(goods,4)
    # 返回分页之后的页码列表
    p_num = p.page_range
    # 返回第gindex页的实例
    goods_list = p.page(int(gindex))
    context = {"p_num":p_num,"goods_list":goods_list}
    return render(request,'myadmin/goods/index.html',context)


def goods_add(request):
    t =Types.objects.filter(status=0)
    context = {"typelist":t}
    return render(request,'myadmin/goods/add.html',context)

# 获取商品添加时的类型ID
get_type = lambda  type_id:Types.objects.filter(id=type_id)

def goods_doadd(request):
    try:
        goods = Goods()
        select_1 = request.POST.get('select_1')
        select_2 = request.POST.get('select_2')
        select_3 = request.POST.get('select_3')

        if select_3:
            type_3 = int(select_3)
            t3 = get_type(type_3)[0]
            goods.type_id = t3
        elif select_2 and select_3 == "":
            type_2 = int(select_2)
            t2 = get_type(type_2)[0]
            goods.type_id = t2
        else:
            type_1 = int(select_1)
            t1 = get_type(type_1)[0]
            goods.type_id = t1
        goods.name = request.POST.get('goods')
        goods.company = request.POST.get("company")
        goods.price = request.POST.get("price")
        goods.stock = request.POST.get("store")
        goods.describe = request.POST.get("descr")
        # 这里注意使用的是request.FILES
        pic = request.FILES.get("pic")
        if pic:
            suffix = pic.name.split('.')[-1:]
            for sf in suffix:
                if sf.lower() in ['jpg','png']:
                    # 格式化文件
                    filename = str(time.strftime("%Y%m%d%H%M%S",time.localtime())) + "." + sf
                    goods.picture = filename
                    upload_path = settings.STATICFILES_DIRS[0] + os.path.sep + "goods" + os.path.sep + filename
                    # 以二进制的方式把图片从内存写入到服务器
                    with open(upload_path, 'wb+') as f:
                        # pic.chunks()循环读取图片内容，每次只从本地磁盘读取一部分图片内容，加载到内存中，并将这一部分内容写入到目录下，写完以后，内存清空；下一次再从本地磁盘读取一部分数据放入内存。就是为了节省内存空间。
                        for file in pic.chunks():
                            f.write(file)
                else:
                    context = {"info":"图片格式有误！"}
                    return render(request, 'myadmin/info.html', context)

        goods.save()
        context = {"info":"添加成功！"}

    except Exception as e:
        context = {"info": "添加失败！"}
    return render(request, 'myadmin/info.html', context)


def goods_edit(request,gid):
    goods = Goods.objects.get(id=gid)
    t = Types.objects.filter(status=0)
    # 因为外键的缘故，goods.type_id取出来的是一个对象
    goods.typeid = goods.type_id.id
    t_path = goods.type_id.path
    path_len = t_path.count(',')
    if path_len == 1:
        goods.typeid_3 = ''
        goods.typeid_2 = ''
        goods.typeid_1 = goods.typeid
    elif path_len == 2:
        goods.typeid_3 = ''
        goods.typeid_2 = goods.typeid
        goods.typename_2 = goods.type_id.name
        goods.typeid_1 = get_type(goods.typeid_2)[0].pid
    elif path_len == 3:
        goods.typeid_3 = goods.typeid
        goods.typename_3 = goods.type_id.name
        goods.typeid_2 = get_type(goods.typeid_3)[0].pid
        goods.typename_2 = get_type(goods.typeid_2)[0].name
        goods.typeid_1 = get_type(goods.typeid_2)[0].pid
    context = {"goods":goods,"typelist":t}
    return render(request, 'myadmin/goods/edit.html', context)


def goods_doedit(request,gid):
    goods = Goods.objects.get(id=gid)
    select_1 = request.POST.get('select_1')
    select_2 = request.POST.get('select_2')
    select_3 = request.POST.get('select_3')

    if select_3:
        type_3 = int(select_3)
        t3 = get_type(type_3)[0]
        goods.type_id = t3
    elif select_2 and select_3 == "":
        type_2 = int(select_2)
        t2 = get_type(type_2)[0]
        goods.type_id = t2
    else:
        type_1 = int(select_1)
        t1 = get_type(type_1)[0]
        goods.type_id = t1
    goods.name = request.POST['goods']
    goods.price = request.POST['price']
    goods.describe = request.POST['descr']
    goods.state = request.POST['state']
    goods.stock = request.POST['store']
    picture = request.FILES.get('pic')
    sf = picture.name.split('.')[-1]
    goods.picture = str(time.strftime('%Y%m%d%H%M%S',time.localtime())+'.'+ sf)
    upload_path = settings.STATICFILES_DIRS[0] + os.path.sep +'goods' + os.path.sep + goods.picture
    with open(upload_path,'wb+') as f:
        for file in picture.chunks():
            f.write(file)
    goods.company = request.POST['company']
    goods.save()
    context = {"info":"修改成功"}
    return render(request,'myadmin/info.html',context)

def goods_del(request,gid):
    try:
        goods = Goods.objects.get(id=gid)
        goods.state = 2
        goods.save()

        context = {"info":"删除成功！"}
    except Exception as e:
        context = {"info":"删除失败！"}

    return render(request,'myadmin/info.html',context)



# 订单管理=================================================================
def order_index(request,oindex):
    if oindex == '':
        oindex = 1

    order = Orders.objects.all()

    p = Paginator(order,4)
    p_num = p.page_range
    order_list = p.page(oindex)
    context = {'page_num':p_num,"orderslist": order_list}

    return render(request,'myadmin/orders/index.html',context)

def order_edit(request,oid):
    try:
        orders = Orders.objects.get(id=oid)
        context = {"orders":orders}

        return render(request,'myadmin/orders/edit.html',context)
    except:
        context = {'info':'修改失败'}
        return render(request,'myadmin/info.html',context)

def order_doedit(request,oid):
    try:
        orders = Orders.objects.get(id=oid)
        orders.status = request.POST.get('status')
        orders.save()
        context = {"info":"修改成功"}
    except Exception as e:
        print(e)
        context = {"info":"修改失败"}

    return render(request,'myadmin/info.html',context)






