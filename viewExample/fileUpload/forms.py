from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

# 处理这个表单的视图将在request.FILES中收到文件数据，可以用request.FILES['file']来获取上传文件的具体数据，其中的键值‘file’是根据file = forms.FileField()的变量名来的。
#
# 注意：request.FILES只有在请求方法为POST,并且提交请求的<form>具有enctype="multipart/form-data"属性时才有效。 否则，request.FILES将为空。




# 如果要使用一个表单字段同时上传多个文件，需要设置字段HTML标签的multiple属性为True
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))