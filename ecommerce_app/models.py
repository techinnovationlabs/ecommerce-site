from django.db import models
import datetime
import uuid


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(default=0, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=600, blank=False)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name

    def get_products_by_id(cart_product_id):
        return Product.objects.filter(id__in=cart_product_id)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def does_exits(self):
        return Customer.objects.filter(email=self.email)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return str(self.id)

    def placeOrder(self):
        return self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')


class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    total = models.IntegerField()

    def __str__(self):
        return str(self.order)

    def placeOrder(self):
        self.save()


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)

# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=100, null=True)
#
#     def __str__(self):
#         return str(self.id)
#
#     @property
#     def get_cart_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total
#
#
# class OrderItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     @property
#     def get_total(self):
#         total = self.product.price * self.quantity
#         return total
#
#
# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
#     address = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     state = models.CharField(max_length=200, null=False)
#     zipcode = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.address


#
# #
# class Order(models.Model):
#         product = models.ForeignKey(Product,
#                                     on_delete=models.CASCADE)
#         customer = models.ForeignKey(Customer,
#                                      on_delete=models.CASCADE)
#         quantity = models.IntegerField(default=1)
#         price = models.IntegerField()
#         city = models.CharField(max_length=50, default='', blank=True)
#         country = models.CharField(max_length=50, default='', blank=True)
#         address = models.CharField(max_length=50, default='', blank=True)
#         phone = models.CharField(max_length=50, default='', blank=True)
#         date = models.DateField(default=datetime.datetime.today)
#         order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
#         def __str__(self):
#             return str(self.date)
#
#         def placeOrder(self):
#             self.save()
#
#         @staticmethod
#         def get_orders_by_customer(customer_id):
#             return Order.objects.filter(customer=customer_id).order_by('-date')
#
#
# class Order(models.Model):
#      order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
