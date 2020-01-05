import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question

# 运行 test case
# python manage.py test polls
#
# 这其中都发生了些什么？：
#
# python manage.py test polls命令会查找投票应用中所有的测试程序
# 发现一个django.test.TestCase的子类
# 为测试创建一个专用的数据库
# 查找名字以test开头的测试方法
# 在test_was_published_recently_with_future_question方法中，创建一个Question实例，该实例的pub_data字段的值是30天后的未来日期。
# 然后利用assertIs()方法，它发现was_published_recently()返回了True，而不是我们希望的False。

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        在将来发布的问卷应该返回False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        只要是超过1天的问卷，返回False
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        最近一天内的问卷，返回True
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)