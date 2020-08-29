from django.contrib import admin
from .models import User, DigitalArt, RatingComment, DigitalArtPreviewImg, DesignerProfile, MDISMember, Category, Cart, \
    Order, OrderDigitalArt

admin.site.register(User)
admin.site.register(DigitalArt)
admin.site.register(RatingComment)
admin.site.register(DigitalArtPreviewImg)
admin.site.register(DesignerProfile)
admin.site.register(MDISMember)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderDigitalArt)
