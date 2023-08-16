from django.db import models

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=5)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    description = models.CharField(
        max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='products/')

    class Meta:
        verbose_name_plural = 'Products'

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.objects.all()

    def __str__(self):
        return self.name



