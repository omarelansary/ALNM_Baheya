from django.db import models

# Create your models here.
from collections import OrderedDict

#TODO:Rga3y kol l json response ll assessments b tarteb l excel 

#This class works on ManyToMany relationships for data serialization
class AssessmentManager(models.Manager):
    def serialize_assessments(self, queryset):
            serialized_assessments = []
            for assessment in queryset:
                serialized_assessment = OrderedDict([
                    ('id', assessment.id),
                    ('MRN', assessment.MRN),
                    ('status', assessment.status),
                    ('status_message', assessment.get_status_message(assessment.status) if assessment.status is not None else None),
                    ('prediction', assessment.prediction),
                    ('ground_truth', assessment.ground_truth),
                    ('creation_date', assessment.creation_date),
                    ('medical_info', OrderedDict([
                        ('MRN', assessment.medical_info.get('MRN')),
                        ('patient_first_bmi', assessment.medical_info.get('patient_first_bmi')),
                        ('patient_age', assessment.medical_info.get('patient_age')),
                       
                        
                        ('vte_result', assessment.medical_info.get('vte_result')),
                        
                        ('Others', assessment.medical_info.get('Others')),
                        ('patient_family_history', assessment.medical_info.get('patient_family_history')),
                        ('patient_menopausal_state', assessment.medical_info.get('patient_menopausal_state')),
                        ('Hormonal_Contraception', assessment.medical_info.get('Hormonal_Contraception')),
                        ('patient_t', assessment.medical_info.get('patient_t')),
                        ('patient_n', assessment.medical_info.get('patient_n')),
                        ('patient_size_cm', assessment.medical_info.get('patient_size_cm')),
                        ('lymphovascular_invasion_result', assessment.medical_info.get('lymphovascular_invasion_result')),
                        ('patient_laterality', assessment.medical_info.get('patient_laterality')),
                        ('er_result', assessment.medical_info.get('er_result')),
                        ('pr_result', assessment.medical_info.get('pr_result')),
                        ('her2_result', assessment.medical_info.get('her2_result')),
                        ('patient_ki67', assessment.medical_info.get('patient_ki67')),
                        ('patient_unilateral_bilateral', assessment.medical_info.get('patient_unilateral_bilateral')),
                        ('patient_site', assessment.medical_info.get('patient_site')),
                        ('patient_tumor_type', assessment.medical_info.get('patient_tumor_type')),
                        ('patient_grade', assessment.medical_info.get('patient_grade'))
                    ]))
                ])
                               
                serialized_assessments.append(serialized_assessment)
            return serialized_assessments

#==================================
class Assessment(models.Model):

    #TODO:add ground truth field(nullable) -->DONE
    #TODO:add predicted field (nullable) -->DONE
    #TODO:status(enum:[1,2,3,4,5]) -->DONE
    #TODO:creation date -->DONE

    #For doctors views
    #TODO:get assessments by doctorid -->DONE
    #TODO:get status by MRN -->DONE
    #TODO:set groundtruth -->DONE
    #TODO:Handle update that same doctor & other new doctors can edit
    #&now save the created date and status -->DONE

    #TODO:Remove when refactor
    objects = AssessmentManager()

    #doctors are null in case doctors are deleted and no associated doctor
    doctors = models.ManyToManyField('doctors.Doctor', blank=True)
    medical_info = models.JSONField(default=dict)
    MRN = models.BigIntegerField()

    STATUS_CHOICES = [
        (1, 'Filled'),
        (2, '⁠Ground truth added'),
        (3, '⁠Reviewd'),
        (4, '⁠Retrianed'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    PREDICTION_CHOICES = [
            (0, 'Yes'),
            (1, 'No'),
            
        ]
    prediction=models.IntegerField(choices=PREDICTION_CHOICES, null=True, blank=True)
    
    GROUNDTRUTH_CHOICES=[
            (0, 'Yes'),
            (1, 'No'),
            
        ]
    ground_truth = models.IntegerField(choices=GROUNDTRUTH_CHOICES, null=True, blank=True)
   
    creation_date = models.DateField(null=True, blank=True)


    # Define a method to set medical info
    def set_medical_info(self, MRN, patient_first_bmi, patient_age, patient_size_cm, 
                     patient_ki67, patient_family_history, patient_menopausal_state, 
                     patient_t, patient_n, patient_laterality, 
                     patient_unilateral_bilateral, patient_site, 
                     patient_tumor_type, patient_grade,
                     vte_result,lymphovascular_invasion_result,er_result,
                     pr_result,her2_result,Others,Hormonal_Contraception):

        
        self.medical_info = OrderedDict([
            ("MRN", MRN),
            ("patient_first_bmi", patient_first_bmi),
            ("patient_age", patient_age),           
            ("vte_result", vte_result),            
            ("Others", Others),
            ("patient_family_history", patient_family_history),
            ("patient_menopausal_state", patient_menopausal_state),
            ("Hormonal_Contraception", Hormonal_Contraception),
            ("patient_t", patient_t),
            ("patient_n", patient_n),
            ("patient_size_cm", patient_size_cm),
            ("lymphovascular_invasion_result", lymphovascular_invasion_result),
            ("patient_laterality", patient_laterality),
            ("er_result", er_result),
            ("pr_result", pr_result),
            ("her2_result", her2_result),
            ("patient_ki67", patient_ki67),
            ("patient_unilateral_bilateral", patient_unilateral_bilateral),
            ("patient_site", patient_site),
            ("patient_tumor_type", patient_tumor_type),
            ("patient_grade", patient_grade)
        ])
        
        #Old model
        # self.medical_info = {
        #     "MRN": MRN,
        #     "patient_first_bmi": patient_first_bmi,
        #     "patient_age": patient_age,
        #     "patient_size_cm": patient_size_cm,
        #     "patient_ki67": patient_ki67,
        #     "patient_family_history": patient_family_history,
        #     "patient_menopausal_state": patient_menopausal_state,
        #     "patient_t": patient_t,
        #     "patient_n": patient_n,
        #     "patient_laterality": patient_laterality,
        #     "patient_unilateral_bilateral": patient_unilateral_bilateral,
        #     "patient_site": patient_site,
        #     "patient_tumor_type": patient_tumor_type,
        #     "patient_grade": patient_grade,
        #     "dm_result":dm_result,
        #     "htn_result":htn_result,
        #     "vte_result":vte_result,
        #     "cvd_result":cvd_result,
        #     "lymphovascular_invasion_result":lymphovascular_invasion_result,
        #     "er_result":er_result,
        #     "pr_result":pr_result,
        #     "her2_result":her2_result,
        #     "Others":Others,
        #     "Hormonal_Contraception":Hormonal_Contraception,

        # }
        
    def is_MRN_matching(self,MRN):
        if self.medical_info.MRN==MRN:
            return True
        else:
            return False
    
    def get_status_message(self, status_value):
        for value, message in self.STATUS_CHOICES:
            if value == status_value:
                return message
        return None

    def validate_binary_choices(self, binary_value):
        valid_ground_truth_values = [choice[0] for choice in self.GROUNDTRUTH_CHOICES]
        if binary_value not in valid_ground_truth_values:
            return False
        return True


    
