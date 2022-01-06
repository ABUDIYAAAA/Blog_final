from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from blog.models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm,CommentForm, PostEditForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        """
        Using Django ORM(Object Relational Mapping) with DB, this querysets allows
        perform SQLqueries in a 'pythonish' way,
        which just means from model 'Post' grab all 'objects'(ie posts) 'filter' it out based on 'published_date'
        attribute less than or equal to(lte) the current time(timezone.now()),'order_by' descending order of ("-")
        published date.
        lller SQL query
        'SELECT * FROM Post WHERE published_date <= timezone.now()'
        """
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    """
    Detail view of post, post_detail.html
    """
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post,pk=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context["liked"] = liked
        return context


# class CreatePostView(LoginRequiredMixin,CreateView):
#     """
#     view of formpage to write up the post, similar to 'login_required' decorator CBV's got
#     mixins which inherits to the classes provides the same functionality that a user must be
#     logged in, to add a post
#     """
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    """
    The PostUpdateView is same as CreatePostview, but in here there's only
    updation of the existing one happens
    """
    login_url = '/signin'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    """
    This view Deletes the post from the DB,(DeleteView-manages that)
    if the post is deleted, it takes user back to 'Post list view'
    """
    model = Post
    success_url = reverse_lazy('post_list')

#######################################
## Functions that require a pk match ##
#######################################
@login_required(login_url="/signin")
def postcreateview(request):
    form = PostForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            user = User.objects.get(username=request.user.username)
            post.author = user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm
        return render(request, 'blog/post_form.html', {'form': form})




@login_required(login_url="/signin")
def post_publish(request,pk):
    """
    To publish the post, using the method 'publish' in model class 'Post'
    :param request:
    :param pk:
    :return: to the post_detail view of published post
    """
    post = get_object_or_404(Post,pk=pk)
    popst = str(post.author)
    if popst == request.user.username:
        post.publish()
        return redirect('post_detail',pk=pk)
    else:
        return render(request, 'blog/fail_page.html', {'reason': "ITS NOT YOUR POST BUDDY SO CHILL"})


def add_comment_to_post(request,pk):
    """
    To add a comment when a 'request' with primary key('pk') of post given,
    :param request:
    :param pk:
    :return: the html tag 'form' and the form is created based on logic
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                user = request.user.username
                comment.author = str(user)
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=pk)
            else:
                comment.author = 'anonymous'
                comment.post = post
                comment.save()
                return redirect('post_detail',pk=post.pk)

    else:
        form = CommentForm
    return render(request,'blog/comment_form.html',{'form':form})

@login_required(login_url="/signin")
def comment_approve(request,pk):
    """
    View to approve comment, using the 'approve' method in Comment model,
    ie, when 'approve' method called it sets the boolean value 'True'
    :param request:
    :param pk:
    :return: to the post_detail view of current post
    """
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required(login_url="/signin")
def comment_remove(request,pk):
    """
    View to Delete a comment, using the 'delete' method in Comment model( native in 'models.Model'),
    an extra variable required to store the key value of comment(ie key of post) to delete
    :param request:
    :param pk:
    :return: to the post_detail view of current post
    """
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required(login_url='/signin')
def likeview(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        Liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post_detail',args=[str(pk)]))
