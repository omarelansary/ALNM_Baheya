from django.shortcuts import render
from django.http import HttpResponse
#edited
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status 
#Allows us to fetch and create users and tokens from our database
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from django. shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Doctor
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from patients.models import Patient
from assessments.models import Assessment
import json
from django.utils import timezone
from django.db.utils import OperationalError
from utils.authenticators import generate_jwt_token
from assessments.serializers import AssessmentSerializer


@api_view(['POST'])
def forgotPassword(request):
    try:    
        # Get request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if both email and password are provided
        if email is None:
            return Response({'success': False, 'message': 'Please provide an email'}, status=400)
        if password is None:
            return Response({'success': False, 'message': 'Please provide a password'}, status=400)
        
        try:
            # Check if a Doctor object with the provided email exists
            doctor = Doctor.objects.get(email=email)
            
            # Hash the new password
            hashed_password = make_password(password)
            
            # Update the password for the doctor object
            doctor.password = hashed_password
            
            # Save the doctor object to update the password in the database
            doctor.save()

            #TODO:Uncomment later
            
            # #send email to doctor
            # my_subject='Password notification for Baheya ALNM Website'
            # my_message='Your password is restored successfully. You can now login with your credentials.'
            # send_mail(
            #     subject=my_subject,
            #     message=my_message,
            #     recipient_list=[email],
            #     from_email=None,
            #     fail_silently=False)

            return Response({'success': True,'message': 'Password restored successfully.'})
        
        except ObjectDoesNotExist:
            # Handle the case where no Doctor object with the provided email exists
            return Response({'success': False, 'message': 'Email address not found.'}, status=404)
        
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)


