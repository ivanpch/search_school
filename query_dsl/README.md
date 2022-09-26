# Query DSL task

## Deployment

```shell
docker-compose -f ../elastic_kibana_compose.yaml up -d
```

## Usage
```shell
python es_query.py [OPTIONS] COMMAND [ARGS]...

Options:
  --es-host TEXT   ES host.
  --es-index TEXT  ES index name.  [required]
  --limit INTEGER  Limit number of entries in response.
  --help           Show this message and exit.

Commands:
  fuzzy
  geo-distance
  match
  match-all
  multi-match
  range
  term
```

## Examples
### Match all query
```shell
python es_query.py --limit 1 \
       --es-index kibana_sample_data_logs match-all
```
```json
[{'_id': 'ukbNw4EBRet1WwPYR9Zv',
  '_index': 'kibana_sample_data_logs',
  '_score': 1.0,
  '_source': {'agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) '
                       'Gecko/20110421 Firefox/6.0a1',
              'bytes': 6219,
              'clientip': '223.87.60.27',
              'event': {'dataset': 'sample_web_logs'},
              'extension': 'deb',
              'geo': {'coordinates': {'lat': 39.41042861, 'lon': -88.8454325},
                      'dest': 'US',
                      'src': 'US',
                      'srcdest': 'US:US'},
              'host': 'artifacts.elastic.co',
              'index': 'kibana_sample_data_logs',
              'ip': '223.87.60.27',
              'machine': {'os': 'win 8', 'ram': 8589934592},
              'memory': None,
              'message': '223.87.60.27 - - [2018-07-22T00:39:02.912Z] "GET '
                         '/elasticsearch/elasticsearch-6.3.2.deb_1 HTTP/1.1" '
                         '200 6219 "-" "Mozilla/5.0 (X11; Linux x86_64; '
                         'rv:6.0a1) Gecko/20110421 Firefox/6.0a1"',
              'phpmemory': None,
              'referer': 'http://twitter.com/success/wendy-lawrence',
              'request': '/elasticsearch/elasticsearch-6.3.2.deb',
              'response': 200,
              'tags': ['success', 'info'],
              'timestamp': '2022-06-26T00:39:02.912Z',
              'url': 'https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.deb_1',
              'utc_time': '2022-06-26T00:39:02.912Z'}},
 {'_id': 'u0bNw4EBRet1WwPYR9Zv',
  '_index': 'kibana_sample_data_logs',
  '_score': 1.0,
  '_source': {'agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) '
                       'Gecko/20110421 Firefox/6.0a1',
              'bytes': 6850,
              'clientip': '130.246.123.197',
              'event': {'dataset': 'sample_web_logs'},
              'extension': '',
              'geo': {'coordinates': {'lat': 38.58338806, 'lon': -86.46248778},
                      'dest': 'IN',
                      'src': 'US',
                      'srcdest': 'US:IN'},
              'host': 'www.elastic.co',
              'index': 'kibana_sample_data_logs',
              'ip': '130.246.123.197',
              'machine': {'os': 'win 8', 'ram': 3221225472},
              'memory': None,
              'message': '130.246.123.197 - - [2018-07-22T03:26:21.326Z] "GET '
                         '/beats/metricbeat_1 HTTP/1.1" 200 6850 "-" '
                         '"Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) '
                         'Gecko/20110421 Firefox/6.0a1"',
              'phpmemory': None,
              'referer': 'http://www.elastic-elastic-elastic.com/success/james-mcdivitt',
              'request': '/beats/metricbeat',
              'response': 200,
              'tags': ['success', 'info'],
              'timestamp': '2022-06-26T03:26:21.326Z',
              'url': 'https://www.elastic.co/downloads/beats/metricbeat_1',
              'utc_time': '2022-06-26T03:26:21.326Z'}},
 {'_id': 'vEbNw4EBRet1WwPYR9Zw',
  '_index': 'kibana_sample_data_logs',
  '_score': 1.0,
  '_source': {'agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 '
                       '(KHTML, like Gecko) Chrome/11.0.696.50 Safari/534.24',
              'bytes': 0,
              'clientip': '120.49.143.213',
              'event': {'dataset': 'sample_web_logs'},
              'extension': 'css',
              'geo': {'coordinates': {'lat': 36.96015, 'lon': -78.18499861},
                      'dest': 'DE',
                      'src': 'US',
                      'srcdest': 'US:DE'},
              'host': 'cdn.elastic-elastic-elastic.org',
              'index': 'kibana_sample_data_logs',
              'ip': '120.49.143.213',
              'machine': {'os': 'ios', 'ram': 20401094656},
              'memory': None,
              'message': '120.49.143.213 - - [2018-07-22T03:30:25.131Z] "GET '
                         '/styles/main.css_1 HTTP/1.1" 503 0 "-" "Mozilla/5.0 '
                         '(X11; Linux i686) AppleWebKit/534.24 (KHTML, like '
                         'Gecko) Chrome/11.0.696.50 Safari/534.24"',
              'phpmemory': None,
              'referer': 'http://twitter.com/success/konstantin-feoktistov',
              'request': '/styles/main.css',
              'response': 503,
              'tags': ['success', 'login'],
              'timestamp': '2022-06-26T03:30:25.131Z',
              'url': 'https://cdn.elastic-elastic-elastic.org/styles/main.css_1',
              'utc_time': '2022-06-26T03:30:25.131Z'}}]
```
### Geo distance query
```shell
python es_query.py --limit 1 \
       --es-index kibana_sample_data_logs geo-distance \
       --distance 200 --distance-unit km  --lat 38 --lon -86 --geo-field geo.coordinates
```
```json
[{'_id': 'u0bNw4EBRet1WwPYR9Zv',
  '_index': 'kibana_sample_data_logs',
  '_score': 1.0,
  '_source': {'agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) '
                       'Gecko/20110421 Firefox/6.0a1',
              'bytes': 6850,
              'clientip': '130.246.123.197',
              'event': {'dataset': 'sample_web_logs'},
              'extension': '',
              'geo': {'coordinates': {'lat': 38.58338806, 'lon': -86.46248778},
                      'dest': 'IN',
                      'src': 'US',
                      'srcdest': 'US:IN'},
              'host': 'www.elastic.co',
              'index': 'kibana_sample_data_logs',
              'ip': '130.246.123.197',
              'machine': {'os': 'win 8', 'ram': 3221225472},
              'memory': None,
              'message': '130.246.123.197 - - [2018-07-22T03:26:21.326Z] "GET '
                         '/beats/metricbeat_1 HTTP/1.1" 200 6850 "-" '
                         '"Mozilla/5.0 (X11; Linux x86_64; rv:6.0a1) '
                         'Gecko/20110421 Firefox/6.0a1"',
              'phpmemory': None,
              'referer': 'http://www.elastic-elastic-elastic.com/success/james-mcdivitt',
              'request': '/beats/metricbeat',
              'response': 200,
              'tags': ['success', 'info'],
              'timestamp': '2022-06-26T03:26:21.326Z',
              'url': 'https://www.elastic.co/downloads/beats/metricbeat_1',
              'utc_time': '2022-06-26T03:26:21.326Z'}}]
```