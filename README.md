# Goal
Legislative Map for tracking legislation at the state level

# Components
* Django + celery
* Postgres for backend DB
* Ingestor to handle importing scraped data into the two data stores
  * processed: postgres
  * json files for ML: file storage (S3 bucket of Azure equivalent) 
