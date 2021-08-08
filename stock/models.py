from django.db import models

class stockModel(models.Model):
    class Meta:
        db_table = "stock"

    stock_id = models.IntegerField(null=False, blank=False)
    stock_name = models.CharField(max_length=20, null=False, blank=False)
    stock_code = models.IntegerField(null=False, blank=False)
    stock_category = models.CharField(max_length=20, null=False, blank=False)
    stock_market_capitalization = models.IntegerField(null=False, blank=False)
    stock_foundation_year = models.IntegerField(null=False, blank=False)
    stock_listing_date = models.CharField(max_length=20, null=False, blank=False)