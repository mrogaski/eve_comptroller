from sqlalchemy import Column, Index, ForeignKey, Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    """The primary record for the system user."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(254))
    password = Column(String(128))
    is_admin = Column(Boolean(create_constraint=True))
    last_login = Column(DateTime(timezone=True))


class UserValidation(Base):
    """Base class for sideband validation of user requests."""
    __tablename__ = 'user_validation'
    id = Column(Integer, primary_key=True)
    type = Column(String(16))
    token = Column(String(32))
    timestamp = Column(DateTime(timezone=True))
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'validation'
    }

class UserActivation(UserValidation):
    """Child class for new user e-mail address validation and account activation."""
    name = Column(String(128))
    email = Column(String(254))
    password = Column(String(128))
    
    __mapper_args__ = {
        'polymorphic_identity':'activation'
    }

class UserReset(UserValidation):
    """Child class for password reset."""
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', backref=backref('user_reset', uselist=False))
    
    __mapper_args__ = {
        'polymorphic_identity':'reset'
    }
    
    