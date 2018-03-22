# soundcloudscraper
# Runs test scrape.
docker-compose up -d

docker exec -it scrapy /bin/bash

cd scrape_app

python

import scripts

scripts.crawl('test')

# View database through exposed port 5432 or:

docker exec -it database psql -U postgres

/c soundcloud

/dt

from names of tables:
COPY *name* TO /tmp/*name*.csv CSV HEADER

csv file will appear in ./database/files
