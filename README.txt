Here is some info how to use the project:

1. before you start scrapper, you need to run 'test_service_output_request.py' module to mock margin saver*
2. in order to start scrapper you need to run 'go_spider.py'
3. you can either run the scrapper once or in time intervals (look at comments in 'go_spider.py')
4. the place where the scrapping 'starts' is '__init__' and 'start_requests' in 'website_spider.py'
5. before sending data to 'test_service_output_request.py' (that mocks margin saver) data is prepared, eg. empty fields
are removed, and validated for wrong output

*to integrate with margin saver change URL in 'process_item()' method of 'pipelines.py' module - scrapper/pipelines.py:37