from django.http import HttpResponse, HttpResponseNotFound
import datetime
from django.http import Http404
from django.shortcuts import render

# 首先，从django.http模块导入了HttpResponse类，以及Python的datetime库。
# 接着，我们定义了current_datetime视图函数。
# 每个视图函数都接收一个HttpRequest对象作为第一位置参数，一般取名为request，你可以取别的名字，但这不符合潜规则，最好不要那么做。
# 视图函数的名称没有强制规则，但尽量不要和Python及Django内置的各种名称重名，并且尽量精确地反映出它的功能，比如这里的current_datetime。
# 该视图返回一个HttpResponse对象，其中包含生成的HTML页面

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

# 返回异常
def my_view(request):
    # ...
    foo = False
    if foo:
        # 404
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        # Return a "created" (201) response code.
        return HttpResponse(status=201)


# 404异常，Django会捕获它，并且带上HTTP404错误码返回你当前app的标准错误页面或者自定义错误页面
def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'polls/detail.html', {'poll': p})