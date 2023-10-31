
import pandas as pd
import re
from ambra_sdk.api import Api
from sqlalchemy import create_engine, URL


#### Database and Table Credentials ######

db_url = os.getenv("D3B_WAREHOUSE_DB_URL")
db = create_engine(db_url)
table = "ambra_mri_export_de-identified"

######### Ambra-SDK ###########

url = 'https://choparcus.ambrahealth.com/api/v3/'
username=  #environment variables
password=  #environment variables

api = Api.with_creds(url, username, password)

# **************** FIND ALL ACCESSION NUMBERS *************
# find all studies
query_object = api \
              .Study \
              .list() \
              .all()
             

study_list = []
for study in query_object:
    if ('Identified' in study['phi_namespace_name']) :
     print(study['phi_namespace_name'])
     study_list.append([study.patientid,
                     study.accession_number,
                     study.phi_namespace_name,
                     study.patient_name,
                     study.patient_age,
                     study.patient_sex,
                     study.patient_birth_date,
                     study.modality,
                     study.image_count,
                     study.referring_physician,
                     study.study_description,
                     study.study_date,
                     study.created  ])

columns = ['mrn',
           'accession_number',
           'phi_namespace_name',
           'name',
           'patient_age',
           'patient_sex',
           'patient_birth_date',
           'modality',
           'image_count',
           'referring_physician',
           'study_description',
           'study_date',
           'created'
        ]

out_df = pd.DataFrame(study_list,columns=columns)

# ****** add in age-in-days-at-imaging ****************
out_df['patient_birth_date'] = pd.to_datetime(out_df['patient_birth_date']).dt.strftime('%Y%m%d')
out_df['study_date'] = pd.to_datetime(out_df['study_date']).dt.strftime('%Y%m%d')
out_df['patient_birth_date'] = pd.to_datetime(out_df['patient_birth_date'])
out_df['study_date'] = pd.to_datetime(out_df['study_date'])
out_df['created'] = pd.to_datetime(out_df['created']).dt.strftime('%Y%m%d')
out_df['created'] = pd.to_datetime(out_df['created'])
out_df['age_in_days'] = (out_df['study_date'] - out_df['patient_birth_date']).dt.days


############ Load data from Ambra to Database table ############

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
