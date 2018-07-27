from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Create your views here.
from .models import Dish, Bill, ServerComment


def index(request):
    """显示餐馆的主页"""
    if request.method != 'POST':  # 如果顾客只是查看这个主页
        # 选出种类是food的菜品
        dishes_food = Dish.objects.filter(kind='food')
        # 选出种类是drinks的菜品
        dishes_drinks = Dish.objects.filter(kind='drinks')
        # 选出种类是salads的菜品
        dishes_salads = Dish.objects.filter(kind='salads')
        # 得到对餐厅的评论，最新的三条
        # 首先计算数据库里有几条评论
        number = 0
        a = ServerComment.objects.all()
        for b in a:
            number = number + 1
        # 从数据库的尾部得到最新的三条评论
        server_comments = ServerComment.objects.all()[number - 3:number]
        comments = []
        for comment in server_comments:
            comments.append(comment)
        comment1 = comments[0]
        comment2 = comments[1]
        comment3 = comments[2]

        content = {'dishes_food': dishes_food, 'dishes_drinks': dishes_drinks,
                   'dishes_salads': dishes_salads, 'comment1': comment1,
                   'comment2': comment2, 'comment3': comment3}
        return render(request, 'restaurant/index.html', content)
    else:
        # 客户输入自己的桌号查看自己的账单
        table = request.POST['table']
        return HttpResponseRedirect(reverse('restaurant:bill', args=table))


def dish_detail(request, dish_id):
    """显示单个菜品的详细信息,并且可以点菜"""
    # 根据从url得到的id来的到对应的菜品
    dish = Dish.objects.get(id=dish_id)
    # 得到对应菜品的图片路径，并且string化
    dish_path = str(dish.picture)

    if request.method != 'POST':
        # 如果用户不是提交点菜的相关信息，就显示菜品的详细信息
        content = {'dish': dish, 'dish_path': dish_path}
        return render(request, 'restaurant/dish.html', content)
    else:
        # 用户提交数据
        table = request.POST['table']  # 客户的桌号
        number = request.POST['number']  # 客户点了几道这个菜
        require = request.POST['require']  # 客户对这道菜的要求
        """在模型里面设置了dish_name为主键，所以即使再次提交需求也可以覆盖之前的信息，保证了客户可以更改点菜要求的功能"""
        price = int(number) * int(dish.price)
        bill = Bill(dish_name=dish.name, dish_number=number, dish_table=table,
                    dish_require=require, dish_price=str(price), dish_id=dish.id)
        bill.save()  # 把点的菜保存到bill里
        return HttpResponseRedirect(reverse_lazy('restaurant:index'))


def get_bill(request, table):
    """显示用户点的菜，并且用户可以去结账"""
    # 如果客户只是查看这个页面
    if request.method != 'POST':
        # 得到所有点过的菜品
        bills = Bill.objects.filter(dish_table=table)
        price = 0
        for dish in bills:
            # 计算总价
            price = price + int(dish.dish_price)

        content = {'bills': bills, 'price': price, 'table': table}
        return render(request, 'restaurant/bill.html', content)
    else:
        # 用户要结账，就清空bill这个表，并且更新销量信息
        bills = Bill.objects.filter(dish_table=table) # 得到整个账单
        # 获取账单里面一道菜的信息，得到菜名和点菜数量
        for bill in bills:
            # 通过菜品的名字得到一道菜，但是名字不是主键有可能得到很多相同的菜品，所以要用for来得到单个菜品，但是菜名也是一个主键
            dishes = Dish.objects.filter(name=bill.dish_name)
            for dish in dishes:
                dish.sale = dish.sale + bill.dish_number
                dish.save()

        bills.delete()
        return HttpResponseRedirect(reverse_lazy('restaurant:evaluation'))


def service_evaluation(request):
    """用户服务进行评论"""
    # 顾客访问这个页面
    if request.method != 'POST':
        return render(request, 'restaurant/comment.html')
    else:
        # 客户提交评价，然后跳转到主页
        comment = request.POST['comment']
        serve_comment = ServerComment(comment=comment)
        serve_comment.save()
        return HttpResponseRedirect(reverse_lazy('restaurant:index'))


def graph_food(request):
    """根据数据库的数据绘制图表"""
    dishes_food = Dish.objects.filter(kind='food')
    content = {'dishes_food': dishes_food}

    return render(request, 'restaurant/graph_food.html', content)


def graph_salads(request):
    """根据数据库的数据绘制图表"""
    dishes_salads = Dish.objects.filter(kind='salads')
    content = {'dishes_salads': dishes_salads}

    return render(request, 'restaurant/graph_salads.html', content)


def graph_drinks(request):
    """根据数据库的数据绘制图表"""
    dishes_drinks = Dish.objects.filter(kind='drinks')
    content = {'dishes_drinks': dishes_drinks}

    return render(request, 'restaurant/graph_drinks.html', content)
