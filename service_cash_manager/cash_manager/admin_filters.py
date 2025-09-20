from datetime import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter


class CashFlowStatusFilter(admin.SimpleListFilter):
    title = "Статус"
    parameter_name = "status_title"
    template = "admin/cash_manager/input_filter.html"

    def lookups(self, request, model_admin):
        return [("", "")]

    def queryset(self, request, queryset):
        if value := self.value():
            return queryset.filter(status__title__icontains=value)
        return queryset

    def choices(self, changelist):
        return []


class CashFlowTypeFilter(admin.SimpleListFilter):
    title = "Тип"
    parameter_name = "type_title"
    template = "admin/cash_manager/input_filter.html"

    def lookups(self, request, model_admin):
        return [("", "")]

    def queryset(self, request, queryset):
        if value := self.value():
            return queryset.filter(type__title__icontains=value)
        return queryset

    def choices(self, changelist):
        return []


class CashFlowCategoryFilter(admin.SimpleListFilter):
    title = "Категория"
    parameter_name = "category_title"
    template = "admin/cash_manager/input_filter.html"

    def lookups(self, request, model_admin):
        return [("", "")]

    def queryset(self, request, queryset):
        if value := self.value():
            return queryset.filter(type__category_by_type__category__title=value)
        return queryset

    def choices(self, changelist):
        return []


class CashFlowSubCategoryFilter(admin.SimpleListFilter):
    title = "Подкатегория"
    parameter_name = "subcategory_title"
    template = "admin/cash_manager/input_filter.html"

    def lookups(self, request, model_admin):
        return [("", "")]

    def queryset(self, request, queryset):
        if value := self.value():
            return queryset.filter(type__category_by_type__category__category_by_subcategory__subcategory__title=value)
        return queryset

    def choices(self, changelist):
        return []


class CashFlowCommentFilter(SimpleListFilter):
    title = 'Поиск по комментарию'
    parameter_name = 'comment'
    template = "admin/cash_manager/input_filter.html"

    def lookups(self, request, model_admin):
        return [("", "")]

    def queryset(self, request, queryset):
        if value := self.value():
            return queryset.filter(comment__icontains=value)
        return queryset

    def choices(self, changelist):
        return []
