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
    
    
class ProductDetailView(RetrieveAPIView):    
    queryset = Product.objects.all()     
    serializer_class = ProductSerializer     
    
class ProductCategoryList(APIView):
    def get(self,request):
        categories=Product.objects.values_list('category', flat=True).distinct() 
        return Response(categories)
    
class ProductsByCategory(ListAPIView):  
    serializer_class = ProductSerializer

    def get_queryset(self):                
        category = self.kwargs['category']           
        return Product.objects.filter(category__iexact=category) 
    


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
            cart = serializer.save()    
            return Response(CartSerializer(cart).data, status=201)  
                                                                    
        return Response(serializer.errors, status=400)
    def get(self,request):
        data=Cart.objects.all()
        serializer=CartSerializer(data,many=True)
        return Response(serializer.data)

class CartQueryView(APIView):
    def get(self, request):
        user_id = request.query_params.get('userId')  
        if not user_id:
            return Response({"error": "userId is required in query params"}, status=400)

        carts = Cart.objects.filter(user_id=user_id) 
        if not carts.exists():
            return Response({"message": "No cart found for this user"}, status=404)

        serializer = CartSerializer(carts, many=True) 
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