#======================================================================================
@api_view(['POST'])
def login(request):
    try:
        #TODO: return id , fisrat and lastname in the response -->DONE
        # Get request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if both email and password are provided
        if email is None or password is None:
            return Response({'success': False, 'message': 'Please provide both email and password'}, status=400)

        # Check if email already exists in the database
        if Doctor.objects.filter(email=email).exists():
            #compare password (methode 2)
            doctor=Doctor.objects.get(email=email)
            print("My doctor object:\n",doctor)
            print("Database password:\n",doctor.password)
            print("User entered password:\n",password)

            print("Manual password checker:\n",type(password))
        
            # Check if user exists and password matches
            if doctor is None or not check_password(password, doctor.password):
                return Response({'success': False,'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                #TODO:set an expiration date
                token=generate_jwt_token(doctor.id)
                print("My token: ",token)
                return Response({'success': True,"id":doctor.id,"firstName":doctor.firstName,"lastName":doctor.lastName,'token': token,'message': 'Login successful'})
        else:
            # Email does not exist in the database
            return Response({'success': False, 'error': 'Email does not exist'}, status=400)
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)


#===========================END BRAND NEW LOGIN=====================
#===========================Risk Assessment View====================
'''
This function takes the doctor id and patients MRN along with other medical info
It allows multiple doctors to insert patients data but ONLY once each

'''

# @api_view(['POST'])
# def insertAndRetrievePatientInfo(request):
    
#     # Extract doctor_id and medical_info from the request
#     doctor_id = request.data.get('doctor_id')
#     MRN = request.data.get('medical_info').get('MRN')

#     # Check if doctor_id and MRN are provided
#     if not doctor_id or not MRN:
#         return Response({
#             'success': False,
#             'message': 'Doctor ID or MRN is missing.'
#         })
#     # Check if medical_info is provided
#     medical_info = request.data.get('medical_info')
#     if not medical_info:
#         return Response({
#             'success': False,
#             'message': 'Medical info is missing.'
#         })
    
#     try:
#         # Retrieve the doctor object based on the ID
#         doctor = Doctor.objects.get(id=doctor_id)
#     except ObjectDoesNotExist:
#         # Return failure response if doctor does not exist
#         return Response({
#             'success': False,
#             'message': 'Doctor does not exist.'
#         })
    
#     try:
#         patient = Patient.objects.get(MRN=MRN)
#     except ObjectDoesNotExist:
#         patient = Patient.objects.create()

#     # Check if the doctor is already associated with the patient
#     if patient.objects.filter(doctors__id=doctor_id).exists():
#         return Response({
#             'success': False,
#             'message': 'Doctor already created this patient before.'
#         })


    


#     # No need to parse medical_info as JSON since it's already a dictionary
#     # try:
#     #     # Parse medical_info as JSON
#     #     medical_info = json.loads(medical_info)
#     # except json.JSONDecodeError:
#     #     # Return failure response if medical_info is not valid JSON
#     #     return Response({
#     #         'success': False,
#     #         'message': 'Invalid medical info format.'
#     #     })


#     # Use the set_medical_info method to set medical info for the patient
#     patient.set_medical_info(
#         MRN=medical_info.get('MRN'),
#         patient_first_bmi=medical_info.get('patient_first_bmi'),
#         patient_age=medical_info.get('patient_age'),
#         patient_size_cm=medical_info.get('patient_size_cm'),
#         patient_ki67=medical_info.get('patient_ki67'),
#         patient_family_history=medical_info.get('patient_family_history'),
#         patient_menopausal_state=medical_info.get('patient_menopausal_state'),
#         patient_t=medical_info.get('patient_t'),
#         patient_n=medical_info.get('patient_n'),
#         patient_laterality=medical_info.get('patient_laterality'),
#         patient_unilateral_bilateral=medical_info.get('patient_unilateral_bilateral'),
#         patient_site=medical_info.get('patient_site'),
#         patient_tumor_type=medical_info.get('patient_tumor_type'),
#         patient_grade=medical_info.get('patient_grade')
#     )


#     # Add the doctor to the patient's doctors
#     patient.doctors.add(doctor)

#     # Save the patient object
#     patient.save()

#     # Return the patient object in the response
#     return Response({
#         'success': True,
#         'id': patient.id,
#         'medical_info': patient.medical_info,
#         'doctors': [doc.id for doc in patient.doctors.all()]
#     })
#####################################
#================GET ASSESSMENTS BY STATUS===================================
@api_view(['POST'])
def getAssessmentsByStatus(request):
    try:
        #Extract request data
        doctor_id=request.data.get('doctor_id')
        status=request.data.get('status')

        if doctor_id is None:
            return Response({
            'success': False,
            'message': 'Doctor ID is missing.'
        })

        if status is None:
            return Response({
            'success': False,
            'message': 'Status is missing.'
        })

        # Retrieve the doctor object by doctor_id
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Retrieve assessments associated with the doctor
        assessments = doctor.assessments.filter(status=status)

        #serialize assessments
        serialized_assessments=doctor.assessments.serialize_assessments(assessments)
        
      
        return Response({
            'success': True,
           'assessments': serialized_assessments, 
        })
    except Doctor.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Doctor not found.',
        })
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)

#============================================================================
#================GET STATUS BY MRN============================================

@api_view(['POST'])
def getStatusByMRN(request):
    try:
        MRN=request.data.get('MRN')
     
        if MRN is None:
            return Response({
            'success': False,
            'message': 'MRN is missing.'
        })   

        try:
            # Attempt to retrieve the assessment object based on MRN
            assessment = Assessment.objects.get(MRN=MRN)
        except Assessment.DoesNotExist:
            # If the assessment doesn't exist, return error message
            return Response({
                'success': False,
                'message': 'This patient doesn\'t exist.'
            })    
        
        message=assessment.get_status_message(assessment.status)

        return Response({
                'success': True,
                'status':assessment.status ,
                'status_message':message,
            })

    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)



#=============================================================================
#================GET ASSESSMENTS BY DOCTOR ID=================================


