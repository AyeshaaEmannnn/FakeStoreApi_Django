from django.shortcuts import render
from .models import *
from  rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView,ListAPIView
# Create your views here.

class ProductView(APIView):
    def get(self,request):
        data=Product.objects.all()
        serializer=ProductSerializer(data,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=404)
    
    def put(self, request):
        item_id=request.data.get('id')
        if not item_id:
            return Response({'error:id not found'},status=404)
        items=get_object_or_404(Product,id=item_id)
        serializer=ProductSerializer(items,data=request.data)
        if serializer .is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=404)
    
    def patch(self, request):
        item_id=request.data.get('id')
        if not item_id:
            return Response({'error:id not found'},status=404)
        items=get_object_or_404(Product,id=item_id)
        serializer=ProductSerializer(items,data=request.data,partial=True)
        if serializer .is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=404)
    
    def delete(self,request):
        item_id=request.data.get('id')
        if not item_id:
            return Response({'error:id not found'},status=404)
        items=get_object_or_404(Product,id=item_id)
        items.delete()
        return Response({'data':'data id deleted'},status=204)
    
    
class ProductDetailView(RetrieveAPIView):    # RetrieveAPIView is a DRF generic view used to retrieve one object.
    queryset = Product.objects.all()     # queryset tells DRF where to search
    serializer_class = ProductSerializer      #	Tells the view which serializer to use for converting data
    
class ProductCategoryList(APIView):
    def get(self,request):
        categories=Product.objects.values_list('category', flat=True).distinct() #.values_list('category', flat=True) grabs just the category field from the DB.  .distinct() ensures there are no duplicates.
        return Response(categories)
    
class ProductsByCategory(ListAPIView):  #ListAPIView is a DRF generic view for listing multiple objects.
    serializer_class = ProductSerializer

    def get_queryset(self):                #get_queryset() customizes which products to show:
        category = self.kwargs['category']           #It grabs the category from the URL (e.g., "jewellery").
        return Product.objects.filter(category__iexact=category) # __iexact (case-insensitive) to filter matching category products.
    
# retriveAPIview ham tab use kare gy jab koi aik object retrive karna hoga queryset btata hy k kis jga search hogi us object k liye or wo hmary model k tamam objects my search kare ga  and serializer_class btati hy views ko k kis serializer ko use karna hy data k liye
# next categorylist k liye ham aik get ki api bna rahy hain data ko show krny k liye categories aik variable hy jismy hmary models k objects my sy aik list aae gi jo list categories ki hogi. flat=True gives a list instead of tuple .distinct function kesi bhi value ko repeat hony sy rokta hy
# listAPIview hame multiple objects ko list krny my help karta hy class_serializer btae ga k konsa serializer my sy data use krna then queryset function customize kre ga k konsy objects show hon gy category variable hy jo url my sy category ko store karee ga product.objects.filter ye filter kree ga sab rows ko or matching rows show kare ga category hmari database ki field hy or iexact case insensitive bnaee ga usko


class SignupView(APIView):
    def post(self,request):
        serializer=SingupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=404)
    
class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
           user=serializer.validated_data['user']
           return Response({'message':'Login successfully','username':user.username},status=200)
        return Response(serializer.errors,status=404)
    
class CartCreateView(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            cart = serializer.save()     #calls the create() method,Extracts userId and products from the input JSON.Creates a new Cart.Creates related CartItem
            return Response(CartSerializer(cart).data, status=201)  #Serialize the cart again using CartSerializer(cart) — this turns it into JSON.
                                                                    #.data returns the serialized dictionary.
        return Response(serializer.errors, status=400)
    def get(self,request):
        data=Cart.objects.all()
        serializer=CartSerializer(data,many=True)
        return Response(serializer.data)

class CartQueryView(APIView):
    def get(self, request):
        user_id = request.query_params.get('userId')  # Get the user id from query string
        if not user_id:
            return Response({"error": "userId is required in query params"}, status=400)

        carts = Cart.objects.filter(user_id=user_id) #matches the user id
        if not carts.exists():
            return Response({"message": "No cart found for this user"}, status=404)

        serializer = CartSerializer(carts, many=True) # return all carts of spaecific user
        return Response(serializer.data, status=200)


class ProductListView(APIView):
    def get(self, request):
        limit = request.query_params.get('limit')
        try:
            if limit:
                limit = int(limit)
                products = Product.objects.all()[:limit]
            else:
                products = Product.objects.all()
        except ValueError:
            return Response({"error": "limit must be an integer"}, status=400)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)

