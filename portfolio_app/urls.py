from django.urls import path, include

from .views import (index, register, PortfolioListView, PortfolioUpdateView, PortfolioDeleteView, portfolio_detail,
                    update_item, delete_item)

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('myportfolios/', PortfolioListView.as_view(), name='myportfolios'),
    path('portfolio/<int:pk>/', portfolio_detail, name='portfolio_detail'),
    path('update_item/<int:pk>/', update_item, name='update_item'),
    path('delete_item/<int:pk>/', delete_item, name='delete_item'),
    path('myportfolios/<int:pk>/update', PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('myportfolios/<int:pk>/delete', PortfolioDeleteView.as_view(), name='portfolio_delete'),
]