@api_view(['GET'])
def getAssessmentsByDocId(request):
    try:
        #Extract request data
        doctor_id=request.data.get('doctor_id')

        if doctor_id is None:
            return Response({
            'success': False,
            'message': 'Doctor ID is missing.'
        })

        # Retrieve the doctor object by doctor_id
        doctor = Doctor.objects.get(id=doctor_id)
        
        # Retrieve assessments associated with the doctor
        assessments = doctor.assessments.all()

        # #serialize assessments
        serialized_assessments=doctor.assessments.serialize_assessments(assessments)
        
      
        return Response({
            'success': True,
           'assessments': serialized_assessments, 
        })
    except Doctor.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Doctor not found.',
        })
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)




#=============================================================================
#============================SET GROUND TRUTH=================================

@api_view(['POST'])
def setGroundTruth(request):
    try:
        #Extract request information
        MRN=request.data.get('MRN')
        doctor_id = request.data.get('doctor_id')
        ground_truth = request.data.get('ground_truth')

        # Check if doctor_id, MRN, and ground_truth are provided
        if doctor_id is None or MRN is None or ground_truth is None:
            return Response({
                'success': False,
                'message': 'Doctor ID, MRN, or ground_truth is missing.'
            })
        

        try:
            # Attempt to retrieve the assessment object based on MRN
            assessment = Assessment.objects.get(MRN=MRN)
        except Assessment.DoesNotExist:
            # If the assessment doesn't exist, return error message
            return Response({
                'success': False,
                'message': 'This patient doesn\'t exist.'
            })
        
        # Check if the doctor is not associated with the assessment
        if not assessment.doctors.filter(id=doctor_id).exists():
            return Response({
                'success': False,
                'message': 'This doctor id is not associated with this assessment.'
            })
        
        isValide=assessment.validate_binary_choices(ground_truth)
        if not isValide:
            return Response({
                'success': False,
                'message': 'Please enter either 0 or 1 for ground truth.'
            })

        assessment.ground_truth=ground_truth
        assessment.status=2
        # Save the assessment object
        assessment.save()

        message=assessment.get_status_message(assessment.status)
        
        return Response({
            'success': True,
            'message': 'Ground truth updated successfully.',
            'status':assessment.status,
            'status_message':message,

        })
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)



    


