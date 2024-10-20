from neomodel import StringProperty, UniqueIdProperty, DateTimeProperty, IntegerProperty, RelationshipFrom, RelationshipTo
from django_neomodel import DjangoNode
from datetime  import datetime, timedelta
from django.utils import timezone

class User(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email_address = StringProperty(required=True, unique_index=True)
    phone_number = StringProperty(required=True, unique_index=True)
    created_at = DateTimeProperty(default=datetime.now)
    

class Contacts(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email_address = StringProperty(required=True, unique_index=True)
    phone_number = StringProperty(required=True, unique_index=True)
    created_at = DateTimeProperty(default=datetime.now)
    relation = RelationshipFrom('User', 'RELATION')
    
        
class Institution(DjangoNode):
    uid = UniqueIdProperty(primary_key=True)
    institution_name = StringProperty(required=True)
    email_address = StringProperty(required=True, unique_index=True)
    phone_number = StringProperty(required=True, unique_index=True)


class OTP(DjangoNode):
    otp_code = StringProperty(required=True)
    emailOrPhone = StringProperty(required=True)
    expiration_time = DateTimeProperty(required=True)

    @staticmethod
    def generate_otp():
        import random
        return str(random.randint(100000, 999999))  

    @staticmethod
    def create_otp(emailOrPhone):
        otp_code = OTP.generate_otp()
        expiration_time = timezone.now() + timedelta(seconds=60)
        otp = OTP(otp_code=otp_code, emailOrPhone=emailOrPhone, expiration_time=expiration_time)
        otp.save()
        return otp_code

    @staticmethod
    def verify_otp(emailOrPhone, otp_code):
        otp_record = OTP.nodes.filter(emailOrPhone=emailOrPhone).first()
        if not otp_record:
            raise Exception("OTP not found")

        if timezone.now() > otp_record.expiration_time:
            raise Exception("OTP expired")

        if otp_record.otp_code != otp_code:
            raise Exception("Invalid OTP")

        # Optionally delete the OTP after successful validation
        otp_record.delete()
        return True