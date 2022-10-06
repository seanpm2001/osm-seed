from django.db import models
from datetime import datetime
import argon2

# Create your models here.
class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=100)
    display_name = models.CharField(unique=True, max_length=100)
    pass_crypt = models.CharField(max_length=100)
    data_public = models.BooleanField(default=True)
    email_valid = models.BooleanField(default=True)
    status = models.CharField(default="active", max_length=20)
    terms_seen = models.BooleanField(default=True)
    terms_agreed = models.DateTimeField(default=datetime.now, null=True)
    tou_agreed = models.DateTimeField(default=datetime.now, null=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        managed = False
        db_table = "users"

    def save(self, *args, **kwargs):
        argon2Hasher = argon2.PasswordHasher(
            time_cost=16, memory_cost=2 ** 16, parallelism=2, hash_len=32, salt_len=16
        )
        self.pass_crypt = argon2Hasher.hash(self.pass_crypt)
        super(Users, self).save(*args, **kwargs)