#=================================================================================
@api_view(['POST'])
def makeAssessment(request):
    try:
        #TODO: add lines of code to save prediction of model to current assessement
        # Extract doctor_id and medical_info from the request
        doctor_id = request.data.get('doctor_id')
        medical_info = request.data.get('medical_info')
        MRN=request.data.get('MRN')

        # Check if doctor_id and medical_info are provided
        if doctor_id is None or medical_info is None or MRN is None:
            return Response({
                'success': False,
                'message': 'Doctor ID, medical info or MRN is missing.'
            })

        try:
            # Retrieve the doctor object based on the ID
            doctor = Doctor.objects.get(id=doctor_id)
        except ObjectDoesNotExist:
            # Return failure response if doctor does not exist
            return Response({
                'success': False,
                'message': 'Doctor does not exist.'
            })
        
        try:
            # Attempt to retrieve the assessment object based on MRN
            assessment = Assessment.objects.get(MRN=MRN)
        except Assessment.DoesNotExist:
            # If the assessment doesn't exist, create a new one
            assessment = Assessment.objects.create(MRN=MRN)

        # # Check if the doctor is already associated with the assessment
        # if assessment.doctors.filter(id=doctor_id).exists():
        #     return Response({
        #         'success': False,
        #         'message': 'Doctor already associated with this assessment.'
        #     })

        # Use the method to set medical info for the assessment
        assessment.set_medical_info(
            MRN=MRN,
            patient_first_bmi=medical_info.get('patient_first_bmi'),
            patient_age=medical_info.get('patient_age'),
            dm_result=medical_info.get('patientdm_result_size_cm'),
            htn_result=medical_info.get('patienhtn_resultt_ki67'),
            vte_result=medical_info.get('patient_famivte_resultly_history'),
            cvd_result=medical_info.get('cvd_result'),
            Others=medical_info.get('Others'),
            patient_family_history=medical_info.get('patient_family_history'),
            patient_menopausal_state=medical_info.get('patient_menopausal_state'),
            Hormonal_Contraception=medical_info.get('Hormonal_Contraception'),
            patient_t=medical_info.get('patient_t'),
            patient_n=medical_info.get('patient_n'),
            patient_size_cm=medical_info.get('patient_size_cm'),
            lymphovascular_invasion_result=medical_info.get('lymphovascular_invasion_result'),
            patient_laterality=medical_info.get('patient_laterality'),
            er_result=medical_info.get('er_result'),
            pr_result=medical_info.get('pr_result'),
            her2_result=medical_info.get('her2_result'),
            patient_ki67=medical_info.get('patient_ki67'),
            patient_unilateral_bilateral=medical_info.get('patient_unilateral_bilateral'),
            patient_site=medical_info.get('patient_site'),
            patient_tumor_type=medical_info.get('patient_tumor_type'),
            patient_grade=medical_info.get('patient_grade'),
        )

        # Add the doctor to the assessment's doctors
        assessment.doctors.add(doctor)

        # Add the assessment to the doctor's assessments
        doctor.assessments.add(assessment)

        #Add status to assessment
        assessment.status = 1
        
        #Add date assessment created 
        assessment.creation_date = timezone.now().date()

        # Save the assessment object
        assessment.save()
        # ###
        # doctorss = assessment.doctors.all()
        
        # # Convert queryset to list of dictionaries
        # doctorss_list = [{'id': doctor.id} for doctor in doctorss]
        # ###
        message=assessment.get_status_message(assessment.status)

        # Return the assessment object in the response
        return Response({
            'success': True,
            'id': assessment.id,
            'MRN':MRN,
            'status':assessment.status,
            'status_message':message,
            'creation_date':assessment.creation_date,
            'medical_info': assessment.medical_info,
            'doctors': [doc.id for doc in assessment.doctors.all()],
        
        })
    
    except OperationalError as e:
        # Return an error response for database errors
        return Response({'success': False, 'message': f'Database error: {e}'}, status=400)
    except Exception as e:
        # Return a generic error response for other exceptions
        return Response({'success': False, 'message': f'An error occurred: {e}'}, status=500)



#===================================================================

#=========================================================================
# @api_view( ['POST'])
# def login (request) :
#   user = get_object_or_404(User, username=request.data ['username'])
#   if not user. check_password (request.data[ 'password']):
#     return Response({"detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
#   token, created = Token.objects.get_or_create(user=user)
#   serializer = UserSerializer (instance=user)
#   return Response({"token": token.key, "user": serializer.data})

#New login for both data and token authentication
# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     # Authenticate the user using username and password
#     user = authenticate(username=username, password=password)

#     if user:
#         # If user is authenticated, generate or retrieve a token
#         token, created = Token.objects.get_or_create(user=user)
        
#         # Serialize the user object to include user data in the response
#         serializer = UserSerializer(instance=user)
        
#         # Return the token and user data in the response
#         return Response({"token": token.key, "user": serializer.data})
#     else:
#         # If authentication fails, return a 404 Not Found response
#         return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
# #===================================================================================

# @api_view( ['POST'])
# def signUp (request) :
#   #Get serializer instance based on the data passed in our request
#   serializer = UserSerializer(data=request.data)
#   #Check if data valid (username,password & email recieved)
#   if serializer.is_valid():
#     serializer.save()
#     #Retrieve user by username
#     user = User.objects.get (username=request. data ['username'] )
#     #Save password in a hashed(encoded) format for security reasons
#     user.set_password (request.data ['password'])
#     user.save()
#     #Generate token for frontend
#     token = Token.objects.create(user=user)

#     #Return user token and data
#     return Response({"token": token.key, "user": serializer.data})
#   return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
