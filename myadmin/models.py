from django.db import models

# Create your models here.
# 用户表
class Users(models.Model):
    username = models.CharField(max_length=16,unique=True)
    name = models.CharField(max_length=8)
    password = models.CharField(max_length=32)
    gender = models.IntegerField(default=0)
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    # 账号类别，区分管理员和普通会员
    # 0：普通会员；1：管理员 2：禁用
    state = models.IntegerField(default=0)
    # 账号状态 0：启用 1：删除
    status = models.IntegerField(default=0)
    # auto_now：每次保存字段时，自动设置该字段的值为当前时间，不允许修改
    # auto_now_add：当对象第一次被创建时设置为当前时间，可以修改
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "user_info" # 更改表名
        ordering = ['-create_date'] # 按创建时间倒序排序


# 商品类型表
class Types(models.Model):
    name = models.CharField(max_length=50)
    # 父类别ID
    pid = models.IntegerField(default=0)
    path = models.CharField(max_length=255)
    # 0：正常 1：删除
    status = models.IntegerField(default=0)

    class Meta:
        db_table = "type"


# 商品明细表
class Goods(models.Model):
    type_id = models.ForeignKey(Types)
    name = models.CharField(max_length=50)
    price = models.FloatField()# 小数点后保留两位
    describe = models.TextField(null=True,blank=True)
    # 0：在售 1：下架 2：删除
    state = models.IntegerField(default=0)
    # 库存
    stock = models.IntegerField(default=0)
    picture = models.CharField(max_length=255,null=True,blank=True)
    company = models.CharField(max_length=255,null=True,blank=True)
    add_date = models.DateField(auto_created=True,auto_now_add=True)

    class Meta:
        db_table = "goods"




# 商品订单表
class Orders(models.Model):
    uid = models.ForeignKey(Users)
    linkman = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=6,null=True,blank=True)
    phone = models.CharField(max_length=11)
    add_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    # 0：代发货 1：已发货  2：已收货  3：无效订单
    status = models.CharField(max_length=1,default=0)

    class Meta:
        db_table = 'orders'

class Order_detail(models.Model):
    order_id = models.IntegerField()
    goods_id = models.IntegerField()
    goods_num = models.IntegerField()

    class Meta:
        db_table = 'order_detail'






