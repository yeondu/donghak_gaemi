from django.db import models
class stockModel(models.Model):
    class Meta:
        db_table = "stock"

    stock_name = models.CharField(max_length=20, null=False, blank=False)
    stock_code = models.CharField(primary_key = True, max_length = 10, null=False, blank=False)
    stock_category = models.CharField(max_length=20, null=False, blank=False)
    stock_foundation_year = models.DateField(null=False, blank=False)
    stock_listing_date = models.DateField(null=False, blank=False)

class priceModel(models.Model):
    class Meta:
        db_table = "price"

    stock_id = models.IntegerField(primary_key=True, null=False, blank=False, db_column = 'stock_id')
    date = models.DateField(null = False, blank = False)
    open = models.FloatField(null = False, blank = False)
    high = models.FloatField(null = False, blank = False)
    low = models.FloatField(null = False, blank = False)
    close = models.FloatField(null = False, blank = False)
    adj_close = models.FloatField(null = False, blank = False)
    volume = models.IntegerField(null = False, blank = False)
    stock_code = models.ForeignKey(stockModel, on_delete = models.CASCADE, db_column = 'stock_code')

class accuracyModel(models.Model):
    class Meta:
        db_table = "accuracy"

    model_id = models.IntegerField(primary_key=True, null=False, blank=False, db_column='model_id')
    accuracy = models.IntegerField(null=False, blank = False)
    stock_code = models.ForeignKey(stockModel, on_delete=models.CASCADE, db_column='stock_code')


class predictModel(models.Model):
    class Meta:
        db_table = "predict"

    model_id = models.ForeignKey(accuracyModel, on_delete=models.CASCADE, db_column = 'model_id')
    stock_id = models.ForeignKey(priceModel, on_delete=models.CASCADE, db_column = 'stock_id')
    result = models.IntegerField(null=False, blank = False)

class newsModel(models.Model):
    class Meta:
        db_table = "news"

    news_id = models.IntegerField(primary_key = True, null = False, blank = False, db_column='news_id')
    title = models.CharField(max_length = 100, null = False, blank = False)
    content = models.TextField(max_length = 20000, null = False, blank = False)
    summary = models.CharField(max_length = 500, null = False, blank = False)
    registrant = models.CharField(max_length = 18, null = False, blank = False)
    press = models.CharField(max_length = 18, null = False, blank = False)
    registration_date = models.DateField(null = False, blank = False)
    link = models.CharField(max_length = 100, null = False, blank = False)
    stock_code = models.ForeignKey(stockModel, on_delete=models.CASCADE, db_column='stock_code')


class sentimentModel(models.Model):
    class Meta:
        db_table = "sentiment"

    news_id = models.ForeignKey(newsModel, on_delete=models.CASCADE, db_column='news_id')
    result = models.IntegerField(null = False, blank = False)


