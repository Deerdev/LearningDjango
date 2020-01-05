from django.contrib import admin
from .models import Question, Choice


# TabularInline 更紧凑的排版
# class ChoiceInline(admin.TabularInline):
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # 显示字段：它是一个由字段组成的元组，其中的每一个字段都会按顺序显示在“change list”页面上
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # 编辑页面显示的字段，包括顺序
    # fields = ['pub_date', 'question_text']
    # 按区域划分，类似 tableview的group, 标题+字段数组
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    # 筛选方式
    list_filter = ['pub_date']
    # 搜索功能
    search_fields = ['question_text']

    # 显示外键：Choice对象将在Question管理页面进行编辑，默认情况，请提供3个Choice对象的编辑区域
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

# 主仓 admin 页面显示的 models
admin.site.register(Choice)
