from django.urls import path
from blog import views

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new/',views.postcreateview,name='post_new'),
    path('post/<int:pk>/bfhewnjmfmkwefmeowmfkemwhjifnewhifnehiwnfejiwnfjiew',views.PostUpdateView.as_view(),name='post_edit'),
    path('post/<int:pk>/ftwygqbunciomkmeqjcnhubgewuvhnijmewjivmjdiwhvbnewmkovkew',views.PostDeleteView.as_view(),name='post_remove'),
    path('post/<int:pk>/publish/',views.post_publish,name='post_publish'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve/',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove/',views.comment_remove,name='comment_remove'),
    path('like/<int:pk>', views.likeview, name='like_post'),
    path('post/search/',views.search_posts,name='search_posts'),

]
