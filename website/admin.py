from django.contrib import admin
from .models import (
    SiteSetting,
    ProductImages,
    Categories,
    Color,
    Product,
    Door,
    Size,
    Unit,
    CatalogProduct,
    SparePart,
    Usage,
    ProductComment
)


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('title',)

# ---------- SiteSetting ----------
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone_factory', 'email', 'created_time')
    list_filter = ('site_name',)
    search_fields = ('site_name',)


# ---------- Inlines for Product ----------
class ProductDetailsInline(admin.StackedInline):
    model = Door
    readonly_fields = ('created_time', 'updated_time')
    filter_horizontal =('usage',)
    extra = 0

class ProductCommentAdmin(admin.StackedInline):
    model = ProductComment
    readonly_fields =  ('created_time', 'updated_time')
    extra = 0

class SparePartInline(admin.StackedInline):
    model = SparePart
    readonly_fields = ('created_time', 'updated_time')
    extra = 0

class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    readonly_fields = ('created_time', 'updated_time')
    extra = 0


class CatalogProductInline(admin.StackedInline):
    model = CatalogProduct
    readonly_fields = ('created_time', 'updated_time')
    extra = 0


# ---------- Product ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_type', 'is_active', 'get_like', 'get_dislike')
    search_fields = ('title', )
    list_filter = ('category', 'product_type', 'is_active', 'berand')
    inlines = (ProductDetailsInline, SparePartInline,ProductImagesInline, CatalogProductInline, ProductCommentAdmin)
    list_display_links = ('title', 'product_type')
    
    filter_horizontal = ('category','like', 'un_like')

    def get_categories(self, obj):
        return ", ".join([c.title for c in obj.category.all()])
    get_categories.short_description = "دسته‌بندی‌ها" # type: ignore
    
    def get_like(self, obj):
        return obj.get_like()
    
    def get_dislike(self, obj):
        return obj.get_unlike()


# ---------- Categories ----------
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'is_active')
    search_fields = ('title',)
    list_filter = ('parent', 'is_active')


# ---------- ProductDetails ----------
@admin.register(Door)
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('product', 'opening_type', 'direction_opening', 'color', 'size')
    search_fields = ('product__title',)
    list_filter = ('opening_type', 'direction_opening', 'fire_resistant', 'has_sensor')
    
    filter_horizontal = ('usage',)


# ---------- Color ----------
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'is_active')
    search_fields = ('title', 'code')
    list_filter = ('is_active',)


# ---------- Size ----------
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('width', 'height', 'length','unit')
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
    list_display = ('product', 'created_time')
    readonly_fields = ('created_time', 'updated_time')


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'full_name', 'is_approved')
    