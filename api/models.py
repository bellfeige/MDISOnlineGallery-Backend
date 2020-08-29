from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from PIL import Image


class User(AbstractUser):
    is_designer = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'

    def get_user_role(self):
        if self.is_superuser and not self.is_designer and not self.is_member:
            return 0
        elif self.is_designer and not self.is_superuser and not self.is_member:
            return 1
        elif self.is_member and not self.is_designer and not self.is_superuser:
            return 2

    def get_user_role_str(self):
        if self.is_superuser and not self.is_designer and not self.is_member:
            return 'Administrator'
        elif self.is_designer and not self.is_superuser and not self.is_member:
            return 'Designer'
        elif self.is_member and not self.is_designer and not self.is_superuser:
            return 'Member'


class DesignerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='designer_profile')
    avatar = models.ImageField(default='avator.png', upload_to=f"desginer_avatar", null=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username}_profile'

    def get_username(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(DesignerProfile, self).save(*args, **kwargs)

        ava = Image.open(self.avatar.path)
        rgb_ava = ava.convert('RGB')

        if rgb_ava.height > 400 or rgb_ava.width > 400:
            output_size = (400, 400)
            rgb_ava.thumbnail(output_size)
            rgb_ava.save(self.avatar.path)


class MDISMember(models.Model):
    member_id = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.member_id}_{self.email}'

        # class Meta:
    #     unique_together = (("member_id", "email"),)
    #     index_together = (("member_id", "email"),)


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)

    # description = models.TextField(max_length=300, null=True)

    def __str__(self):
        return self.name


class DigitalArt(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='digital_art_category')
    file = models.FileField(upload_to='downloading', blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    def get_file_path(self):
        return self.file.path

    def rating_average(self):
        sum = 0
        ratings = RatingComment.objects.filter(digital_art=self)
        for rating in ratings:
            sum = sum + rating.star
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0

    def comments_list(self):
        allcomments = RatingComment.objects.filter(digital_art=self)
        listallcomments = []
        for comment in allcomments:
            # print(comment.comments)
            listallcomments.append(comment.comment)
        return listallcomments


# def get_preview_image_path():
#     now = datetime.now()
#     ts = datetime.now().timestamp()
#     return f'{now.strftime("%Y%m%d%H%M")}_{str(ts)[-1:-5:-1]}'


class DigitalArtPreviewImg(models.Model):
    digital_art = models.ForeignKey(DigitalArt, on_delete=models.CASCADE, blank=False, null=False,
                                    related_name='previewImgs')
    image_sequence = models.PositiveSmallIntegerField(null=True)
    image = models.ImageField(default='blank.png', upload_to='preview_imgs/%Y%m%d%H%M%S/')

    def __str__(self):
        return f"{self.digital_art.title}{self.image_sequence}"

    # def get_image_path_name(self):
    #     pass

    def save(self, *args, **kwargs):
        super(DigitalArtPreviewImg, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        rgb_ava = image.convert('RGB')

        if rgb_ava.height > 400 or rgb_ava.width > 400:
            output_size = (400, 400)
            rgb_ava.thumbnail(output_size)
            rgb_ava.save(self.image.path)


class RatingComment(models.Model):
    digital_art = models.ForeignKey(DigitalArt, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.IntegerField()
    comment = models.TextField(max_length=300)

    class Meta:
        unique_together = (("user", "digital_art"),)
        index_together = (("user", "digital_art"),)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digital_art = models.ForeignKey(DigitalArt, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}_{self.digital_art.title}'

    # def price_in_total(self):
    #     price_in_total = 0
    #     order_das = DigitalArt.objects.filter(order=self)
    #     for order_da in order_das:
    #         price_in_total = price_in_total + order_da.get_price()
    #     return price_in_total


# class OrderStatus(models.Model):
#     name = models.CharField(max_length=50, blank=False, null=False)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_user')
    # status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20)
    # price_in_all = models.FloatField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def price_in_total(self):
        price_in_total = 0
        order_das = OrderDigitalArt.objects.filter(order=self)
        for order_da in order_das:
            price_in_total = price_in_total + order_da.get_price()
        return price_in_total

    def __str__(self):
        return f'{self.id} by {self.user.username}'


class OrderDigitalArt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_digital_art')
    digital_art = models.ForeignKey(DigitalArt, on_delete=models.SET_NULL, null=True, related_name='ODA_digital_art')

    # title = models.CharField(max_length=50)
    # download_url = models.URLField()
    # price = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f'{self.order}_{self.digital_art}'

    def get_title(self):
        title = self.digital_art.title
        return title

    def get_download_url(self):
        if self.order.status == 'Completed':
            download_url = str(self.digital_art.file)
            return download_url
        else:
            return ''

    def get_price(self):
        price = self.digital_art.price
        return price
