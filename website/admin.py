from django.contrib import admin
from .models import (
    SiteSetting,
    ProductImages,
    Categories,
    Color,
    Product,
    ProductDetails,
    Size,
    Unit,
    CatalogProduct
)


# ---------- SiteSetting ----------
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone_factory', 'email', 'created_time')
    list_filter = ('site_name',)
    search_fields = ('site_name',)


# ---------- Inlines for Product ----------
class ProductDetailsInline(admin.StackedInline):
    model = ProductDetails
    can_delete = False
    readonly_fields = ('created_time', 'updated_time')
    extra = 0


class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    can_delete = False
    readonly_fields = ('created_time', 'updated_time')
    extra = 0


class CatalogProductInline(admin.StackedInline):
    model = CatalogProduct
    can_delete = False
    readonly_fields = ('created_time', 'updated_time')
    extra = 0


# ---------- Product ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_categories', 'title', 'product_type', 'is_active')
    search_fields = ('title', )
    list_filter = ('category', 'product_type', 'is_active',)
    inlines = (ProductDetailsInline, ProductImagesInline, CatalogProductInline)
    
    filter_horizontal = ('category',)

    def get_categories(self, obj):
        return ", ".join([c.title for c in obj.category.all()])
    get_categories.short_description = "دسته‌بندی‌ها"


# ---------- Categories ----------
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'is_active')
    search_fields = ('title',)
    list_filter = ('parent', 'is_active')


# ---------- ProductDetails ----------
@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'opening_type', 'direction_opening', 'color', 'size')
    search_fields = ('product__title',)
    list_filter = ('opening_type', 'direction_opening', 'fire_resistant', 'has_sensor')


# ---------- Color ----------
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'is_active')
    search_fields = ('title', 'code')
    list_filter = ('is_active',)


# ---------- Size ----------
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('width', 'height', 'unit')
    search_fields = ('unit__title',)
    list_filter = ('unit',)


# ---------- Unit ----------
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'symbol')
    search_fields = ('title', 'symbol')


# ---------- ProductImages ----------
@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created_time')
    list_filter = ('is_primary',)
    readonly_fields = ('created_time', 'updated_time')


# ---------- CatalogProduct ----------
@admin.register(CatalogProduct)
class CatalogProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created_time')
    list_filter = ('is_primary',)
    readonly_fields = ('created_time', 'updated_time')
