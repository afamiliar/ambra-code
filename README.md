# Ambra code
The included tools are intended for interfacing with the Ambra Health platform for imaging (radiology) studies, utilizing the Ambra SDK which calls the Ambra API. Requires the user to have the appropriate permissions on Ambra to perform the given actions.

### Code

The ```ambra_download``` command can be used to download data from Ambra. Based on user input it will download all studies in a given location or a specific study or studies.

For quick review, ```QC_studies.py``` will print the number of unique studies and subjects found for a given bucket.

### Variables
Expected environment variables:

```
AMBRA_USERNAME
      required, user's associated e-mail for Ambra account

AMBRA_PASSWORD
      required, user's associated password for Ambra account
```

For QC_studies.py only:
```
AMBRA_PHI_NAMESPACE
      required, the PHI namespace ID for the given Ambra bucket/project
```

### Inputs for ambra_download
```
download_type
      required, specifies the type of download. Either 'all' (all studies on the instance), 'mrn' (all studies associated with a given patient), or 'accession_number' (one study based on an accession number).

patient_mrn
      required if download_type is 'mrn', the patient MRN to download studies for.

accession_number
      required if download_type is 'accession_number', the accession number of the study to download.

ambra_phi_namespace
      required if download_type is 'all', the Ambra PHI Namepsace defining the source bucket.    
```

### Example usage
```
python3 ambra_download.py --download_type mrn --patient_mrn 012345
```

### Other resources

Ambra-SDK documentation: https://dicomgrid.github.io/sdk-python/index.html

Ambra API documentation: https://uat.dicomgrid.com/api/v3/api.html
