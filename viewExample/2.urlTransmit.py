# url 转发
from django.urls import include, path
from viewExample import views

# 通过 include 二级转发，它会去掉URL中匹配的部分并将剩下的字符串发送给include的URLconf做进一步处理，也就是转发到二级路由去。
urlpatterns = [
    # ... 省略...
    path('community/', include('aggregator.urls')),
    path('contact/', include('contact.urls')),
    # ... 省略 ...
]


# 公共前缀
urlpatterns2 = [
    path('<page_slug>-<page_id>/', include([
        path('history/', views.history),
        path('edit/', views.edit),
        path('discuss/', views.discuss),
        path('permissions/', views.permissions),
    ])),
]


# URLconfs具有一个钩子（hook），传递额外参数，避免和url里参数同名
urlpatterns3 = [
    path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
]