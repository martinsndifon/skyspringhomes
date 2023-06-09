#!/usr/bin/python3
"""Base model for all classes"""
import uuid
from datetime import datetime
import pytz
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
import models

Base = declarative_base()


class BaseModel:
    """Implement shared attributes"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos')))
    updated_at = Column(DateTime, default=datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos')))

    def __init__(self, *args, **kwargs):
        """Initialize the basemodel"""
        if kwargs:
            for attr, val in kwargs.items():
                setattr(self, attr, val)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos'))
            else: 
                if type(self.created_at) is str:
                    time = '%Y-%m-%dT%H:%M:%S.%f'
                    self.created_at = datetime.strptime(self.created_at, time)
            if 'updated_at' not in kwargs:
                self.updated_at = None
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos'))
            self.updated_at = datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos'))

    def __str__(self):
        """Return string representationof the object"""
        model = self.__class__.__name__
        return "[{}] ({}) {}".format(model, self.id, self.__dict__)

    def save(self):
        """save the object in the database"""
        self.updated_at = datetime.utcnow().astimezone(pytz.timezone('Africa/Lagos'))
        models.storage.new(self)
        models.storage.save()

    def new(self):
        """Add an object to the db session"""
        models.storage.new(self)

    def to_dict(self):
        """Convert object to dictionary representation"""
        obj = self.__dict__.copy()
        if obj['updated_at']:
            obj['updated_at'] = obj['updated_at'].isoformat()
        if obj.get('_sa_instance_state'):
            del obj['_sa_instance_state']
        obj['created_at'] = obj['created_at'].isoformat()
        obj['class_name'] = self.__class__.__name__
        return obj
