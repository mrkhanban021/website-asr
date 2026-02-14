from django.db import models
from identify.models import BaseModel
from django.utils.text import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


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


class Usage(BaseModel):

    title = models.CharField(
        max_length=100,
        unique=True,
        help_text="عنوان کاربرد (مسکونی، تجاری، بیمارستانی)"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_time',)


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

    description = models.TextField(
        null=True,
        blank=True,
        help_text='توضیح مختصر'
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
        help_text='عنوان واحد اندازه‌گیری (مثلاً سانتی‌متر)',
        unique=True
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

    class BerandType(models.TextChoices):
        RADPLUS = 'radplus', 'رادپلاس'
        SELECOMPLUS = 'selecom_plus', 'سلکوم پلاس'
        HALFSELECOM = 'half_selcom', 'نیمه سلکوم'
        ASR = 'asr', 'آریان سیستم رو'

    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='نام کلی محصول'
    )

    slug = models.SlugField(unique=True, allow_unicode=True,
                            null=True, blank=True, help_text='اسلاگ فیلد')

    category = models.ManyToManyField(
        Categories,
        related_name='products',
        help_text='دسته‌بندی‌های محصول'
    )

    berand = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=BerandType.choices,
        help_text='برند محصول'
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

    like = models.ManyToManyField(
        User, blank=True, help_text='کاربران کاربران که لایک کردن', related_name='like_product')
    un_like = models.ManyToManyField(
        User, blank=True, help_text='کاربران دیس لایک کرده اند', related_name='unlike_product')

    def get_like(self):
        return self.like.count()

    def get_unlike(self):
        return self.un_like.count()

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.title)

        super().save(*args, **kwargs)


class Door(BaseModel):
    class OpeningType(models.TextChoices):
        CENTRAL = 'Central', 'سانترال'
        TELESCOPIC = 'telescopic', 'تلسکوپی'

    class DirectionOpening(models.TextChoices):
        LEFT = 'left', 'چپ باز شو'
        RIGHT = 'right', 'راست باز شو'
        MID = 'mid', 'وسط باز شو'

    LEAF_CHOICES = (
        (1, "تک‌لته"),
        (2, "دولته"),
        (3, "سه‌لته"),
        (4, "چهارلته"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='details',
        help_text='محصول مرتبط'
    )

    title = models.CharField(
        max_length=100,
        null=True, blank=True,
        help_text='نام دقیق محصول'
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

    usage = models.ManyToManyField('Usage', blank=True, help_text='کاربرد ها')

    leaf_count = models.PositiveSmallIntegerField(
        choices=LEAF_CHOICES,
        help_text="تعداد لته",
        null=True,
        blank=True
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
        help_text='توضیحات تکمیلی محصول',
        max_length=1000
    )

    slug = models.SlugField(unique=True, allow_unicode=True,
                            null=True, blank=True, help_text='اسلاگ فیلد')

    class Meta:
        ordering = ('-created_time',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Door, self.title)

        super().save(*args, **kwargs)


class SparePart(BaseModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="spare_parts",
        help_text="محصولی که این قطعه مربوط به آن است"
    )

    title = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='عنوان قطعه یدکی'
    )

    code = models.CharField(
        max_length=100,
        unique=True,
        help_text="کد قطعه یدکی"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="وضعیت فعال بودن قطعه"
    )

    slug = models.SlugField(unique=True, allow_unicode=True,
                            null=True, blank=True, help_text='اسلاگ فیلد')

    description = models.TextField(
        blank=True,
        help_text='توضیحات تکمیلی محصول',
        max_length=1000
    )

    def __str__(self):
        return f"{self.title} - {self.product.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Door, self.title)

        super().save(*args, **kwargs)


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
    length = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='طول'
    )

    class Meta:
        ordering = ('-created_time',)

    @property
    def height_display(self):
        return f"{self.height}{self.unit.symbol}"
    
    @property
    def length_display(self):
        return f"{self.length}{self.unit.symbol}"
    
    @property
    def width_display(self):
        return f"{self.width}{self.unit.symbol}"

    def __str__(self):
        if self.width and self.height:
            return f"عرض({self.width})×ارتفاع({self.height}) {self.unit}"
        if self.length:
            return f"طول-({self.length}{self.unit})"
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
    is_active = models.BooleanField(
        default=True,
        help_text='فعال بودن'
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
        related_name='catalog_files',
        help_text='محصول مربوطه'
    )

    file = models.FileField(
        upload_to=upload_product_images,
        help_text='تصویر محصول',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True,
        help_text='فعال بودن'
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


class ProductComment(BaseModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="محصول مربوطه"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="کاربر ثبت‌نام شده"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="کامنت والد (برای ریپلای)"
    )

    full_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="نام ارسال‌کننده (برای کاربران مهمان)"
    )

    text = models.TextField(
        help_text="متن نظر",
        max_length=1000
    )

    is_approved = models.BooleanField(
        default=False,
        help_text="آیا توسط ادمین تأیید شده؟"
    )

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        if not self.full_name:
            return f"{self.product.title}"
        return f"{self.full_name} - {self.product.title}"

    @property
    def display_name(self):
        if self.full_name:
            return self.full_name

        if self.user:
            try:
                return f"{self.user.user_profile.first_name} {self.user.user_profile.last_name}" or self.full_name  # type: ignore
            except Exception:
                return self.full_name

        return "کاربر مهمان"
    


    def save(self, *args, **kwargs):
        if not self.full_name:
            if self.user:
                first_name = getattr(self.user.user_profile, 'first_name', 'کاربر')
                last_name = getattr(self.user.user_profile, 'last_name', 'بدون نام')
                self.full_name = f"{first_name} {last_name}"
            self.full_name = f"کاربر بدون نام"
        super().save(*args, **kwargs)