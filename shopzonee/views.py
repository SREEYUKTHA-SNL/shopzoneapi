from django.shortcuts import render
from .models import Registration,Login,Product,Review,Cart,Wishlist,Order,Address,Category,Subcategory
from .serializers import RegisterSerializer,LoginSerializer,ProductSerializer,ReviewSerializer,CartSerializer,WishlistSerializer,OrderSerializer,AddressSerializer,CategorySerializer,SubCategorySerializer
from rest_framework.generics import GenericAPIView
from django.conf import settings
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import generics, status
from django.shortcuts import get_object_or_404 
import cloudinary   
import cloudinary.uploader
import cloudinary.api



# Create your views here.
class registraion_api(GenericAPIView):
    serializer_class = RegisterSerializer
    serializer_class_login = LoginSerializer

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        number = request.data.get('number')
      
        role = 'user'

       
        

     
        if Registration.objects.filter(email=email).exists():
            return Response({'message': 'Duplicate email found'}, status=status.HTTP_400_BAD_REQUEST)
        if Registration.objects.filter(number=number).exists():
            return Response({'message': 'Duplicate phone number found'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        login_data = {'email': email, 'password': password, 'role': role}
        serializer_login = self.serializer_class_login(data=login_data)
        
        
        if serializer_login.is_valid():
            log = serializer_login.save()
            login_id = log.id
        else:
            return Response({'message': 'Login creation failed', 'errors': serializer_login.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
        registration_data = {
            'name': name,
            'email': email,
            'password': password,
            'number': number,
            'login_id': login_id,
            'role': role
        }
        serializer = self.serializer_class(data=registration_data)
        
       
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Registration successful', 'success': 1}, status=status.HTTP_200_OK)
        
        return Response({'error': serializer.errors, 'message': 'Registration failed', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

class login_api(GenericAPIView):
    serializer_class=LoginSerializer
    

    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        login_var=Login.objects.filter(email=email,password=password)
        if login_var.count()>0:
            a=LoginSerializer(login_var,many=True)
            for i in a.data:
                login_id=i['id']
                role=i['role']
                registraion_data=Registration.objects.filter(login_id=login_id).values()
                print(registraion_data)
                for i in registraion_data:
                    id=i['id']
                    name=i['name']
                    number=i['number']
            return Response({'data':{'login_id':login_id,'user_id':id,'email':email,'password':password,'name':name,'role':role,'number':number},'success':1,'message':'login successfully'},status=status.HTTP_200_OK)
        else:
           return Response({'data':'user name or password invalid',},status=status.HTTP_400_BAD_REQUEST)

class viewuser_api(GenericAPIView):
    serializer_class=RegisterSerializer
    def get(self,request):
        user=Registration.objects.all()
        if (user.count()>0):
            serializer=RegisterSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)
    

class viewsingleuser_api(GenericAPIView):
    serializer_class=RegisterSerializer
    def get(self,request,id):
        user=Registration.objects.get(pk=id)
        serializer=RegisterSerializer(user)
        return Response(serializer.data)
class deleteusers_api(GenericAPIView):
    serializer_class = RegisterSerializer
    def delete(self, request, id):
        user = get_object_or_404(Registration, pk=id)
        user.delete()
        return Response({'message': 'User deleted', 'success': True}, status=status.HTTP_200_OK)
class updateusers_api(GenericAPIView):
    serializer_class=RegisterSerializer
    def put(self,request,id):
        user=Registration.objects.get(pk=id)
        print(user)
        serializer=RegisterSerializer(instance=user,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)
    

cloudinary.config(cloud_name='dws6st29l',api_key='912175176892196',api_secret='M_eH-684kf_g23lG89QOgt2twXM')
class addproductview_api(GenericAPIView):
    serializer_class=ProductSerializer
    def post(self,request):
        productname=request.data.get('productname')
        price=request.data.get('price')
        category_id=request.data.get('category')
        subcategory_id=request.data.get('subcategory')

        color=request.data.get('color')
        description=request.data.get('description')
        image=request.FILES.get('image')
        size=request.data.get('size')
        if not image:
            return Response({'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)
        try:
            upload_data=cloudinary.uploader.upload(image)
            image_url=upload_data['url']
            serializer=self.serializer_class(data={'productname':productname,'image':image_url,'price':price,'category':category_id,'color':color,'description':description,'size':size,'subcategory':subcategory_id})
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data ,'message':'product added successfully','success':1},status=status.HTTP_200_OK) 
            return Response({'data':serializer.errors,'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'An error occurred: {}'.format(str(e)), 'success': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class viewproduct_api(GenericAPIView):
    serializer_class=ProductSerializer
    def get(self,request):
        user=Product.objects.all()
        if (user.count()>0):
            serializer=ProductSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)       
class viewsingleproduct_api(GenericAPIView):
    serializer_class=ProductSerializer
    def get(self,request,id):
        user=Product.objects.get(pk=id)
        serializer=ProductSerializer(user)
        return Response(serializer.data)
    

class deleteproduct_api(GenericAPIView):
    serializer_class=ProductSerializer
    def delete(self,request,id):
        user=Product.objects.get(pk=id)
        user.delete()
        return Response({'message':'user deleted','success':True},status=status.HTTP_200_OK)

class updateproduct_api(GenericAPIView):
    serializer_class=ProductSerializer
    def put(self,request,id):
        user=Product.objects.get(pk=id)
        print(user)
        serializer=ProductSerializer(instance=user,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)


class addcategory_api(GenericAPIView):
    serializer_class=CategorySerializer
    def post(self,request):
        categoryname=request.data.get('categoryname')
        
       
        
        serializer=self.serializer_class(data={'categoryname':categoryname})
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data ,'message':'product added successfully','success':1},status=status.HTTP_200_OK) 
        return Response({'data':serializer.errors,'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)

class viewcategory_api(GenericAPIView):
    serializer_class=CategorySerializer
    def get(self,request):
        user=Category.objects.all()
        if (user.count()>0):
            serializer=CategorySerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)   
        
class viewsinglecategory_api(GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, category_id=None):
        if  category_id:
            Category = Category.objects.filter(category_id=category_id)
        else:
            Categorys = Category.objects.all()

        if Categorys.exists():
            serializer = CategorySerializer(Categorys, many=True)
            return Response({'data': serializer.data, 'message': 'data get', 'success': True}, status=status.HTTP_200_OK)
        return Response({'data': 'no data available'}, status=status.HTTP_400_BAD_REQUEST)
    

class deletecategory_api(GenericAPIView):
    serializer_class=CategorySerializer
    def delete(self,request,category_id):
        user=Category.objects.get(pk=category_id)
        user.delete()
        return Response({'message':'user deleted','success':True},status=status.HTTP_200_OK)

class updatecategory_api(GenericAPIView):
    serializer_class=CategorySerializer
    def put(self,request,id):
        user=Category.objects.get(pk=id)
        print(user)
        serializer=CategorySerializer(instance=user,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)
    
cloudinary.config(cloud_name='dws6st29l',api_key='912175176892196',api_secret='M_eH-684kf_g23lG89QOgt2twXM')

# class addsubcategory_api(GenericAPIView):
#     serializer_class=SubCategorySerializer
#     def post(self,request):
#         subcategoryname=request.data.get('subcategoryname')
        
#         subcategory_image=request.FILES.get('subcategory_image')
#         category_id=request.data.get('category_id')
#         if not subcategory_image:
#             return Response({'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)
#         try:
#             upload_data=cloudinary.uploader.upload(subcategory_image)
#             image_url=upload_data['url']
#             serializer=self.serializer_class(data={'subcategoryname':subcategoryname,'subcategory_image':image_url,'category_id':category_id})
#             if serializer.is_valid():
#                  serializer.save()
#             return Response({'data':serializer.data ,'message':'product added successfully','success':1},status=status.HTTP_200_OK) 
#         except Exception as e:
#             return Response({'message': 'An error occurred: {}'.format(str(e)), 'success': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class viewsubcategory_api(GenericAPIView):
    serializer_class=SubCategorySerializer
    def get(self,request):
        user=Subcategory.objects.all()
        if (user.count()>0):
            serializer=SubCategorySerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)   
        

# class viewsinglesubcategory_api(GenericAPIView):
#     serializer_class = SubCategorySerializer

#     def get(self, request, subcategory_id=None):
#         try:
#             subcategory = Subcategory.objects.get(id=subcategory_id)
#             products = Product.objects.filter(subcategory=subcategory)

#             subcategory_serializer = self.get_serializer(subcategory)
#             product_serializer = ProductSerializer(products, many=True)

#             return Response({
#                 'subcategory': subcategory_serializer.data,
#                 'products': product_serializer.data,
#                 'message': 'Data retrieved successfully',
#                 'success': True
#             }, status=status.HTTP_200_OK)

#         except Subcategory.DoesNotExist:
#             return Response({
#                 'data': 'Subcategory not found',
#                 'success': False
#             }, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({
#                 'data': str(e),
#                 'success': False
#             }, status=status.HTTP_400_BAD_REQUEST)

    

class addsubcategory_api(GenericAPIView):
    serializer_class = SubCategorySerializer

    def post(self, request):
        subcategory_name = request.data.get('subcategoryname')
        subcategory_image = request.FILES.get('subcategory_image')
        category_id = request.data.get('category_id')

        if not subcategory_name or not category_id:
            return Response({'message': 'subcategoryname and category_id are required', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)
        if not subcategory_image:
            return Response({'message': 'subcategory_image is required', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

        try:
            upload_data = cloudinary.uploader.upload(subcategory_image)
            image_url = upload_data['url']

            serializer = self.serializer_class(data={
                'subcategoryname': subcategory_name,
                'subcategory_image': image_url,
                'category_id': category_id
            })

            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'message': 'Subcategory added successfully', 'success': 1}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Invalid data', 'errors': serializer.errors, 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}', 'success': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class viewsinglesubcategory_api(GenericAPIView):
    serializer_class = SubCategorySerializer

    def get(self, request, subcategory_id=None):
        if not subcategory_id:
            return Response({'message': 'subcategory_id is required', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subcategory = Subcategory.objects.get(id=subcategory_id)
            products = Product.objects.filter(subcategory=subcategory)

            subcategory_serializer = self.get_serializer(subcategory)
            product_serializer = ProductSerializer(products, many=True)

            return Response({
                'subcategory': subcategory_serializer.data,
                'products': product_serializer.data,
                'message': 'Data retrieved successfully',
                'success': True
            }, status=status.HTTP_200_OK)

        except Subcategory.DoesNotExist:
            return Response({'message': 'Subcategory not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}', 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class deletesubcategory_api(GenericAPIView):
    serializer_class=SubCategorySerializer
    def delete(self,request,id):
        user=Subcategory.objects.get(pk=id)
        user.delete()
        return Response({'message':'user deleted','success':True},status=status.HTTP_200_OK)

class updatesubcategory_api(GenericAPIView):
    serializer_class = SubCategorySerializer

    def put(self, request, id):
        try:
            # Try to get the subcategory by ID
            user = Subcategory.objects.get(pk=id)
            
            # Check if there's a new image being uploaded
            subcategory_image = request.FILES.get('subcategory_image')
            if subcategory_image:
                # Upload the new image to Cloudinary
                upload_data = cloudinary.uploader.upload(subcategory_image)
                image_url = upload_data['url']
                
                # Update the request data with the new image URL
                request.data['subcategory_image'] = image_url

            # Attempt to serialize and update the subcategory data
            serializer = SubCategorySerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'message': 'updated successfully', 'success': 1}, status=status.HTTP_200_OK)
            else:
                # Return an error if the serializer is not valid
                return Response({'message': 'Invalid data', 'errors': serializer.errors, 'success': 0}, status=status.HTTP_400_BAD_REQUEST)
        
        except Subcategory.DoesNotExist:
            # Handle the case where the subcategory does not exist
            return Response({'message': 'Subcategory not found', 'success': 0}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Handle any other exceptions
            return Response({'message': f'An error occurred: {str(e)}', 'success': 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class review_api(GenericAPIView):
    serializer_class=ReviewSerializer

    def post(self,request):
        productname=""
        productid=request.data.get('productid')
        username=""
        userid=request.data.get('userid')
        reviewdescription=request.data.get('reviewdescription')
        product_data=Product.objects.filter(id=productid).values()
        for i in product_data:
            productname=i['productname']
            print(productname)
        user_data=Registration.objects.filter(login_id=userid).values()
        print(user_data)
        for i in user_data:
            username=i['name']
            print(username)
        serializer=self.serializer_class(data={'productid':productid,'userid':userid,'productname':productname,'name':username,'reviewdescription':reviewdescription})
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'review add successfully','success':1},status=status.HTTP_200_OK)
        return Response({'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)  

class viewreview_api(GenericAPIView):
    serializer_class=ReviewSerializer
    def get(self,request):
        user=Review.objects.all()
        if (user.count()>0):
            serializer=ReviewSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)

class viewsinglereview_api(GenericAPIView):
    serializer_class=ReviewSerializer
    def get(self,request,id):
        user=Review.objects.get(pk=id)
        serializer=ReviewSerializer(user)
        return Response(serializer.data)

class deletereview_api(GenericAPIView):
    serializer_class=ReviewSerializer
    def delete(self,request,id):
        user=Review.objects.get(pk=id)
        user.delete()
        return Response({'message':'user deleted','success':True},status=status.HTTP_200_OK)

class updatereview_api(GenericAPIView):
    serializer_class=ReviewSerializer
    def put(self,request,id):
        user=Review.objects.get(pk=id)
        print(user)
        serializer=ReviewSerializer(instance=user,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)

class addcart_api(GenericAPIView):
    serializer_class=CartSerializer

    def post(self,request):
        productid=request.data.get('productid')
        userid=request.data.get('userid')
        cart_status=1
        quantity=1
        cart=Cart.objects.filter(productid=productid,userid=userid)
        if cart.exists():
           return Response({'message':'item already exist','success':False},status=status.HTTP_400_BAD_REQUEST)
        product_data=Product.objects.filter(id=productid).first()
        if not product_data:
           return Response({'message':'product not found','success':False},status=status.HTTP_400_BAD_REQUEST)
        productname=product_data.productname
        price=product_data.price
        image=product_data.image
        description=product_data.description
        total_price=price*quantity
        print(total_price)
        serializer=self.serializer_class(data={
        'productid':productid,
        'userid':userid,
        'productname':productname,
        'price':price,
        'description':description,
        'quantity':quantity,
        'cart_status':cart_status,
        'image':image
        })
        if serializer.is_valid():
          serializer.save()
          return Response({'data': serializer.data, 'message': 'added to cart successfully', 'success': 1}, status=status.HTTP_200_OK)
        else:
          print(serializer.errors) 

class viewcart_api(GenericAPIView):
    serializer_class=CartSerializer
    def get(self,request):
        user=Cart.objects.all()
        if (user.count()>0):
            serializer=CartSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST)

class deletecart_api(GenericAPIView):
    serializer_class=CartSerializer
    def delete(self,request,id):
        user=Cart.objects.get(pk=id)
        user.delete()
        return Response({'message':'user deleted','success':True},status=status.HTTP_200_OK)

class viewsinglecart_api(GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request, userid):
        cart_items = Cart.objects.filter(userid=userid)
        if cart_items.exists():
            serializer = CartSerializer(cart_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No cart items found for the user', 'success': 0}, status=status.HTTP_404_NOT_FOUND)

class addwishlist_api(GenericAPIView):
    serializer_class = WishlistSerializer

    def post(self, request):
        productid = request.data.get('productid')
        userid = request.data.get('userid')
        wishlist_status = 1
        wishlist = Wishlist.objects.filter(productid=productid, userid=userid)
        if wishlist.exists():
            wishlist.delete()
            return Response({'message': 'remove from wishlist', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        product_data = Product.objects.filter(id=productid).first()
        if not product_data:
            return Response({'message': 'product not found', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        productname = product_data.productname
        price = product_data.price
        image = product_data.image
        description=product_data.description

        serializer = self.serializer_class(data={
            'productid': productid,
            'userid': userid,
            'description':description,
            'productname': productname,
            'price': price,
            'wishlist_status': wishlist_status,
            'image': image,
             })
        
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'added to wishlist successfully', 'success': 1}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class viewwishlist_api(GenericAPIView):
    serializer_class=WishlistSerializer
    def get(self,request):
        user=Wishlist.objects.all()
        print(user)
        if (user.count()>0):
            serializer=WishlistSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':[]},status=status.HTTP_200_OK)

class order_api(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, userid):
        cart_items = Cart.objects.filter(userid=userid, cart_status=1)
        if cart_items.exists():
            orders = []
            for item in cart_items:
                order_data = {
                    'productid': item.productid,
                    'productname': item.productname,
                    'image': item.image,
                    'userid': item.userid,
                    'price': item.price,
                    'quantity': item.quantity,
                    
                }

                
                serializer = self.serializer_class(data=order_data)
                if serializer.is_valid():
                    
                    serializer.save()
                    orders.append(serializer.data)
                else:
                    
                    return Response({'message': 'Order creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

           
            cart_items.delete()

            return Response({'data': orders, 'message': 'Order placed successfully', 'success': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items in cart', 'success': 0}, status=status.HTTP_400_BAD_REQUEST)

    

class OrderViewApi(GenericAPIView):
    serializer_class = OrderSerializer
    def get(self, request, userid):
        user_orders = Order.objects.filter(userid=userid)
        if user_orders.exists():
            serializer = self.serializer_class(user_orders, many=True)
            return Response({'data': serializer.data, 'message': 'Orders fetched successfully', 'success': 1}, status=status.HTTP_200_OK)
        return Response({'message': 'No orders found', 'success': 0}, status=status.HTTP_404_NOT_FOUND)
    

class addaddress_api(GenericAPIView):
    serializer_class=AddressSerializer
    def post(self,request):
        userid=request.data.get('userid')
        name=request.data.get('name')
        phonenumber=request.data.get('phonenumber')
        house_no=request.data.get('house_no')
        street=request.data.get('street')
        city=request.data.get('city')
        district=request.data.get('district')
        state=request.data.get('state')
        pincode=request.data.get('pincode')
        serializer=self.serializer_class(data={'userid':userid,'name':name,'phonenumber':phonenumber,'street':street,'house_no':house_no,'state':state,'district':district,'pincode':pincode,'city':city})
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data ,'message':'address added successfully','success':1},status=status.HTTP_200_OK) 
        return Response({'data':serializer.errors,'message':'failed','success':0},status=status.HTTP_400_BAD_REQUEST)

class viewaddress_api(GenericAPIView):
    serializer_class=AddressSerializer
    def get(self,request):
        user=Address.objects.all()
        if (user.count()>0):
            serializer=AddressSerializer(user,many=True)
            return Response({'data':serializer.data,'message':'data get','success':True},status=status.HTTP_200_OK)
        return Response({'data':'no data available'},status=status.HTTP_400_BAD_REQUEST) 
    
class deleteaddress_api(GenericAPIView):
    serializer_class=AddressSerializer
    def delete(self,request,userid):
        user=Address.objects.get(pk=userid)
        user.delete()
        return Response({'message':'address deleted','success':True},status=status.HTTP_200_OK)

class updateaddress_api(GenericAPIView):
    serializer_class=AddressSerializer
    def put(self,request,userid):
        user=Address.objects.get(userid=userid)
        print(user)
        serializer=AddressSerializer(instance=user,data=request.data,partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,'message':'updated successfully','success':1},status=status.HTTP_200_OK)
        

class search_api(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        search_query = request.data.get('search_query', '')
        if search_query:
        
            products = Product.objects.filter(Q(productname__exact=search_query))
            if not products:
                return Response({'message': 'No products found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.serializer_class(products, many=True)
            for product in serializer.data:
                if product['image']:
                    product['image'] = settings.MEDIA_URL + product['image']
            
            return Response({'data': serializer.data, 'message': 'Image fetched successfully'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'No query found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
     search_query = request.query_params.get('search_query', '')
     if search_query:
        products = Product.objects.filter(
            Q(productname__icontains=search_query) 
        ).values('productname').distinct()[:10] 
        
        if not products.exists(): 
              return Response({'Message': 'no suggestions found'}, status=status.HTTP_400_BAD_REQUEST)

        suggestion_list = [{'product_name': product['productname']} for product in products]
        
        return Response({'suggestion': suggestion_list, 'message': 'suggestions fetched successfully', 'success': True}, status=status.HTTP_200_OK)
     return Response({'error': 'no search query provided', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
    

class changepassword_api(GenericAPIView):
    serializer_class = LoginSerializer
    def put(self,request,id):
        try:
            user=Login.objects.get(pk=id)
        except Login.DoesNotExist:
            return Response({'message':'user not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user,data=request.data,partial=True)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('password')
            if new_password:
                user.password = new_password
                user.save()
                return Response({'message':'password updated successfully'}, status = status.HTTP_200_OK)
            else:
                return Response({'message':'no password provided'}, status = status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':'password updated failed'}, status = status.HTTP_400_BAD_REQUEST)
    
         
