import graphene
from .models import User as UserModel, Contacts as ContactModel, OTP
from graphene_django import DjangoObjectType
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .otp import send_otp, send_sms
from datetime import datetime, timedelta
import jwt
from HelpBack.settings import SECRET_KEY

class UserType(graphene.ObjectType):
    uid = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email_address = graphene.String()
    phone_number = graphene.String()

# class CreateContact(graphene.Mutation):
#     class Arguments:
#         first_name = graphene.String(required=True)
#         last_name = graphene.String(required=True)
#         email_address = graphene.String(required=True)
#         phone_number = graphene.String(required=True)

class Register(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email_address = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        
    user = graphene.Field(UserType)
    
    def mutate(self, info, first_name, last_name, email_address, phone_number):
        if UserModel.nodes.filter(email_address=email_address):
            raise Exception ("User already exists")
        
        user = UserModel(first_name=first_name, last_name=last_name, email_address=email_address, phone_number=phone_number)
        print('user_creation', user)
        user.save()
        
        send_otp(phone_number)
        print('huraaay')
        
        return Register(user=user)
        
class ValidateOTP(graphene.Mutation):
    success = graphene.Boolean()
    access_token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        emailOrPhone = graphene.String(required=True)
        otp = graphene.String(required=True)
    
    def mutate(self, info, emailOrPhone, otp):
        try:
            
            user = UserModel.nodes.filter(phone_number=emailOrPhone).first()
            
            if not user:
                raise Exception("User not found")

            if OTP.verify_otp(emailOrPhone, otp):
                # Now `user` is a single node, and you can safely access `uid`
              
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                return ValidateOTP(success=True, access_token=access_token, refresh_token=refresh_token)
            
            raise Exception("OTP verification failed")
        
        except Exception as e:
            print(f"Error: {str(e)}")  # Logs the error in the server console
            raise Exception("An error occurred while validating OTP")

    
class LoginUser(graphene.Mutation):
    success = graphene.Boolean()
    access_token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        emailOrPhone = graphene.String(required=True) 

    def mutate(self, info, emailOrPhone):
        try:
            user = UserModel.nodes.filter(email_address=emailOrPhone) or UserModel.nodes.filter(phone_number=emailOrPhone)
            if not user:
                raise Exception("Account does not exist")            
            
            if '@' in emailOrPhone:
                send_otp(user.email_address)
            else:
                send_sms(user.phone_number)
            
            return LoginUser(success=True)
        except Exception:
            return LoginUser(success=False)
        
        
def generate_access_token(user):
    payload = {
        'user_id': user.uid,
        'exp' : datetime.utcnow() + timedelta(minutes=15),
        'iat' : datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY , algorithm='HS256')


def generate_refresh_token(user):
    payload = {
        'user_id': user.uid,
        'exp' : datetime.utcnow() + timedelta(days=7),
        'iat' : datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY , algorithm='HS256')
class Query(graphene.ObjectType):
    user_by_email = graphene.Field(UserType, email_address=graphene.String(required=True))
    
    def resolve_user_by_email(self, info, email_address):
        try:
            return UserModel.nodes.get(email_address=email_address)
        except UserModel.DoesNotExist:
            return None
        
class Mutation(graphene.ObjectType):
    Register = Register.Field()
    login = LoginUser.Field()
    validateOTP = ValidateOTP.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)
