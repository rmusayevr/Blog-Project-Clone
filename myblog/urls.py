from .views import *
from django.urls import path


urlpatterns = [
    path("", PostListView.as_view(template_name="post_list.html"), name = "post_list"),
    path("about/", AboutView.as_view(), name = "about"),
    path("post/<int:pk>/", PostDetailView.as_view(template_name="post_detail.html"), name = "post_detail"),
    path("post/create/", PostCreateView.as_view(template_name="post_form.html"), name = "create_post"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(template_name="post_form.html"), name = "update_post"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(template_name="post_confirm_delete.html"), name = "delete_post"),
    path("post/drafts/", PostDraftsListView.as_view(template_name="post_drafts.html"), name="post_drafts_list"),
    path("post/<int:pk>/comments/", add_comments, name="add_comments"),
    path("post/comment/<int:pk>/remove/", remove_comment, name="remove_comment"),
    path("post/comment/<int:pk>/approve/", approve_comment, name="approve_comment"),
    path("post/<int:pk>/publish/", post_publish, name="post_publish"),

]