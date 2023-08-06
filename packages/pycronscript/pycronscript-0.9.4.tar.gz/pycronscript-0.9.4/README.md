# pycronscript
Schedule your Python scripts.

## Getting started
**Install package**

`pip install pycronscript`

**Create config file**

This is created with the first run of `pycronscript` and you can see the path where it is has been created.

**Register your scripts for the scheduled run in config file**

*Note: Scripts must have a '**run**' method!*
```
[custom_name]
path=/home/my_user/foo/bar/my_script.py
each={'minutes': 5} # datetime.timedelta args, but in dict format. Default=1h.
...
```

**Start**

Run again `pycronscript`

## Getting started with *Docker* (example)
**Files needed:**
```
pycronscript_with_docker
├── config.cfg
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── test.py
```

**test.py**
```
def run():
    print('working!')
```

**config.cfg**
```
[test]
path=/usr/app/src/test.py
each={'minutes': 5}
```

**Dockerfile**
```
FROM python:3.11

WORKDIR /usr/app/src
RUN pip install pycronscript
RUN mkdir -p /root/.config/pycronscript
COPY config.cfg /root/.config/pycronscript/config.cfg

# Install your custom requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy scripts
COPY test.py ./
```

**docker-compose.yml**
```
version: '3.4'

services:
  pycronscript:
    build: .
    container_name: pycronscript
    entrypoint: 'pycronscript'
    restart: always
```

**Start**
```
docker-compose up -d
```
