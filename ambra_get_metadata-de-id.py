import pandas as pd
import re

from ambra_sdk.api import Api
from ambra_sdk.models import Study
from sqlalchemy import create_engine, URL
from datetime import datetime
from ambra_sdk.models import Account


db_url = URL.create(
    "postgresql",
    username="viswanathk",
    password="b3sis1UzGiMcFf4u",  # plain (unescaped) text
    host="d3b-warehouse-aurora.cluster-cxxdzxepyea2.us-east-1.rds.amazonaws.com",
    database="postgres",

)

db = create_engine(db_url)
table = "ambra_mri_export_de-identified"

#site = 'D3b CBTN Orlando Health Arnold Palmer Hospital - Deidentified'
#phi_namespace='31216709-9f43-488f-83c0-a5184b91a061'
#phi_namespace='bfacdf34-0ada-4cbc-a5a3-8b808e5d4418'


url = 'https://choparcus.ambrahealth.com/api/v3/'
username='viswanathk@chop.edu' # expects these environment variables
password='S@iram1989' # expects these environment variables

api = Api.with_creds(url, username, password)

# **************** FIND ALL ACCESSION NUMBERS *************
# find all studies



query_object = api \
              .Study \
              .list() \
              .all()
              #.filter_by(Study.phi_namespace == phi_namespace)  \
              #.all()

study_list = []
for study in query_object:
    if ('Deidentified' in study['phi_namespace_name']) :
     print(study['phi_namespace_name'])
     study_list.append([

         study.patient_name,
         study.patient_age,
         study.patient_sex,
         study.modality,
         study.image_count,
         study.created
         #datetime.strptime(study.study_date, '%Y%m%d') - datetime.strptime(study.patient_birth_date, '%Y%m%d')

     ])
columns = [
           'sdg_id',
           'patient_age',
           'patient_sex',
           'modality',
           'image_count',
           'uploaded_date'
           #'age_in_days'
        ]

out_df = pd.DataFrame(study_list,columns=columns)

# ****** add in age-in-days-at-imaging ****************

out_df['uploaded_date'] = pd.to_datetime(out_df['uploaded_date']).dt.strftime('%Y%m%d')
out_df['uploaded_date'] = pd.to_datetime(out_df['uploaded_date'])
#out_df['age_in_days'] = (out_df['age_in_days']).dt.days
#out_df.to_csv(f'all_study_information.csv',index=False)


if out_df.all:
    rex = re.compile(r"(?<!_)(?=[A-Z])")
    df = (
        pd.DataFrame(out_df)
        .rename(columns=lambda x: x.replace(".", "_"))  # avoid "." in colnames
        .rename(columns=lambda x: rex.sub("_", x).lower())  # camelcase to snake
    )
    print(f"Submitting {len(df)} records to the '{table}' table in {repr(db.url)}...")
    df.to_sql(
        table, db, schema="ambra", index=False, if_exists="replace", chunksize=10000, method="multi"
    )
    # df.to_csv('fw_export_test_FINAL_ms.csv', index=False)
    # with db.connect() as conn:
    # conn.execute(f"GRANT SELECT ON {table} TO public")
else:
    print("No files found")
