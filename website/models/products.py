from django.db import models
from identify.models import BaseModel
from django.utils.text import slugify


def upload_product_images(instance, filename):
    if instance.product_id:  # اطمینان از وجود محصول
        product_slug = slugify(instance.product.title, allow_unicode=True)
        return f"products/{product_slug}/{filename}"
    return f"products/temp/{filename}"


def generate_unique_slug(model, field_value):
    base_slug = slugify(field_value, allow_unicode=True)
    slug = base_slug
    counter = 1
    while model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


class Categories(BaseModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text='دسته‌بندی والد'
    )

    title = models.CharField(
        max_length=50,
        unique=True,
        help_text='عنوان دسته‌بندی'
    )

    slug = models.SlugField(
        allow_unicode=True,
        unique=True,
        blank=True,
        help_text='اسلاگ برای URL دسته‌بندی'
    )

    image = models.ImageField(
        upload_to='categories',
        null=True,
        blank=True,
        help_text='تصویر دسته‌بندی'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='فعال / غیرفعال'
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Categories, self.title)
        super().save(*args, **kwargs)


class Unit(BaseModel):
    title = models.CharField(
        max_length=50,
        help_text='عنوان واحد اندازه‌گیری (مثلاً سانتی‌متر)'
    )

    symbol = models.CharField(
        max_length=20,
        help_text='نماد واحد (cm, mm, kg)'
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.symbol


class Product(BaseModel):

    class ProductType(models.TextChoices):
        DOOR = 'door', 'درب آسانسور'
        SPARE = 'spare', 'قطعه یدکی'

    category = models.ManyToManyField(
        Categories,
        related_name='products',
        help_text='دسته‌بندی‌های محصول'
    )

    title = models.CharField(
        max_length=120,
        unique=True,
        help_text='نام محصول'
    )

    slug = models.SlugField(
        allow_unicode=True,
        unique=True,
        blank=True,
        help_text='اسلاگ محصول برای URL'
    )

    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        help_text='نوع محصول'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='فعال / غیرفعال'
    )


    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.title)

        super().save(*args, **kwargs)


class ProductDetails(BaseModel):
    class OpeningType(models.TextChoices):
        CENTRAL = 'Central', 'سانترال'
        TELESCOPIC = 'telescopic', 'تلسکوپی'

    class DirectionOpening(models.TextChoices):
        LEFT = 'left', 'چپ'
        RIGHT = 'right', 'راست'
        MID = 'mid', 'وسط'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='details',
        help_text='محصول مرتبط'
    )

    color = models.ForeignKey(
        'Color',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='رنگ محصول'
    )

    size = models.ForeignKey(
        'Size',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='ابعاد محصول'
    )

    opening_type = models.CharField(
        max_length=50,
        blank=True,
        choices=OpeningType.choices,
        help_text='نوع بازشو (سانترال، تلسکوپی و …)'
    )

    direction_opening = models.CharField(
        max_length=50,
        choices=DirectionOpening.choices,
        help_text='جهت باز شو',
        null=True,
        blank=True
    )

    material = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='جنس متریال'
    )
    
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        help_text='عنوان سئو (Google Title)'
    )

    meta_description = models.CharField(
        max_length=160,
        blank=True,
        null=True,
        help_text='توضیحات سئو (Meta Description)'
    )
    
    
    usage = models.CharField(
        max_length=100,
        blank=True,
        help_text='کاربرد (مسکونی، تجاری، بیمارستانی)'
    )

    fire_resistant = models.BooleanField(
        default=False,
        help_text='مقاوم در برابر حریق'
    )

    has_sensor = models.BooleanField(
        default=False,
        help_text='دارای سنسور ایمنی'
    )

    description = models.TextField(
        blank=True,
        help_text='توضیحات تکمیلی محصول'
    )

    class Meta:
        ordering = ('-created_time',)


class Color(BaseModel):
    title = models.CharField(
        max_length=50,
        help_text='نام رنگ'
    )

    code = models.CharField(
        max_length=20,
        help_text='کد رنگ (HEX یا نام)'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='فعال / غیرفعال'
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title


class Size(BaseModel):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        help_text='واحد اندازه‌گیری'
    )

    width = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text='عرض'
    )

    height = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text='ارتفاع'
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        if self.width and self.height:
             return f"{self.width}×{self.height}"
        return "نامشخص"


class ProductImages(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        help_text='محصول مربوطه'
    )

    image = models.ImageField(
        upload_to=upload_product_images,
        help_text='تصویر محصول'
    )

    is_primary = models.BooleanField(
        default=False,
        help_text='تصویر اصلی'
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_file = ProductImages.objects.get(pk=self.pk)
                if old_file.image and old_file.image != self.image:
                    old_file.image.delete(save=False)
            except ProductImages.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class CatalogProduct(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='catalog_files',  # اصلاح شد
        help_text='محصول مربوطه'
    )

    file = models.FileField(
        upload_to=upload_product_images,
        help_text='تصویر محصول',
        null=True,
        blank=True
    )

    is_primary = models.BooleanField(
        default=False,
        help_text='تصویر اصلی'
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_file = CatalogProduct.objects.get(pk=self.pk)
                if old_file.file and old_file.file != self.file:
                    old_file.file.delete(save=False)
            except CatalogProduct.DoesNotExist:
                pass
        super().save(*args, **kwargs)
