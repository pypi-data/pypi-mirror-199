# apifonica-client
Unofficial Python Package to easily integrate the [Apifonica](https://www.apifonica.com/) API to your project.

> Note: Currently this only supportings sending SMS messages. Other api endpoints will be implemented over time.


## Installation

apifonica-client is available on PyPi:

```
$ python -m pip install ApifonicaClient
```


## Usage

```
from apifonica_client import ApifonicaClient

apifonica = ApifonicaClient(
    apifonica_account_sid="your_account_sid_here",
    apifonica_auth_token="your_auth_token_here",
    apifonica_number_from="your_phone_number_here"
)

apifonica.send_sms("1234567890", "Hello, world!")
```
