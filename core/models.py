from django.db import models
from core.constans import GENDER_CHOICES,SUBJECT_CHOICES, POST_TYPE
from accounts.models import CustomUser


class Post(models.Model):
    title=models.CharField(max_length=40,verbose_name='عنوان')
    content=models.TextField(verbose_name='محتوا')
    created_at=models.DateTimeField(verbose_name='تاریخ ساخت',auto_now_add=True)
    user=models.ForeignKey(to=CustomUser,on_delete=models.CASCADE,verbose_name='کاربر', related_name='posts')
    post_type=models.CharField(max_length=20,verbose_name='نوع پست', default='نظم', choices=POST_TYPE)
    subject=models.CharField(max_length=20,choices=SUBJECT_CHOICES,null=True,default='love', verbose_name='موضوع')
    class Meta:
        verbose_name='پست'
        verbose_name_plural='پست'

   
   
class Comment(models.Model):
    content = models.CharField(max_length=255, verbose_name='نظر')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='پست', related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='کاربر', related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ نگارش')
    
    