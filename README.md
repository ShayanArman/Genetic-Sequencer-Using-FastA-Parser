Overview

This system uses a copy of the reference genome (build GRCh37) found at: https://s3.amazonaws.com/downloads.solvebio.com/sequence/genbank.GRCh37.fa.gz
For the Django project to work, you must download the FastA file and put it in geneticapi/templates/data

This API provides programmatic access to the reference Human genome. (All 24 Chromosomes)
The API endpoint accepts both GET and POST requests.

API: /geneticapi/get_genetic_info 

Request:
--------
Method: GET 
{
 chromosome: (String),
 start: (Integer),
 stop: (Integer)
}

Response: 
--------- 
{
    "genetic_sequence": "AABABA"
}


Request:
--------
Method: POST 
[
    {
     chromosome: (String),
     start: (Integer),
     stop: (Integer)
    },
    {
     chromosome: (String),
     start: (Integer),
     stop: (Integer)
    }
]

Response: 
--------- 
[
    {
        "genetic_sequence": "AABABA"
    },
    {
        "genetic_sequence": "AABABA"
    }
]

Sample Request:
------------ 
```shell
curl -H 'Accept: application/json; indent=4' -X POST -d '[{"chromosome":"3","start":"1", "stop":"1"}, {"chromosome":"22","start":"38000900", "stop":"38000910"}]' http://127.0.0.1:8000/geneticapi/get_genetic_info
```

Sample Response:
-------------
```javascript
[{"genetic_sequence": "N"}, {"genetic_sequence": "GAGATGGGGTT"}]
```

Input Parameters: 
chromosome: can take on values (1-22, X, Y)
start: [1,..]
stop: [1, ..]

Rules: 
API only accepts ranges of up to 500 base pairs 
Only accepts positive ranges i.e stop >= start  
