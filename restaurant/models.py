from django.db import models

# Create your models here.


class Dish(models.Model):
    """餐馆里面的一道菜"""
    # 菜的名字
    name = models.CharField(max_length=20)
    # 菜的价格
    price = models.IntegerField(default=0)
    # 菜的种类,food;drink;salads
    kind = models.CharField(max_length=10)
    # 菜的销量
    sale = models.IntegerField(default=0)
    # 菜的图片,图片的根目录是MEDIA_ROOT规定的,这里的upload_to是子文件夹的名称
    picture = models.ImageField(upload_to='dish_pic/')

    def __str__(self):
        """返回一道菜品的信息"""
        basic_txt = '菜名是：' + self.name + ',' + '价格是：' + str(self.price)
        add_txt = '这道菜的销量是 :' + str(self.sale) + ',' + '这道菜的种类为：' + self.kind
        return basic_txt + ',' + add_txt


class Bill(models.Model):
    """
    记录单个客人的账单
    这个表的一个实例是，一道菜的详细订单信息，包括菜名，下单数量，客户对这道菜的要求
    整个表的内容是客人一次点单的信息，在结账完成之后，这个表清空
    """
    # 点过的菜名，菜名设为主键，是为了客户可以重新设置菜品要求然后进行覆盖
    dish_name = models.CharField(max_length=10, primary_key=True)
    # 客户的桌号
    dish_table = models.IntegerField(default=0)
    # 一道菜点的数量
    dish_number = models.IntegerField(default=0)
    # 顾客对一道菜的要求
    dish_require = models.CharField(max_length=50, default='无')
    # 一道菜的总价，数量*单价
    dish_price = models.CharField(max_length=20, default='0')
    # 那道菜的ID，方便到时候跳转
    dish_id = models.IntegerField(default=0)

    def __str__(self):
        """显示信息"""
        txt = '菜名是：' + self.dish_name + ',' + '数量是:' + str(self.dish_number)
        add_txt = '客户的要求是：' + self.dish_require
        return txt + ',' + add_txt


class DishComment(models.Model):
    """记录顾客对每道菜品的评价"""
    name = models.ForeignKey(Dish, on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.comment[:20] + '...'


class ServerComment(models.Model):
    """记录顾客对我们餐厅服务的评价"""
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.comment[:20] + '...'
