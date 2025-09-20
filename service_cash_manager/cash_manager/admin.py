from django import forms
from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder

from .admin_filters import (
    CashFlowStatusFilter,
    CashFlowTypeFilter,
    CashFlowCategoryFilter,
    CashFlowSubCategoryFilter,
    CashFlowCommentFilter,
)
from .models import (
    CashFlow,
    CashFlowStatus,
    CashFlowCategoryByType,
    CashFlowType,
    CashFlowCategoryBySubcategory,
    CashFlowCategory,
    CashFlowSubCategory,
)

class DefaultAdmin(admin.ModelAdmin):
    list_display = ("title", "alias")
    list_display_links = ("title", )

    ordering = ("title", "alias")
    sortable_by = ("title", "alias")
    search_fields = ("title",)


@admin.register(CashFlowStatus)
class CashFlowStatusAdmin(DefaultAdmin):
    pass


@admin.register(CashFlowSubCategory)
class CashFlowSubCategoryAdmin(DefaultAdmin):
    pass


class CashFlowCategoryBySubcategoryForm(forms.ModelForm):
    class Meta:
        model = CashFlowCategoryBySubcategory
        fields = "__all__"
        widgets = {"subcategory_id": forms.Select(attrs={"class": "select2"})}


class CashFlowCategoryBySubcategoryInline(admin.TabularInline):
    model = CashFlowCategoryBySubcategory
    form = CashFlowCategoryBySubcategoryForm
    extra = 1
    autocomplete_fields = ("subcategory_id", )


@admin.register(CashFlowCategory)
class CashFlowCategoryAdmin(DefaultAdmin):
    inlines = (CashFlowCategoryBySubcategoryInline, )


class CashFlowCategoryByTypeForm(forms.ModelForm):
    class Meta:
        model = CashFlowCategoryByType
        fields = "__all__"
        widgets = {"category_id": forms.Select(attrs={"class": "select2"})}


class CashFlowCategoryByTypeInline(admin.TabularInline):
    model = CashFlowCategoryByType
    form = CashFlowCategoryByTypeForm
    extra = 1
    autocomplete_fields = ("category_id", )


@admin.register(CashFlowType)
class CashFlowTypeAdmin(DefaultAdmin):
    inlines = (CashFlowCategoryByTypeInline, )


class CashFlowAdminForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = "__all__"
        widgets = {
            "status": forms.Select(attrs={"class": "select2"}),
            "type": forms.Select(attrs={"class": "select2"}),
        }


@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    form = CashFlowAdminForm

    list_display = (
        "id",
        "status__title",
        "type__title",
        "titles_categories",
        "titles_subcategories",
        "amount",
        "comment",
        "created_at",
    )
    list_display_links = ("id", )

    ordering = ("amount", "created_at")
    sortable_by = ("amount", "created_at")
    list_filter = [
        CashFlowStatusFilter,
        CashFlowTypeFilter,
        CashFlowCategoryFilter,
        CashFlowSubCategoryFilter,
        CashFlowCommentFilter,
        ("created_at", DateRangeFilterBuilder(title="Дата создания")),
    ]

    def titles_categories(self, obj):
        if obj.type:
            categories_titles = CashFlowCategory.objects.filter(
                category_by_type__type=obj.type
            ).values_list(
                "title",
                flat=True,
            ).distinct()

            return (
                ", ".join(categories_titles)
                if categories_titles else "—"
            )
        return "—"

    def titles_subcategories(self, obj):
        if obj.type:
            subcategories_titles = CashFlowSubCategory.objects.filter(
                category_by_subcategory__category__category_by_type__type=obj.type
            ).values_list(
                "title",
                flat=True,
            ).distinct()

            return (
                ", ".join(subcategories_titles)
                if subcategories_titles else "—"
            )
        return "—"
