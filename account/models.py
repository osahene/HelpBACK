from neomodel import StringProperty, UniqueIdProperty, DateTimeProperty, IntegerProperty, RelationshipFrom, RelationshipTo
from django_neomodel import DjangoNode
from datetime  import datetime

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
