
# Step1 Best practice for application

## Tasks 
* An existing article is retrieved. The title of the article should be recorded in the log line.
* A non-existing article is accessed and a 404 page is returned. 
* The "About Us" page is retrieved.
* A new article is created. The title of the new article should be recorded in the logline.
* healthz
* metrics

## Correction
* try/except&log logic to handle the missing database.db file.
* use, app.logger.error instead of app.logger.info when A non-existing article is accessed and a 404 page is returned. 
* implement a dynamic endpoint

# Step2 Docker for Application Packaging

## Tasks 
* Dockerfile
* Docker commands 
* Docker-Run-Local screenshot

## Correction
* Dockerfile corrected so that `docker build -t techtrends -f ./Dockerfile .` works

# Step3 Continuous Integration with GitHub Actions

## Tasks 
* Workflow techtrends-dockerhub.yml
* CI-github-action screenshot
* CI-dockerhub screenshot