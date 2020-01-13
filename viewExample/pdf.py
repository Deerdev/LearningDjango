# pip install reportlab
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # 创建带有PDF头部定义的HttpResponse对象
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # 创建一个PDF对象，并使用响应对象作为它要处理的‘文件’
    p = canvas.Canvas(response)

    # 通过PDF对象的drawString方法，写入一条信息。具体参考模块的官方文档说明。
    p.drawString(100, 100, "Hello world.")

    # 关闭PDF对象
    p.showPage()
    p.save()
    return response

# reportlab 非线程安全


# 处理复杂pdf
# 使用ReportLab创建复杂的PDF文档时，可以考虑使用io库作为PDF文件的临时保存地点。
# 这个库提供了一个类似于文件的对象接口，非常实用。 下面的例子是上面的“Hello World”示例采用io重写后的样子：
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response