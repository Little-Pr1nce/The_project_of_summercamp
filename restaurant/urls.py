"""restaurant这个应用的urls设计"""

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'restaurant'

urlpatterns = [

    # 餐馆的主页
    url(r'^$', views.index, name='index'),

    # 单个菜品的详细页面,并可以点餐
    url(r'^(?P<dish_id>\d+)/$', views.dish_detail, name='dish'),

    # 显示账单
    url(r'^bill/(?P<table>\d+)/$', views.get_bill, name='bill'),

    # 结完账之后去给服务进行评价
    url(r'^bill/evaluation/$', views.service_evaluation, name='evaluation'),

    # 显示图表
    url(r'^graph/1/$', views.graph_food, name='graph_food'),
    url(r'^graph/2/$', views.graph_drinks, name='graph_drinks'),
    url(r'^graph/3/$', views.graph_salads, name='graph_salads'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 用来指向media，使html文件里面可以直接使用URL来调用
