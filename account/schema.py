import graphene
from .models import User as UserModel
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .otp import send_otp

class UserType(graphene.ObjectType):
    uid = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email_address = graphene.String()
    phone_number = graphene.String()

class CreateUser(graphene.Mutation):
        class Arguments:
            first_name = graphene.String(required=True)
            last_name = graphene.String(required=True)
            email_address = graphene.String(required=True)
            phone_number = graphene.String(required=True)
            
        user = graphene.Field(UserType)
        
        def mutate(self, info, first_name, last_name, email_address, phone_number):
            if UserModel.objects.filter(email_address=email_address).exists():
                raise Exception ("User already exists")
            
            user = UserModel(first_name=first_name, last_name=last_name, email_address=email_address, phone_number=phone_number)
            user.save()
            
            send_otp(phone_number)
            
            return CreateUser(user=user)
        
class ValidateOTP(graphene.Mutation):
    class Arguments:
        phone_number = graphene.String(required=True)
        otp = graphene.String(required=True)
    
    success = graphene.Boolean()
    
    def mutate(self, info, phone_number, otp):
        user = UserModel.objects.filter(phone_number=phone_number).first()
        if not user or user.otp != otp:
            raise Exception("Invalid OTP")
        
        user.otp = None
        user.save()
        
        return ValidateOTP(success=True)
    
class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, email, password):
        user = authenticate(email=email, password=password)
        if not user:
            raise Exception('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        return LoginUser(
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
            user=user
        ) 

class Query(graphene.ObjectType):
	pass

class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
