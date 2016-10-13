# djangorest-boilerplate

[use http://forge.fwd.wf/ not https]

1. to get token (login):
    ```bash
    curl -X POST -d \
    "client_id=GwTf8YnLb4giiPa3mhEpj1MwfKN9HFUYL6yGwpXw& \
    client_secret=Fwb9AgayN7RN5Gn3HlwKebw2XZS2jSvMP7yZHTNs8HYyzK9l0wiaecpm8PY9DsBX7urL2w8L0UYw14j2A7bIRZqrqyeiUatvw3ccWf81bR904SMt056OAE5FUK0edqi8& \
    grant_type=password& \
    username=gdasu@alumni.stanford.edu&password=nidna88" \
    http://shutter1.us-west-2.elasticbeanstalk.com/auth/token
    
    Response:
    {
    "access_token": "5wUrM95jYpLmYGa6jDyyzhoyKgBDKH", 
    "token_type": "Bearer", 
    "expires_in": 36000, 
    "refresh_token": "G7WiEyFSeCvb6UrHIsozpA9YFYsva5", 
    "scope": "read write"
    }
    ```

2. to get the uid given the access token (login):
    ```bash
    curl -X GET -H "Authorization: Django goqWy84UfcYKhwmVoviSKtC8uiW8im" http://localhost:8000/djoser-auth/me/
    Response:
    {
    "email":"govinda@govindadasu.com",
    "id":23,
    "username":"govinda@govindadasu.com"
    }
    ```
    
3. accessing an unprotected url:

    ```bash
    curl http://localhost:8000/api/users/
    Response: 
    {"count":4,
    "next":null,
    "previous":null,
    "results":[
        {"url":"http://localhost:8000/api/users/4/","username":"govinda1","email":"gdasu@stanford.edu","groups":[]},
        {"url":"http://localhost:8000/api/users/3/","username":"govinda","email":"gdasu@alumni.stanford.edu","groups":[]},
        {"url":"http://localhost:8000/api/users/2/","username":"admin2a","email":"gdasu@alumni.stanford.edu","groups":[]},
        {"url":"http://localhost:8000/api/users/1/","username":"admin","email":"govinda@govindadasu.com","groups":[]}
        ]
      }
    ```
4. accessing a protected url:
    ```bash
    curl -X PATCH -H "Authorization: Django 5wUrM95jYpLmYGa6jDyyzhoyKgBDKH" -d 'first_name=Govinda1&last_name=Dasu1' http://localhost:8000/api/users/5/
    Response: 
    {
    "url":"http://localhost:8000/api/users/5/",
    "first_name":"Govinda1",
    "last_name":"Dasu1",
    "email":"info@learningdollars.com",
    "groups":[]
    }
    
    curl -X DELETE -H "Authorization: Django 5wUrM95jYpLmYGa6jDyyzhoyKgBDKH" http://localhost:8000/api/users/5/
    Response:  [no response]
    ```

5. fb login (generate token through https://developers.facebook.com/tools/accesstoken/)
    ```bash
    curl -X POST -d "grant_type=convert_token& \ 
    client_id=GwTf8YnLb4giiPa3mhEpj1MwfKN9HFUYL6yGwpXw& \
    client_secret=Fwb9AgayN7RN5Gn3HlwKebw2XZS2jSvMP7yZHTNs8HYyzK9l0wiaecpm8PY9DsBX7urL2w8L0UYw14j2A7bIRZqrqyeiUatvw3ccWf81bR904SMt056OAE5FUK0edqi8& \
    backend=facebook&\
    token=CAAGZBzIcBZBRcBAPZCZAZAWlMPjZC0R2ZCUCPwn12NfDi0dAUs2h1LgUnxkkn8sKyILdCfNpBROKogXimr8RfqoQMflpL1k2JZAj1jI2f4vJZBeH7CqfvSTnE7Y1cY
    Wwwt1n5NZArCh3RZAZBy9mZBhYmyJgMeU9GmMb3ySKFCZC5JAm6cU6mjsIDwqydjscp3qpmN6WHOBXEPqQAEw7Q3C6sTjVw1" 
    http://localhost:8000/auth/convert-token
    
    Response:
    {
    "access_token": "HhePUo1jpIknAMLG6c74JmYvEiISB7", 
    "token_type": "Bearer", 
    "expires_in": 36000, 
    "refresh_token": "zxLQePhrL9eXi5FhzKIWNJGlloLToX", 
    "scope": "read write"
    }
    ```
6. google login (generate token through http://forge.fwd.wf/googlesignin/)

    ```bash
    curl -X POST -d "grant_type=convert_token& \
    client_id=GwTf8YnLb4giiPa3mhEpj1MwfKN9HFUYL6yGwpXw& \
    client_secret=Fwb9AgayN7RN5Gn3HlwKebw2XZS2jSvMP7yZHTNs8HYyzK9l0wiaecpm8PY9DsBX7urL2w8L0UYw14j2A7bIRZqrqyeiUatvw3ccWf81bR904SMt056OAE5FUK0edqi8& \
    backend=google-oauth2&token=ya29.nQIoJn-jsUfWJgon_t_BIyd1XQLJ99wFWAWr0za-RQCRXL0J0j_W5uTmVQKSks5MUh8" \                
    http://localhost:8000/auth/convert-token
    
    {
    "access_token": "MaSxkeklBaehU5x1FOn6Tnt4Mqfq01", 
    "token_type": "Bearer", 
    "expires_in": 36000, 
    "refresh_token": "1SeomBSeY1wD3rvKD5rh4Rx7Bp4QBY", 
    "scope": "read write"
    }
    ```
7. refresh token -- use http://jeremymarc.github.io/2014/08/14/oauth2-with-angular-the-right-way/ on the front end
    
    ```bash
        curl -X POST -d "grant_type=refresh_token& \
        client_id=GwTf8YnLb4giiPa3mhEpj1MwfKN9HFUYL6yGwpXw& \
        client_secret=4UrBWZwNcYVhd1y9XTKr2zu9IlZeb67H5vShIxJ4wh26zCXEIMGrmKVPz9Kfni1Y0NfEdug5GMaZaVVmxHjKB54tBHfKCYGTuCFDmDuuQw7l20lE7TW
        djCi
        ntnIjNpVZ& \
        refresh_token=M81BWw9htRzdXv0hLWJmoY9P7eCBkD" http://localhost:8000/auth/token
    ```
    
8. register new user (activated even before link in email clicked??)
    ```bash
        curl -X POST -d 'username=info@learningdollars.com&email=info@learningdollars.com&password=govinda5'
        http://localhost:8000/djoser-auth/register/
    ```
    [note username must be same as email]

9. change registered user's password
    [to send the email which contains the password change link]
    ```bash
        curl -X POST -d 'email=info@learningdollars.com' http://localhost:8000/djoser-auth/password/reset/
    ```
    
    [after clicking on the password change link (which is of form djoser-auth/password/reset/confirm/{uid}/{token}) you should go to a new page where you are provided with a form to fill in the new password ... pressing submit on that form should trigger the following post request:]
    
    ```bash
        curl -X POST -d 'uid=MjU&token=462-812da3160ac2a9fbef46&new_password=gobi' 
        http://localhost:8000/djoser-auth/password/reset/confirm/
    ```