from django.forms import Form, ModelForm
from django import forms
from django.forms import ValidationError
from django.core import validators
from core.models import Post, Comment
from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','post_type','subject']


        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'post_type': forms.Select(attrs={'class':'form-select'}),
            'subject': forms.Select(attrs={'class':'form-select'}),
        }

    def clean_title(self):
        data = self.cleaned_data
        t = data.get('title')
        if len(t) < 3:
            raise ValidationError('این فیلد نمی تواند کمتر از سه کاراکتر داشته باشد')
        return t
    

    def clean_content(self):
        data = self.cleaned_data
        title = data.get('title')
        content = data.get('content')
        if title == content:
            raise ValidationError('عنوان و محتوا نمی تواند شبیه به هم باشد')
        return content
    
    def clean_post_type(self):
        data = self.cleaned_data
        post_type = data.get('post_type')
        valid_types = [
            'نثر',
            'نظم',
            'عکس',
            'محاوره',
        ]

        if post_type not in valid_types:
            raise ValidationError(f"این فیلد فقط می تواند شامل این موارد باشد: {'/'.join(valid_types)}")
        return post_type
    

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        widgets = {
            'content': forms.Textarea(attrs={'calss':'form-control', 'cols':80, 'rows':8})
        }
