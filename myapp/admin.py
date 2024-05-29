from django.contrib import admin
from .models import SparePart, SparePartCategory, Sale, Purchase
from rangefilter.filters import DateRangeFilter
from django.http import HttpResponse
import pandas as pd
from django.utils.timezone import make_naive

class SparePartCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'part_number', 'price', 'stock')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('spare_part', 'quantity', 'date', 'selling_price', 'total_amount', 'tax', 'profit')
    list_filter = (('date', DateRangeFilter),)
    actions = ['export_to_csv']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # if obj is not None, it's an edit
            return ['spare_part', 'quantity', 'date', 'selling_price', 'total_amount', 'tax', 'profit']
        else:
            return self.readonly_fields

    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'

        data = list(queryset.values(*field_names))
        for item in data:
            for field in field_names:
                if isinstance(item[field], pd.Timestamp) and item[field].tzinfo is not None:
                    item[field] = make_naive(item[field])

        df = pd.DataFrame(data)
        df.to_csv(path_or_buf=response, index=False)
        return response

    export_to_csv.short_description = 'Export to CSV'

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('spare_part', 'quantity', 'date', 'purchase_price', 'total_amount', 'tax')
    list_filter = (('date', DateRangeFilter),)
    actions = ['export_to_csv']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # if obj is not None, it's an edit
            return ['spare_part', 'quantity', 'date', 'purchase_price', 'total_amount', 'tax']
        else:
            return self.readonly_fields

    def export_to_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'

        data = list(queryset.values(*field_names))
        for item in data:
            for field in field_names:
                if isinstance(item[field], pd.Timestamp) and item[field].tzinfo is not None:
                    item[field] = make_naive(item[field])

        df = pd.DataFrame(data)
        df.to_csv(path_or_buf=response, index=False)
        return response

    export_to_csv.short_description = 'Export to CSV'

admin.site.register(SparePartCategory, SparePartCategoryAdmin)
admin.site.register(SparePart, SparePartAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Purchase, PurchaseAdmin)
