from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()   #read-only field computed by custom method

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'category', 'image', 'rating']

    def get_rating(self, obj):   # When the serializer outputs JSON, this method is called for the rating field.It returns a dictionary containing the product's rate and count
        return {
            'rate': obj.rate,
            'count': obj.count
        }
    def create(self, validated_data):
        # Extract 'rating' from the input data
        rating_data = self.initial_data.get('rating', {})
        rate = rating_data.get('rate')
        count = rating_data.get('count')

        # Add 'rate' and 'count' manually to validated_data
        validated_data['rate'] = rate
        validated_data['count'] = count

        return Product.objects.create(**validated_data)
    
#     self.initial_data gives the raw input JSON data.
# It extracts the rating dict from the input (which normally would be ignored because rating is read-only).
# Pulls out rate and count from the rating.
# Adds these values into validated_data so they can be saved in the model.
# Creates a new Product instance using Product.objects.create(...).


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
    productId = serializers.IntegerField(source='product.id')  #productid name show hoga or product.id the actual path
                                                                #where it comes from

    class Meta:
        model = CartItem
        fields = ['productId', 'quantity']
        
class CartSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id')                 #same as above
    date = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.000Z',read_only=True)  #automatic add when object is  
                                                                                        # created 
    products = CartItemSerializer(many=True)              # products feild my opr wala serializer ae ga or many=True agr aik ay zyda hue to unko bi jsaon my karee ga
    _v = serializers.SerializerMethodField()            # ye method feild sy aae ga 
    
    class Meta:
        model = Cart
        fields = ['id', 'userId', 'date', 'products', '_v'] 

    def get__v(self, obj):              #to get v
        return 0
    
    def create(self, validated_data):
      user_id = validated_data['user']['id']           # validated_data['user'] comes from source='user.id' in the    
                                                    #serializer.This gets the actual user ID from the nested input and stores it in user_id.
      products_data = validated_data.pop('products')  #.pop('products') removes the 'products' list from 
                                                        #validated_data and stores it separately.

      cart = Cart.objects.create(user_id=user_id)       # new Cart is created in the database for this user.        
                                                        #user_id=user_id assigns the cart to the correct user.
      for item in products_data:
        CartItem.objects.create(
            cart=cart,                              #cart=cart — link the item to the newly created cart.
            product_id=item['product']['id'],       #product_id=item['product']['id'] — extract the product ID.
            quantity=item['quantity']               #quantity=item['quantity'] — extract quantity.
        )
      return cart
