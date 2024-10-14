from neomodel import StructuredNode, StringProperty, UniqueIdProperty, DateTimeProperty
from datetime  import datetime

class User(StructuredNode):
    uid = UniqueIdProperty()
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    email_address = StringProperty(required=True, unique_index=True)
    phone_number = StringProperty(required=True, unique_index=True)
    created_at = DateTimeProperty(default=datetime.now)
    
class Institution(StructuredNode):
    uid = UniqueIdProperty()
    institution_name = StringProperty(required=True)
    email_address = StringProperty(required=True, unique_index=True)
    phone_number = StringProperty(required=True, unique_index=True)
