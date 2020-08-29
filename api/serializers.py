from rest_framework import serializers
from .models import User, DigitalArt, RatingComment, DigitalArtPreviewImg, MDISMember, DesignerProfile, \
    Category, Cart, Order, OrderDigitalArt
from rest_framework.authtoken.models import Token


class DigitalPreviewImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalArtPreviewImg
        fields = ("image_sequence", "image")
        # fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class DigitalArtSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.__str__')
    # owner = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=True,
    #     slug_field='get_username',
    #     # queryset=User.objects.filter(is_member=1).reverse()
    # )
    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='name',
        queryset=Category.objects.all()
    )

    previewImgs = DigitalPreviewImgSerializer(
        many=True,
        read_only=False
    )

    class Meta:
        model = DigitalArt
        # fields = "__all__"
        fields = (
            "id",
            "title",
            "description",
            "price",
            "rating_average",
            "category",
            "owner",
            "comments_list",
            # "file",
            "previewImgs",
            "created_at"
        )
        read_only_fields = ('created_at',)
        extra_kwargs = {"url": {"required": True}}

    # def to_representation(self, instance):
    #     self.fields['category'] = CategorySerializer(read_only=True)
    #     return super(DigitalArtSerializer, self).to_representation(instance)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingComment
        fields = ("id", "star", "user", "digital_art", "comment")


class DesignerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerProfile
        fields = ('avatar', 'bio')


class UserSerializer(serializers.ModelSerializer):
    # designerProfile = DesignerProfileSerializer(
    #     many=False,
    #     read_only=False,
    #     required=False
    # )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            'get_full_name',
            'is_superuser',
            'is_designer',
            'is_member',
            # 'designerProfile',
            'get_user_role',
            'get_user_role_str'
        )
        read_only_fields = ('is_superuser', 'get_user_role', 'get_full_name', 'get_user_role_str')
        extra_kwargs = {"password": {"write_only": True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     print(f"user = {user}")
    #     Token.objects.create(user=user)
    #     return user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            'get_full_name',
            'is_superuser',
            'is_designer',
            'is_member',
            'get_user_role',
            'get_user_role_str'
        )
        read_only_fields = ('get_user_role', 'get_full_name', 'get_user_role_str')
        extra_kwargs = {"password": {"write_only": True, "required": True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            'get_full_name',
            'is_superuser',

        )
        # read_only_fields = ('get_user_role', 'get_full_name', 'get_user_role_str')
        extra_kwargs = {"password": {"write_only": True, "required": True}}


class MDISMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MDISMember
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=False,
    #     slug_field='username',
    #     required=False,
    #     queryset=User.objects.filter(is_member=1)
    # )
    # digital_art = DigitalArtSerializer(
    #     many=False,
    #     read_only=False
    # )
    digital_art = serializers.ReadOnlyField(source='digital_art.title')
    digital_art_id = serializers.ReadOnlyField(source='digital_art.id')
    digital_art_price = serializers.ReadOnlyField(source='digital_art.price')

    # digital_art = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=False,
    #     slug_field='title',
    #     queryset=DigitalArt.objects.all()
    # )

    class Meta:
        model = Cart
        fields = ('id',
                  'user',
                  'digital_art',
                  'digital_art_id',
                  'digital_art_price')
        read_only_fields = ('user',)


class OrderDigitalArtSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDigitalArt
        fields = ('id',
                  'order',
                  'digital_art',
                  'get_title',
                  'get_download_url',
                  'get_price'
                  )
        read_only_fields = ('order', 'digital_art', 'get_title', 'get_download_url', 'get_price')


class OrderSerializer(serializers.ModelSerializer):
    order_digital_art = OrderDigitalArtSerializer(
        many=True,
        read_only=False
    )

    class Meta:
        model = Order
        fields = ('id',
                  'user',
                  'status',
                  'price_in_total',
                  'order_digital_art',
                  'created_at')
        read_only_fields = ('user', 'price_in_all', 'order_digital_art', 'created_at')
