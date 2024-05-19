### create venv
python3 -m venv venv
----
### activate venv
source venv/bin/activate
---
### deactivate venv
deactivate
---
### install deps from req.txt
pip install -r requirements.txt
---
- if the package is in accordance with the manifest:
    - show nothing 
- else show total no. of packages that are:
    - strictly not compatible 
    - loosely not compatible 
    - do not have licenses

----
