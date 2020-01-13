from django.urls import path, register_converter

from . import views

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]

# path转换器
# str：匹配任何非空字符串，但不含斜杠/，如果你没有专门指定转换器，那么这个是默认使用的；
# # int：匹配0和正整数，返回一个int类型
# # slug：可理解为注释、后缀、附属等概念，是url拖在最后的一部分解释性字符。该转换器匹配任何ASCII字符以及连接符和下划线，比如building-your-1st-django-site；
# # uuid：匹配一个uuid格式的对象。为了防止冲突，规定必须使用破折号，所有字母必须小写，例如075194d3-6885-417e-a8a8-6c931e272f00。返回一个UUID对象；
# # path：匹配任何非空字符串，重点是可以包含路径分隔符’/‘。这个转换器可以帮助你匹配整个url而不是一段一段的url字符串。要区分path转换器和path()方法。


# 自定义path转换器
class FourDigitYearConverter:
    regex = '[0-9]{4}'

    # 转换为 python 类型
    def to_python(self, value):
        return int(value)

    # python 类型转换为 url
    def to_url(self, value):
        return '%04d' % value

register_converter(FourDigitYearConverter, 'yyyy')

# yyyy 类型可以使用，使用 FourDigitYearConverter 解析 yyyy 类型
urlpatterns2 = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<yyyy:year>/', views.year_archive),
    ...
]



# 配置默认参数
urlpatterns = [
    path('blog/', views.page),
    path('blog/page<int:num>/', views.page),
]

# 匹配第一个path默认参数 num = 1
def page(request, num=1):
    # Output the appropriate page of blog entries, according to num.
    # ...
    pass


# 自定义 404
# 增加的条目
handler400 = views.bad_request
handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.error

# ---
def bad_request(request):
    return render(request, '400.html')


def permission_denied(request):
    return render(request, '403.html')


def page_not_found(request):
    return render(request, '404.html')


def error(request):
    return render(request, '500.html')