from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.home,name='home'),
    path('login_page',views.loginpage,name='login_page'),

    path('admin_home',views.adminhome,name='admin_home'),

    path('login',views.login,name='login'),

    path('add_agency_page',views.addagencypage,name='add_agency_page'),

    path('add_agent',views.addagent,name='add_agent'),

    path('logout',views.logout,name='logout'),

    path('view_agent/<int:dd>',views.viewagent,name='view_agent'),

    path('delete_agent/<int:dd>',views.deleteagent,name='deleteagent'),

    path('edit_agent/<int:dd>',views.editagent,name='edit_agent'),
    path('edit/<int:dd>',views.edit,name='edit'),

    path('agent_home',views.agenthome,name='agent_home'),
    path('edit_profile/<int:dd>',views.editprofile,name='edit_profile'),
    path('edit_pro/<int:dd>',views.editpro,name='edit_pro'),
    path('delete_profile/<int:dd>',views.deleteprofile,name='delete_profile'),

    path('add_customer',views.addcustomer,name='add_customer'),
    path('add_cus',views.addcus,name='add_cus'),

    path('dash_board',views.dashboard,name='dash_board'),
    path('view_customer/<int:dd>',views.viewcustomer,name='view_customer'),
    path('edit_customer/<int:dd>',views.editcustomer,name='edit_customer'),
    path('edit_cus/<int:dd>',views.editcus,name='edit_cus'),
    path('delete_customer/<int:dd>',views.deletecustomer,name='delete_customer'),
]