from rest_framework import viewsets, status
from .models import User, DigitalArt, RatingComment, DigitalArtPreviewImg, MDISMember, Category, Cart, Order, \
    OrderDigitalArt
from .serializers import DigitalArtSerializer, RatingSerializer, UserSerializer, AdminSerializer, MDISMemberSerializer, \
    CategorySerializer, CartSerializer, OrderSerializer, CategorySerializer, ProfileSerializer
from .permissions import IsDigitalArtOwnerOrAdmin, IsCurrentUserOrAdmin, IsAdminAndOnly, IsMyCartOrAdmin
from .hashers import hashed_password
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.views import APIView
import json


# submittedStatus = 1
# completedStatus = 2
# cancelledStatus = 3
#
#
# def order_status_value(index):
#     with open('api\orderStatus.json', 'r') as f:
#         order_status = json.load(f)
#
#     # for status in order_status:
#     #     # print(status)
#     #     print(status['Value'])
#     #     print(status['Status'])
#
#     if index <= 3:
#         return order_status[index - 1]['Status']
#     else:
#         return ''


class DigitalArtViewSet(viewsets.ModelViewSet):
    queryset = DigitalArt.objects.all().order_by('-created_at')
    serializer_class = DigitalArtSerializer
    authentication_classes = (TokenAuthentication,)
    parser_class = (FileUploadParser, MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            # if self.request.method == 'GET' or 'HEAD' or 'OPTIONS':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsDigitalArtOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        title = self.request.data["title"]
        description = self.request.data["description"]
        category = Category.objects.get(id=self.request.data["category"])
        price = self.request.data["price"]
        owner = self.request.user
        file = self.request.data["file"]
        # previewImg0 = self.request.data["previewImg0"]
        previewImgsCount = self.request.data["previewImgsCount"]
        if int(previewImgsCount) > 6:
            response = {"message": "No more than 6 images"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if self.request.user.is_authenticated:
            newDigitalArt = DigitalArt.objects.create(title=title, description=description,
                                                      category=category,
                                                      price=price, owner=owner, file=file)

            if newDigitalArt.id:
                if previewImgsCount == 0:
                    DigitalArtPreviewImg.objects.create(digital_art=newDigitalArt)
                else:
                    for i in range(int(previewImgsCount)):
                        DigitalArtPreviewImg.objects.create(digital_art=newDigitalArt, image_sequence=i,
                                                            image=self.request.data[f"previewImg{i}"])
            serializer = DigitalArtSerializer(newDigitalArt)
            response = {"message": "New product created",
                        "data": serializer.data}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {"message": "Product failed to be created, due to not authenticated"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None, *args, **kwargs):
        digital_art = DigitalArt.objects.get(id=pk)
        title = self.request.data["title"]
        description = self.request.data["description"]
        category = Category.objects.get(id=self.request.data["category"])
        price = self.request.data["price"]

        if "file" in request.data:
            file = self.request.data["file"]
        else:
            file = digital_art.file
        previewImgsCount = self.request.data["previewImgsCount"]
        if int(previewImgsCount) > 6:
            response = {"message": "No more than 6 images"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user.is_authenticated:
            try:
                digital_art.title = title
                digital_art.description = description
                # if 'category' in self.request.data:
                digital_art.category = category
                digital_art.price = price
                digital_art.file = file
                digital_art.save()

                if int(previewImgsCount) > 0:
                    DigitalArtPreviewImg.objects.filter(digital_art=digital_art).delete()

                    if not DigitalArtPreviewImg.objects.filter(digital_art=digital_art).exists():
                        for i in range(int(previewImgsCount)):
                            DigitalArtPreviewImg.objects.create(digital_art=digital_art, image_sequence=i,
                                                                image=self.request.data[f"previewImg{i}"])

                serializer = DigitalArtSerializer(digital_art, many=False)
                response = {
                    "message": "Product has been updated",
                    "result": serializer.data,
                }
                return Response(response, status=status.HTTP_200_OK)
            except:
                response = {"message": "Failed to update"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {"message": "Product failed to be updated, not authenticated"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(methods=["POST"], detail=True)
    def rate(self, request, pk=None):
        if "stars" in request.data:
            digital_art = DigitalArt.objects.get(id=pk)
            star = request.data["star"]
            comment = request.data["comment"]
            user = request.user
            try:
                rating = RatingComment.objects.get(user=user.id, digital_art=digital_art.id)
                rating.stars = star
                rating.comments = comment
                rating.save()

                serializer = RatingSerializer(rating, many=False)
                response = {
                    "message": "rating has been updated",
                    "result": serializer.data,
                }
                return Response(response, status=status.HTTP_200_OK)

            except:
                rating = RatingComment.objects.create(
                    user=user, digital_art=digital_art, star=star, comment=comment
                )
                serializer = RatingSerializer(rating, many=False)
                response = {"message": "rating created",
                            "result": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = {"message": "Please enter stars for the rating"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class MyDigitalArtViewSet(viewsets.ModelViewSet):
    # queryset = DigitalArt.objects.all().order_by('-created_at')
    serializer_class = DigitalArtSerializer
    authentication_classes = (TokenAuthentication,)

    # parser_class = (FileUploadParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return DigitalArt.objects.filter(owner=self.request.user)

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsDigitalArtOwnerOrAdmin]
        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)

    # http_method_names = ['get', 'post', 'head', 'options', 'put', 'delete', 'patch']

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            # if self.request.method == 'GET' or 'HEAD' or 'OPTIONS':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminAndOnly]
        return [permission() for permission in permission_classes]


class RatingCommentViewSet(viewsets.ModelViewSet):
    queryset = RatingComment.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        response = {"message": "Rating cannot be updated like this"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {"message": "Rating cannot be created like this"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (AllowAny,)
    # http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        elif self.request.method == 'POST' and 'is_superuser' in self.request.data:
            permission_classes = [IsAuthenticated, IsAdminAndOnly]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsAdminAndOnly]
        else:
            permission_classes = [IsAuthenticated, IsCurrentUserOrAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_superuser = False
        is_designer = False
        is_member = False
        if 'is_superuser' in request.data:
            is_superuser = self.request.data['is_superuser']
        if 'is_designer' in request.data:
            is_designer = self.request.data['is_designer']
        if 'is_member' in request.data:
            is_member = self.request.data['is_member']
        username = self.request.data['username']

        if is_member or is_superuser:
            try:
                MDISMember.objects.get(member_id=username)
            except MDISMember.DoesNotExist:
                print("This username is already existed")
            else:
                response = {"message": "This username already exists"}
                return Response(response, status=status.HTTP_409_CONFLICT)

        if is_designer:
            try:
                email = self.request.data['email']
                MDISMember.objects.get(member_id=username, email=email)
            except MDISMember.DoesNotExist:
                response = {"message": "Incorrect MDIS Member id or Email address"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {"message": "User Created",
                    "result": serializer.data}
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = hashed_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    # def partial_update(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        # Hash password but passwords are not required
        password = hashed_password(self.request.data['password'])
        print(password)
        serializer.save(password=password)
        # if 'password' in self.request.data:
        #     password = hashed_password(self.request.data['password'])
        #     serializer.save(password=password)
        # else:
        #     # password = hashed_password(self.request.data['password'])
        #     # serializer.save(password=password)
        #     serializer.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get', 'head', 'options', 'patch']

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)

    def get_serializer_class(self):
        return ProfileSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]


class UserAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'full_name': user.get_full_name(),
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_designer': user.is_designer,
            'is_member': user.is_member,
            'get_user_role': user.get_user_role(),
            'get_user_role_str': user.get_user_role_str()
        })


class CurrentUserView(APIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MDISMemberViewSet(viewsets.ModelViewSet):
    queryset = MDISMember.objects.all()
    serializer_class = MDISMemberSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminAndOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (IsAuthenticated, IsAdminOnly,)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            # if self.request.method == 'GET' or 'HEAD' or 'OPTIONS':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminAndOnly]
        return [permission() for permission in permission_classes]


class CartViewSet(viewsets.ModelViewSet):
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMyCartOrAdmin)
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        digital_art = DigitalArt.objects.get(id=self.request.data["digital_art"])
        user = self.request.user
        if self.request.user.is_authenticated:
            if not Cart.objects.filter(user=user, digital_art=digital_art).exists():
                Cart.objects.create(user=user, digital_art=digital_art)
                response = {"message": "Added to cart",
                            "result": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {"message": "This product is already in your cart"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {"message": "Login required"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)


class OrderViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsMyCartOrAdmin)

    # http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Order.objects.all().order_by('-created_at')
            return queryset
        else:
            queryset = Order.objects.filter(user=self.request.user.id).order_by('-created_at')
            return queryset

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return OrderSerializer
        else:
            return OrderSerializer

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        cart = Cart.objects.filter(user=self.request.user.id)
        user = self.request.user
        submittedStatus = 'Submitted'
        if self.request.user.is_authenticated:
            if 'digital_art' in self.request.data:
                # digital_art = self.request.data["digital_art"]
                digital_art = DigitalArt.objects.get(pk=self.request.data["digital_art"])
                newOrder = Order.objects.create(user=user, status=submittedStatus)
                if newOrder.id:
                    OrderDigitalArt.objects.create(order=newOrder, digital_art=digital_art)
                serializer = OrderSerializer(newOrder)
                response = {"message": "Order placed",
                            "result": serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                if cart.exists():
                    newOrder = Order.objects.create(user=user, status=submittedStatus)
                    if newOrder.id:
                        for product in cart:
                            OrderDigitalArt.objects.create(order=newOrder, digital_art=product.digital_art)
                        if OrderDigitalArt.objects.filter(order=newOrder.id).exists():
                            Cart.objects.filter(user=user).delete()
                        serializer = OrderSerializer(newOrder)
                        response = {"message": "Order placed",
                                    "result": serializer.data}
                        return Response(response, status=status.HTTP_201_CREATED)

                else:
                    response = {"message": "Your cart is empty"}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {"message": "Login required"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

    # def update(self, request, pk=None, *args, **kwargs):
    #     order = Order.objects.get(id=pk)
    #     # paid cancelled unpaid
    #     # order_action = self.request.data["order_action"]
    #     # if self.request.user.is_authenticated:
    #     message = ''
    #     order.status = order_status_value(completedStatus)
    #     message = 'Paid successfully, order completes'
    #     # try:
    #     # if order_action == 'paid':
    #     #     order.status = order_status_value(completedStatus)
    #     #     message = 'Paid successfully, order completes'
    #     # elif order_action == 'cancelled':
    #     #     order.status = order_status_value(cancelledStatus)
    #     #     message = 'Order cancelled'
    #     # else:
    #     #     order.status = order.status
    #     #     message = 'Payment not successful'
    #
    #     serializer = DigitalArtSerializer(order, many=False)
    #     response = {
    #         "message": message,
    #         "result": serializer.data,
    #     }
    #     return Response(response, status=status.HTTP_200_OK)
    #     # except:
    #     #     response = {"message": "Unable to process"}
    #     #     return Response(response, status=status.HTTP_400_BAD_REQUEST)
    #
    #     # else:
    #     #     response = {"message": "Login required"}
    #     #     return Response(response, status=status.HTTP_403_FORBIDDEN)
