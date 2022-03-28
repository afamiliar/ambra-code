# Ambra code
The included scripts are intended for interfacing with the Ambra Health platform for imaging (radiology) studies, utilizing the Ambra SDK which calls the Ambra API.

### Scripts

There is ```download_ambra_studies.py``` for downloading all studies in a bucket, and ```download_by_accession.py``` for downloading studies specified by an accession number (could be easily modified to loop through a list of accession numbers).
Studies get saved locally to zip files, named uniquely by their accession numbers. Requires the user to have download permissions for the bucket.

For quick review, ```QC_studies.py``` will print the number of unique studies and subjects found for a given bucket.

As of now the intended use is for the user to modify variables in the main script & then run it, e.g., ```python3 download_ambra_studies.py```

### Variables
Expected environment variables:

```
AMBRA_USERNAME
      required, user's associated e-mail for Ambra account

AMBRA_PASSWORD
      required, user's associated password for Ambra account
```

#### **download_ambra_studies.py**, **QC_studies.py**
```
AMBRA_PHI_NAMESPACE
      required, the PHI namespace ID for the given Ambra bucket/project
```

#### **download_by_accession.py**
```
STUDY_ACCESSION_NUMBER
      required, the accession number of the study/studies to download
```

### Other resources

Ambra-SDK documentation: https://dicomgrid.github.io/sdk-python/index.html

Ambra API documentation: https://uat.dicomgrid.com/api/v3/api.html
