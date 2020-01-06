from django.contrib import admin
from django.urls import path
from pages.views import GeneratePdf, DownloadPdf, index, pdf_direct_download, html_view

urlpatterns = [
    path('', index, name="home"),
    path('html_view/', html_view, name="html_view"),
    path('pdf_view/', GeneratePdf.as_view(), name="pdf_view"),
    path('pdf_view_download/', DownloadPdf.as_view(), name="pdf_view_download"),
    path('pdf_direct_download', pdf_direct_download, name="pdf_direct_download"),
    path('admin/', admin.site.urls),
]
