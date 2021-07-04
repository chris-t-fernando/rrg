import os
import boto3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.orm').setLevel(logging.INFO)

# handler for pulling config from SSM
def getSSMParameter(ssm, parameterPath, encryptionOption=False):
    return ssm.get_parameter(Name=parameterPath, WithDecryption=encryptionOption).get('Parameter').get('Value')
# FIX THIS - dunno why proxies are messing this up, but getting SSL errors 4/07/21
ssmClient = boto3.client('ssm', verify=False)

host = getSSMParameter(ssmClient, '/rrg-creator/rds-endpoint')
user = getSSMParameter(ssmClient, '/rrg-creator/rds-user')
password = getSSMParameter(ssmClient, '/rrg-creator/rds-password', True)
database = getSSMParameter(ssmClient, '/rrg-creator/rds-database')

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://'+user+':'+password+'@'+host+':3306'+'/'+database

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()