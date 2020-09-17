# Datasaur API Client Sample

## Pre-requisite
```
pip3 install -r requirements.txt
```

## API Documentation
API Documentation can be found [here](https://datasaurai.gitbook.io/datasaur/datasaur-apis).

## Export Project
```
python3 export.py https://datasaur.ai <client_id> <client_secret> <project_id> <filename> <export_format> <output_dir>
python3 export.py https://datasaur.ai <client_id> <client_secret> <project_id> datasaur conll_2003 ./output
```

## Create Doc Based Labeling by Using External Files
```
python3 create_project_doc_file_url.py https://datasaur.ai <client_id> <client_secret> <team_id> 
```

## Create Doc Based Labeling by Uploading Files (Simulation Only)
```
python3 create_project_doc.py https://datasaur.ai <client_id> <client_secret> <team_id> <file_count>
```

## Create Row Based Labeling
```
python3 create_project_row.py https://datasaur.ai <client_id> <client_secret> <team_id> <path_to_file>
python3 create_project_row.py https://datasaur.ai <client_id> <client_secret> <team_id> ./sample-files/row-based/bookcover-multiplefiles
```

## Create Token Based Labeling
```
python3 create_project_token.py https://datasaur.ai <client_id> <client_secret> <team_id> <path_to_file>
python3 create_project_token_multiple_files.py https://datasaur.ai <client_id> <client_secret> <team_id> ./sample-files/token-based/multiple-files
```