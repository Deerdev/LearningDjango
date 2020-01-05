from django.db import models
from django.utils import timezone
import datetime

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    # 判断是否是最近一天发布
    def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        # 不展示未来的数据
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # djadmin was_published_recently 展示优化
    was_published_recently.admin_order_field = 'pub_date'   # 排序方式
    was_published_recently.boolean = True       # bool 值方式展示
    was_published_recently.short_description = 'Published recently?' # 标题


class Choice(models.Model):
    # 关联键值对
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text



### python manage.py shell

# >>> from polls.models import Question, Choice # 导入我们写的模型类
# # 现在系统内还没有questions对象
# >>> Question.objects.all()
# <QuerySet []>
#
# # 创建一个新的question对象
# # Django推荐使用timezone.now()代替python内置的datetime.datetime.now()
# # 这个timezone就来自于Django的依赖库pytz
# from django.utils import timezone
# >>> q = Question(question_text="What's new?", pub_date=timezone.now())
#
# # 你必须显式的调用save()方法，才能将对象保存到数据库内
# >>> q.save()
#
# # 默认情况，你会自动获得一个自增的名为id的主键
# >>> q.id
# 1
#
# # 通过python的属性调用方式，访问模型字段的值
# >>> q.question_text
# "What's new?"
# >>> q.pub_date
# datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)
#
# # 通过修改属性来修改字段的值，然后显式的调用save方法进行保存。
# >>> q.question_text = "What's up?"
# >>> q.save()
#
# # objects.all() 用于查询数据库内的所有questions
# >>> Question.objects.all()
# <QuerySet [<Question: Question object>]>
#
# # 创建3个choices.
# >>> q.choice_set.create(choice_text='Not much', votes=0)
# <Choice: Not much>
# >>> q.choice_set.create(choice_text='The sky', votes=0)
# <Choice: The sky>
# >>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
