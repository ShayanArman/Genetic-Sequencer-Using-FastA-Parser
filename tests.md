Sample Request(1):
------------ 
```shell
curl -H 'Accept: application/json; indent=4' -X POST -d '[{"chromosome":"3","start":"1", "stop":"1"}, {"chromosome":"22","start":"38000900", "stop":"38000910"}]' http://127.0.0.1:8000/geneticapi/get_genetic_info
```

Sample Response:
-------------
```javascript
[{"genetic_sequence": "N"}, {"genetic_sequence": "GAGATGGGGTT"}]
```

Sample Request(2):
------------ 
```shell
curl -H 'Accept: application/json; indent=4' -X POST -d '[{"chromosome":"X","start":"1", "stop":"1"}, {"chromosome":"Y","start":"380000900", "stop":"380000910"}]' http://127.0.0.1:8000/geneticapi/get_genetic_info
```

Sample Response:
-------------
```javascript
{"status": 400, "message": "Stop index was greater than the number of base pairs in chromosome Y"}
```

Sample Request(3):
------------ 
```shell
curl -H 'Accept: application/json; indent=4' -X POST -d '[{"chromosome":"3","start":"1", "stop":"1"}, {"chromosome":"22","start":"38000900", "stop":"38000900"}]' http://127.0.0.1:8000/geneticapi/get_genetic_info
```

Sample Response:
-------------
```javascript
[{"genetic_sequence": "N"}, {"genetic_sequence": "G"}]
```

Sample Request(4):
------------ 
```shell
curl -H 'Accept: application/json; indent=4' -X POST -d '[{"chromosome":"3","start":"1", "stop":"1"}, {"chromosome":"22","start":"10", "stop":"-5"}]' http://127.0.0.1:8000/geneticapi/get_genetic_info
```

Sample Response:
-------------
```javascript
{"status": 400, "message": "Start and stop must be greater than 0. Stop must be greater than or equal start."}
```

