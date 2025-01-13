from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import AddCommentForm


@login_required
def add_comment(request, movie_id):
    reply_form = AddCommentForm()
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie_id = movie_id
            comment.user = request.user
            comment.save()
            return redirect('movie_details', movie_id=movie_id)
    else:
        comment_form = AddCommentForm()
        return render(request, 'Comment/comment-form.html', {'form': comment_form, 'reply_form': reply_form})


@login_required
def reply_comment(request, movie_id, parent_id):
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie_id = movie_id
            comment.user = request.user
            comment.parent_id = parent_id
            comment.save()
            return redirect('movie_details', movie_id=movie_id)
    else:
        comment_form = AddCommentForm()
        return render(request, 'Comment/reply-comment-form.html', {'reply_form': comment_form})



# @login_required
# def like_comment(request, comment_id, movie_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     like, created = CommentLikes.objects.get_or_created(user=request.user, comment=comment)
#
#     if not created:
#         like.delete()
#     return redirect('movie_details', movie_id=movie_id)



    # if request.method == 'POST':
    #     query = request.GET.get('reaction', '')
    #     # srch = movie_api.search(query)
    #
    #     context = {
    #         'query': query
    #     }
    #     return render(request, 'Movies/search-details.html', context)