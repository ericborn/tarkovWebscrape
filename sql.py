# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 17:31:06 2019

@author: Eric Born
"""
from sqlalchemy import create_engine, MetaData, insert, Table, Column, String, Integer, Float, Boolean
meta = MetaData()

# Creates a connection string
engine = create_engine('postgresql://TomBrody:pass@localhost/tarkov')

# Automatically reflects the database table and stores the column types and details
weaponProperties = Table('weaponproperties', meta, autoload = True, autoload_with = engine)

# Selects all tables in the db
#print(engine.table_names())

# Maps out the insert statement
ins = weaponProperties.insert()

str(ins)

weaponDF.to_sql(weaponProperties, con = engine, if_exists = 'append')

print(weaponDF.iloc[1,:])


result = table.update().returning()

stmt = insert(weaponProperties('weaponProperties'))




