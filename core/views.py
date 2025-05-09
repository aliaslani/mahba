from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.contrib import messages
from core.models import Post
from core.forms import NewPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
import io
# Create your views here.
import jdatetime
from jalali_date import datetime2jalali, date2jalali
import plotly.express as px
from django.http import JsonResponse
from django.template.loader import render_to_string
import csv

@login_required
def export_posts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'User', 'Created At'])

    for post in Post.objects.all():
        writer.writerow([post.id, post.title, post.user.username, post.created_at])

    return response

@login_required
def post_type_plot(request):
    from core.models import Post
    from django.db.models import Count

    data = Post.objects.values('post_type').annotate(count=Count('id'))
    fig = px.pie(data, names='post_type', values='count', title="Post Type Distribution")

    graph_html = fig.to_html(full_html=False)
    return render(request, 'core/plot.html', {'plot': graph_html})

@login_required
def export_posts_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    posts = Post.objects.order_by('-created_at')[:20]
    y = 800
    p.setFont("Helvetica", 12)
    p.drawString(100, 820, ("Post Report (Latest 20 Posts)"))

    for post in posts:
        p.drawString(100, y, f"{post.title} - {post.user.username} - {jdatetime.datetime.fromgregorian(datetime=post.created_at).strftime('%Y/%m/%d')}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf')

def home(request):
    posts=Post.objects.order_by('created_at')
    latest_posts = posts[:3]
    return render(request,'core/index.html' , context={'posts':posts, 'latest_posts':latest_posts})

def post_detail(request,id):
    post=get_object_or_404(Post,id=id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
        else:
            return redirect('core:post_detail', id=post.id)
    
    form = CommentForm()
    return render(request,'core/post_detail.html',context={'post':post,  'form':form})



@login_required()
def new_post(request):
    form = NewPostForm()
    if request.method =='POST':
        form =  NewPostForm(request.POST)
        if form.is_valid():
            clean_data =  form.cleaned_data
            new_post = Post.objects.create(title=clean_data.get('title'), content=clean_data.get('content'), user=request.user, post_type=clean_data.get('post_type'), subject=clean_data.get('subject'))
            messages.success(request,'پست شما با موفقیت ذخیره شد')
            return redirect('core:home')
        else:
            messages.error(request, 'فرم معتبر نیست')
            print(form.non_field_errors)
    return render(request,'core/new_post.html', {'form':form})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.user != post.user:
        return HttpResponse('شما اجازه ویرایش این پست را ندارید')
    if request.method == 'POST':
        form = NewPostForm(instance=post, data=request.POST)
        
        if form.is_valid():
            
            data = form.cleaned_data
            
            form.save()
            messages.success(request, 'پست شما با موفقیت ویرایش شد')
            return redirect('core:post_detail', id=post.id)
        else:
            messages.error(request, 'اطلاعات فرم معتبر نیست')
    form = NewPostForm(initial={'title':post.title, 'content':post.content, 'user':post.user, 'post_type':post.post_type, 'subject':post.subject})
    return render(request, 'core/edit_post.html', {'post':post, 'form':form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    messages.success(request, 'پست با موفقیت حذف شد')
    return redirect('core:home')


def about(request):
    return render(request, 'core/about.html')

