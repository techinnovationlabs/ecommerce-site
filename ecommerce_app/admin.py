from django.contrib import admin
from .models import *
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    search_fields = ['name']
    list_filter = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.image.url))

    image_tag.short_description = 'Product Image Preview'
    readonly_fields = ['image_tag']


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)

admin.site.site_header = "E-Store Dashboard"
admin.site.site_title = "E-Store"
admin.site.index_title = "Welcome to E-Store Dashboard"
