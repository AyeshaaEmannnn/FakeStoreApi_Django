from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()   

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'category', 'image', 'rating']

    def get_rating(self, obj):   
        return {
            'rate': obj.rate,
            'count': obj.count
        }
    def create(self, validated_data):
       
        rating_data = self.initial_data.get('rating', {})
        rate = rating_data.get('rate')
        count = rating_data.get('count')

       
        validated_data['rate'] = rate
        validated_data['count'] = count

        return Product.objects.create(**validated_data)
    



class SingupSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
        
        
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self,data):
        username=data.get('username')
        password=data.get('password')
        
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid Username")
        if user.password!=password:
            raise serializers.ValidationError("Invalid Password")
        
        data['user']=user
        return data
    
class CartItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(source='product.id')  

    class Meta:
        model = CartItem
        fields = ['productId', 'quantity']
        
class CartSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id')                
    date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.000Z',read_only=True)   
    products = CartItemSerializer(many=True)              
    _v = serializers.SerializerMethodField()            
    
    class Meta:
        model = Cart
        fields = ['id', 'userId', 'date', 'products', '_v'] 

    def get__v(self, obj):              
        return 0
    
    def create(self, validated_data):
      user_id = validated_data['user']['id']          
      products_data = validated_data.pop('products')  

      cart = Cart.objects.create(user_id=user_id)       
      for item in products_data:
        CartItem.objects.create(
            cart=cart,                             
            product_id=item['product']['id']       
            quantity=item['quantity']               
        )
      return cart
