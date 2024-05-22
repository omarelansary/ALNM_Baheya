from django.db import models

# Create your models here.
from django.db import models



class Patient(models.Model):
    #doctors are null in case doctors are deleted and no associated doctor
    # doctors = models.ManyToManyField('doctors.Doctor', blank=True)
    medical_info = models.JSONField(default=dict)
    MRN = models.BigIntegerField()

    # Define a method to set medical info
    def set_medical_info(self, MRN, patient_first_bmi, patient_age, patient_size_cm, patient_ki67, patient_family_history, patient_menopausal_state, patient_t, patient_n, patient_laterality, patient_unilateral_bilateral, patient_site, patient_tumor_type, patient_grade):
        self.medical_info = {
            "MRN": MRN,
            "patient_first_bmi": patient_first_bmi,
            "patient_age": patient_age,
            "patient_size_cm": patient_size_cm,
            "patient_ki67": patient_ki67,
            "patient_family_history": patient_family_history,
            "patient_menopausal_state": patient_menopausal_state,
            "patient_t": patient_t,
            "patient_n": patient_n,
            "patient_laterality": patient_laterality,
            "patient_unilateral_bilateral": patient_unilateral_bilateral,
            "patient_site": patient_site,
            "patient_tumor_type": patient_tumor_type,
            "patient_grade": patient_grade
        }
    
    def is_MRN_matching(self,MRN):
        if self.medical_info.MRN==MRN:
            return True
        else:
            return False






