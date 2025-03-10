# Leo's Numismatics Store in Python

A cool numismatics store written in Python and FastAPI, demonstrating Snowplow's capabilities.

## Getting Started

Make sure you have at least Python 3 installed.

It's recommended to generate a virtual environment to run this project locally. The following command can easily do it:

```sh
$ python3 -m venv ve
```

This will generate a `ve` folder. The next command depends on your OS:

### Mac/Linux 

```sh
$ source ./ve/bin/activate
```

### Windows

```powershell
$ ./ve/Scripts/activate.ps1
```

After activating your virtual environment, you should pull all the dependent packages:

```sh
$ pip install -r requirements.txt
```

## Running

Before running, it is recommended to create a `.env` file with the information to access your connector. For instance, from `.env.snowplow-micro`:

```ini
SNOWPLOW_COLLECTOR_URI=localhost
SNOWPLOW_COLLECTOR_PROTOCOL=http
SNOWPLOW_COLLECTOR_PORT=9090
```

Use the following command to run this project locally:

```sh
$ fastapi dev main.py
```