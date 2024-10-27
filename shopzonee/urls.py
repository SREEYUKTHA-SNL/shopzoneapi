from django.urls import path,include
from . import views


urlpatterns = [
   path('registration/',views.registraion_api.as_view(),name='registration'),
   path('login/',views.login_api.as_view(),name='login'),


   path('viewusers/',views.viewuser_api.as_view(),name='viewuser'),
   path('viewsingleusers/<int:id>',views.viewsingleuser_api.as_view(),name='viewsingleuser'),
   path('deleteusers/<int:id>',views.deleteusers_api.as_view(),name='deleteusers'),
   path('updateusers/<int:id>',views.updateusers_api.as_view(),name='updateusers'),


   path('addproductview/',views.addproductview_api.as_view(),name='addproductview'),
   path('viewproduct/',views.viewproduct_api.as_view(),name='viewproduct'),
   path('viewsingleproduct/<int:id>',views.viewsingleproduct_api.as_view(),name='viewsingleproduct'),
   path('deleteproduct/<int:id>',views.deleteproduct_api.as_view(),name='deleteproduct'),
   path('updateproduct/<int:id>',views.updateproduct_api.as_view(),name='updateproduct'),


   path('addcategory/',views.addcategory_api.as_view(),name='addcategory'),
   path('viewcategory/',views.viewcategory_api.as_view(),name='viewcategory'),
   path('viewsinglecategory/<int:category_id>',views.viewsinglecategory_api.as_view(),name='viewsinglecategory'),
   path('updatecategory/<int:id>',views.updatecategory_api.as_view(),name='updatecategory'),

   path('addsubcategory/',views.addsubcategory_api.as_view(),name='addsubcategory'),
   path('viewsubcategory/',views.viewsubcategory_api.as_view(),name='viewsubcategory'),
   path('viewsinglesubcategory/<int:subcategory_id>', views.viewsinglesubcategory_api.as_view(), name='viewsinglesubcategory'),
   path('updatesubcategory/<int:subcategory_id>',views.updatesubcategory_api.as_view(),name='updatesubcategory'),


   path('review/',views.review_api.as_view(),name='review'),
   path('viewreview/',views.viewreview_api.as_view(),name='viewreview'),
   path('viewsinglereview/<int:id>',views.viewsinglereview_api.as_view(),name='viewsinglereview'),
   path('deletereview/<int:id>',views.deletereview_api.as_view(),name='deleteview'),
   path('updatereview/<int:id>',views.updatereview_api.as_view(),name='updatereview'),


   path('addcartapi/',views.addcart_api.as_view(),name='addcartapi'),
   path('viewcart/',views.viewcart_api.as_view(),name='viewcart'),
   path('viewsinglecart/<int:userid>',views.viewsinglecart_api.as_view(),name='viewsinglecart'),
   path('deletercart/<int:id>',views.deletecart_api.as_view(),name='deletecart'),

   path('addwishlist/',views.addwishlist_api.as_view(),name='addwishlist'),

   path('order/<int:userid>',views.order_api.as_view(),name='order'),
   path('OrderViewApi/<int:userid>',views.OrderViewApi.as_view(),name='OrderViewApi'),


   path('addaddress/',views.addaddress_api.as_view(),name='addaddress'),
   path('viewaddress/',views.viewaddress_api.as_view(),name='viewaddress'),
   path('updateaddress/<int:userid>',views.updateaddress_api.as_view(),name='updateaddress'),
   path('deleteaddress/<int:id>',views.deleteaddress_api.as_view(),name='deleteaddress'),

   
   path('search/',views.search_api.as_view(),name='search'),
   path('changepassword/<int:id>',views.changepassword_api.as_view(),name='changepassword'),
  
]