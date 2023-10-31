import pandas as pd
import re
from ambra_sdk.api import Api
from sqlalchemy import create_engine, URL



db_url = URL.create(
 

)

db = create_engine(db_url)
table = "ambra_mri_export_de-identified"

#site = 'D3b CBTN Orlando Health Arnold Palmer Hospital - Deidentified'
#phi_namespace='31216709-9f43-488f-83c0-a5184b91a061'
#phi_namespace='bfacdf34-0ada-4cbc-a5a3-8b808e5d4418'


url = 'https://choparcus.ambrahealth.com/api/v3/'
username= # expects these environment variables
password= # expects these environment variables

api = Api.with_creds(url, username, password)

# **************** FIND ALL ACCESSION NUMBERS *************
# find all studies



query_object = api \
              .Study \
              .list() \
              .all()
             

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
         

     ])
columns = [
           'sdg_id',
           'patient_age',
           'patient_sex',
           'modality',
           'image_count',
           'uploaded_date'
         
        ]

out_df = pd.DataFrame(study_list,columns=columns)

# ****** add in age-in-days-at-imaging ****************

out_df['uploaded_date'] = pd.to_datetime(out_df['uploaded_date']).dt.strftime('%Y%m%d')
out_df['uploaded_date'] = pd.to_datetime(out_df['uploaded_date'])



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
