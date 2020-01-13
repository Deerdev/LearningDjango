from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, ModelFormWithFileField

# 另外写一个处理上传过来的文件的方法，并在这里导入
from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES) # 注意获取数据的方式, 必须将request.FILES传递到form的构造函数中
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


# ----
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():    # 遍历UploadedFile.chunks()，而不是直接使用read()方法，能确保大文件不会占用系统过多的内存。
            destination.write(chunk)





# 使用模型处理上传的文件


def upload_file2(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # 这么做就可以了，文件会被保存到Model中upload_to参数指定的位置
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'upload.html', {'form': form})


# 如果手动构造一个对象，还可以简单地把文件对象直接从request.FILES赋值给模型：

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .models import ModelWithFileField

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 自定义model
            instance = ModelWithFileField(file_field=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})



# 上传多个文件
# 自己编写一个FormView的子类，并覆盖它的post方法，来处理多个文件上传：
from django.views.generic.edit import FormView
from .forms import FileFieldForm
class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # 用你的模版名替换.
    success_url = '...'  # 用你的URL或者reverse()替换.

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



