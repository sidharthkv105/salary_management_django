from django.db import models

class Salary(models.Model):
    salary_date = models.DateField()
    pay = models.FloatField()
    da = models.FloatField()
    hra = models.FloatField()
    allowance = models.FloatField()
    co_date = models.DateField()
    gpf = models.FloatField()
    sli = models.FloatField()
    gis = models.FloatField()
    lic = models.FloatField()
    medisep = models.FloatField()
    gpais = models.FloatField()
    pro_tax = models.FloatField()
    i_tax = models.FloatField()

    gross = models.FloatField()
    deduction = models.FloatField()
    net = models.FloatField()

    def save(self, *args, **kwargs):
        self.gross = self.pay + self.da + self.hra + self.allowance
        self.deduction = self.gpf + self.sli + self.gis + self.lic + self.medisep + self.gpais + self.pro_tax + self.i_tax
        self.net = self.gross - self.deduction
        super().save(*args, **kwargs)

