from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from .utils import unique_prescription_id
from cryptography.fernet import Fernet


class Prescription(models.Model):
    KEY = Fernet.generate_key()
    ENCRYPTER = Fernet(KEY)
    TEST_CHOICES = (
        ('1', 'CBC'),
        ('2', 'Dengue'),
        ('3', 'Malaria'),
        ('4', 'Random Blood Sugar'),
        ('5', 'Pregnancy'),
    )
    prescription_id = models.CharField(unique=True, max_length=10)
    created_at = models.DateTimeField()
    remarks = models.TextField(max_length=240)
    doctor = models.ForeignKey(to='accounts.Doctor', on_delete=models.CASCADE, null=True)
    utilised = models.BooleanField(default=False)

    def __str__(self):
        return self.prescription_id


def pre_save_prescription(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.created_at = timezone.now()
        instance.prescription_id = unique_prescription_id(instance)


pre_save.connect(pre_save_prescription, sender=Prescription)


class Drug(models.Model):
    drug_id = models.CharField(unique=True, max_length=16)

    # DRUG LIST REQUIRED
    drug_name = models.CharField(max_length=40)


class PrescribedDrug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Appointment(models.Model):
    doctor = models.ForeignKey(to="accounts.Doctor", on_delete=models.CASCADE,
                               related_name="app_doctor", blank=True, null=True)
    patient = models.CharField(max_length=50)  # ldap for iitj / firstname__ldap for family members
    time = models.DateTimeField()  # time, date of appointment
    temp = models.CharField(max_length=8, blank=True, null=True)   # temperature (to be put in by receptionist)

    def __str__(self):
        return self.doctor.user.first_name + ", " + self.patient


class DoctorSpecialization(models.Model):
    specialization = models.TextField(max_length=32)

    def __str__(self):
        return self.specialization
