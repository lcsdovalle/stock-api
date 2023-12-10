from users.admin import admin_site

from .models.stock import Stock

admin_site.register(Stock)
