from django.db import models
from user.models import UserModel

class tradingNoteModel(models.Model):
    class Meta:
        db_table = "tradingNote"

    trading_note_id = models.IntegerField(null=False, blank=False)
    user_id = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    stock_id = models.IntegerField(null=False, blank=False)
    trading_category = models.CharField(max_length=20, null=False, blank=False)
    buying_date = models.DateField()
    sell_date = models.DateField()
    stop_loss = models.IntegerField()
    holding_period = models.IntegerField()
    profit = models.IntegerField()
    contract_price = models.IntegerField(null=False, blank=False)
    contract_amount = models.IntegerField(null=False, blank=False)
    total_price = models.IntegerField(null=False, blank=False)
    trading_comment = models.CharField(max_length=2000)


