from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path("not_login_user", views.not_login_user, name="not_login_user" ),
    path("register", views.register, name="register" ),
    path("login", views.login, name="login" ),
    path("", views.HomeView.as_view(), name="home-page"),

    path("restauran", views.RestaurantView.as_view(), name="restaurant"),
    path("customuser", views.CustomUserCreateView.as_view(), name="customuser"),

    path("order", views.OrderList.as_view(), name="order"),
    path("order/user", views.OrderCreate.as_view(), name="order_users"),
    path('order/<int:pk>/update/', views.OrderUpdate.as_view(), name='order_update'),
    path('orderfood/', views.OrderFoodList.as_view(), name='order_food'),
    path('order/<int:pk>/update/foood', views.OrderUpdateFood.as_view(), name='order_update_food'),

    path("reviews", views.ReviewsCreateView.as_view(), name="comments-create"),
    path("reviews/list", views.ReviewsListView.as_view(), name="comments"),

    path("workers/list", views.WorkersListView.as_view(), name="workers"),
    path("workers", views.WorkersCreateView.as_view(), name="workers-create"),

    path("menu/list", views.MenuListView.as_view(), name="menu"),
    
    path("order_menu", views.MenuOrderView.as_view(), name="order_menu"),
    path("menu_create", views.MenuCreateView.as_view(), name="menu-create"),

    path("menu/<int:pk>/special/", views.AddSpecial.as_view(), name="special_all"),
    path("special/", views.SpecialList.as_view(), name="special"),
    
    path("start_page", views.StartView.as_view(), name="start_page"),

    path('more_info/', views.MoreInformation.as_view(), name='more_information'),

]