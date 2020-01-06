from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import View
import os
from certificate import settings

def index(request):

    return render(request, "page/home.html", {})

def html_view(request):

    return render(request, "pdf/certificate.html", {})

def link_callback(uri, rel):
    
    # use short variable names
    s_url = settings.STATIC_URL      # Typically /static/
    s_root = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    m_url = settings.MEDIA_URL       # Typically /static/media/
    m_root = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(m_url):
        path = os.path.join(m_root, uri.replace(m_url, ""))
    elif uri.startswith(s_url):
        path = os.path.join(s_root, uri.replace(s_url, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (s_url, m_url)
            )
    return path

# pdf render func
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            "data_1": 'İışŞÇçÖöĞğÜü',
            "data_2": "John Cooper",
            "data_3": 1399.99,
            "data_4": "Today",
        }
        pdf = render_to_pdf('pdf/certificate.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# view and download
class DownloadPdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf/certificate.html')
        context = {
            "data_1": 123,
            "data_2": "John Cooper",
            "data_3": 1399.99,
            "data_4": "Today",
        }
        pdf = render_to_pdf('pdf/certificate.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %("dosya_adi")
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

# direct download
def pdf_direct_download(request):
    template_path = 'pdf/certificate.html'
    context = {'data1': 'Lorem, ipsum dolor.'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dosya_adi.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response