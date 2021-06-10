from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.files import FileField

# Create your models here.

FUNCTION_CHOICE = (
    ('ENCRYPT', 'Encrypt'),
    ('DECRYPT', 'Decrypt'),
)

TYPE_CHOICE = (
    ('AESCBC', 'AES CBC'),
    ('AESCFB', 'AES CFB'),
    ('OTK', 'One-time Key'),
    ('BASESF', 'Base 64'),
)

class Cryptdb(models.Model):
    function = CharField(max_length=7, choices=FUNCTION_CHOICE, default='Encrypt')
    type = CharField(max_length=15, choices=TYPE_CHOICE, default=None, null=True)
    inputfile = FileField(upload_to='inputs/')
    encryptedfile = FileField(upload_to='encrypted/', null=True)
    decryptedfile = FileField(upload_to='decrypted/', null=True)
    keyfile = FileField(null=True)
    ivfile = FileField(null=True)