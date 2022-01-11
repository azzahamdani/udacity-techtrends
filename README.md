
# Step1 Best practice for application

[x] An existing article is retrieved. The title of the article should be recorded in the log line.
[x] A non-existing article is accessed and a 404 page is returned. 
[x] The "About Us" page is retrieved.
[x] A new article is created. The title of the new article should be recorded in the logline.
[x] healthz
[x] metrics

# Step1 corrections

[x] try/except&log logic to handle the missing database.db file.
[x] use, app.logger.error instead of app.logger.info when A non-existing article is accessed and a 404 page is returned. 
[x] implement a dynamic endpoint