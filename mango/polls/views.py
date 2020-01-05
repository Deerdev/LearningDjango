from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.views import generic
from django.urls import reverse

# 两种通用视图ListView和DetailView（它们是作为父类被继承的）。这两者分别代表“显示一个对象的列表”和“显示特定类型对象的详细页面”的抽象概念
# 通过 model 和 template_name 绑定模型和模板
class IndexView(generic.ListView):
    # ListView通用视图使用一个默认模板称为<app name>/<model name>_list.html
    template_name = 'polls/index.html'

    # 默认会使用 question_list，绑定question的所以list
    # 指定说我们希望使用latest_question_list而不是question_list
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # DetailView通用视图使用一个称作<app name>/<model name>_detail.html的模板
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    # 1. 使用 template loader
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))
    # 2. 使用 shortcuts render, HttpResponse 也不需要
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # 1. 常规 404 写法
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return HttpResponse("You're looking at question %s." % question_id)

    # 2. get_object_or_404 快速404
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] 参数获取方式，request.POST[’choice’,None] 提供默认值
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 跳转到新页面
        # HttpResponseRedirect的构造器中使用了一个reverse()函数。它能帮助我们避免在视图函数中硬编码URL。
        # 它首先需要一个我们在URLconf中指定的name，然后是传递的数据。例如'/polls/3/results/'，其中的3是某个question.id的值。
        # 重定向后将进入polls:results对应的视图，并将question.id传递给它。白话来讲，就是把活扔给另外一个路由对应的视图去干。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



