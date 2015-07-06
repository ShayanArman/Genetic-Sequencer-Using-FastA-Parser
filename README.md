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
 chromosome: <str>,
 start: <integer>,
 stop: <integer>
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
     chromosome: <str>,
     start: <integer>,
     stop: <integer>
    },
    {
     chromosome: <str>,
     start: <integer>,
     stop: <integer>
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

Input Parameters: 
chromosome: can take on values (1-22, X, Y)
start: [1,..]
stop: [1, ..]

Rules: 
API only accepts ranges of up to 500 base pairs 
Only accepts positive ranges i.e stop >= start  
