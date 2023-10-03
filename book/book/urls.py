
# urls.py
from django.urls import path
from twodb_app import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
]

