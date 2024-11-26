from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import CommentForm
from .models import Post

from django.core.paginator import Paginator

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/blog.html"
    paginate_by = 3



def blog_list(request):
    blogs = Post.objects.filter(status=1).order_by('-created_on')  # Filtrar posts publicados

    paginator = Paginator(blogs, 3)  # 5 entradas por página

    page_number = request.GET.get('page')  # Obtén el número de página actual
    page_obj = paginator.get_page(page_number)  # Obtén los objetos de la página actual

    return render(request, 'blog/blog.html', {'page_obj': page_obj})
# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, pk):
    template_name = "blog/blog-detail.html"
    post = get_object_or_404(Post, id=pk)
    # comments = post.comments.filter(active=True).order_by("-created_on")
    # new_comment = None
    # Comment posted
    # if request.method == "POST":
    #     comment_form = CommentForm(data=request.POST)
    #     if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            # new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            # new_comment.post = post
            # Save the comment to the database
            # new_comment.save()
    # else:
        # comment_form = CommentForm()
    return render(
        request,
        template_name,
        {
            "post": post,
            # "comments": comments,
            # "new_comment": new_comment,
            # "comment_form": comment_form,
        },
    )
