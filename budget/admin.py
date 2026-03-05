from django.contrib import admin
from .models import Project, Category, Expense

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'budget', 'budget_left', 'total_transactions')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('budget_left', 'total_transactions')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')
    list_filter = ('project',)
    search_fields = ('name',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'project', 'category')
    list_filter = ('project', 'category')
    search_fields = ('title', 'project_name', 'category_name')
    ordering = ('-amount',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Expense, ExpenseAdmin)