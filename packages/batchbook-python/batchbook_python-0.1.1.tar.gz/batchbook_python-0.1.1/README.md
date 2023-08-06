# Batchbook-python
Batchbook API wrapper written in python.

## Installing
```
pip install batchbook-python
```

## Usage
### Simple access with API KEY
```
from batchbool.client import Client

client = Client('API_KEY')
```

Get Contacts
```
client.get_contacts()
```

Get an specific contact
```
client.get_contact(contact_id)
```
## Requirements

```
-Requests
-Urllib
```

## TODO
- Companies
- Custom Fields
- Users
- Roles
- Communications
