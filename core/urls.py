from django.urls import path
from core.views import home, post_detail,new_post, edit_post, delete_post, about, export_posts_pdf, post_type_plot, export_posts_csv

app_name = 'core'

urlpatterns = [
    path('',home,name='home'),
    path('post/<int:id>/', post_detail,name='post_detail'), 
    path('post/new/',new_post,name='new_post'),
    path('edit-post/<int:id>/',edit_post,name='edit_post'),
    path('delete-post/<int:id>/',delete_post,name='delete_post'),
    path('edit-post/<int:id>/', edit_post, name='edit_post'),
    path('about/', about, name='about'),
    path('report/pdf/', export_posts_pdf, name='report_pdf'),
    path('report/plot/', post_type_plot, name='report_plot'),
    path('report/csv/', export_posts_csv, name='report_csv'),
]