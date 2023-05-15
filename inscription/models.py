from django.db import models

# Create your models here.

class Sequence(models.Model):
    seqid = models.CharField(max_length=8, unique=True, blank=False, null=False)
    seq_in_num = models.CharField(max_length=150, blank=False, null=False)
    links = models.CharField(max_length=700, blank=True, null=True)
    cisi_id = models.CharField(max_length=10, null=True, blank=True)
    wells_id = models.CharField(max_length=5, null=True, blank=True)
    site = models.CharField(max_length=50, null=True, blank=True)
    artefact_type = models.CharField(max_length=25, null=True, blank=True)
    material_type = models.CharField(max_length=25, null=True, blank=True)
    field_symbol = models.CharField(max_length=25, null=True, blank=True)
    excavation_number = models.CharField(max_length=25, null=True, blank=True)
    area = models.CharField(max_length=25, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.seqid
    
    def save(self, *args, **kwargs):
        if '-' in self.seq_in_num:
            self.links = [f'/static/ivcgraphemes/CEL{ss}.png' for ss in self.seq_in_num.split('-')]
        else:
            self.links = [f'/static/ivcgraphemes/CEL{self.seq_in_num}.png']
        super().save(*args, **kwargs)


class Signary(models.Model):
    signid = models.CharField(max_length=8, unique=True, blank=False, null=False)
    wellsid = models.CharField(max_length=10, null=True, blank=True)
    #mahadevanid = models.CharField(null=True, blank=True)
    frequency = models.IntegerField(default=0)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.signid
    
    def save(self, *args, **kwargs):
        self.link = f'/static/ivcgraphemes/CEL{self.signid}.png'
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Signary'
    

