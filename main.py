from decouple import config
from dotenv import load_dotenv
from typing import Union
import logging

from fastapi import FastAPI

# Option 1
# from snowplow_tracker import Snowplow, EmitterConfiguration, Subject, TrackerConfiguration
# Option 2
from snowplow_tracker import Tracker, Emitter, AsyncEmitter, Subject, PageView

import logging
import contextlib
from http.client import HTTPConnection

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def debug_requests_off():
    '''Switches off logging of the requests module, might be some side-effects'''
    HTTPConnection.debuglevel = 0

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False

@contextlib.contextmanager
def debug_requests():
    '''Use with 'with'!'''
    debug_requests_on()
    yield
    debug_requests_off()


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv()
app = FastAPI()

SNOWPLOW_COLLECTOR_URI = config('SNOWPLOW_COLLECTOR_URI')
SNOWPLOW_COLLECTOR_PROTOCOL = config('SNOWPLOW_COLLECTOR_PROTOCOL', default='https')
SNOWPLOW_COLLECTOR_PORT = config('SNOWPLOW_COLLECTOR_PORT', default=80, cast=int)

# Option 1
'''Snowplow.create_tracker(namespace='leos-numismatics-python', endpoint='localhost:9090')
tracker = Snowplow.get_tracker('ns')

tracker.track_page_view('https://leo-numismatics.com', 'example page', 'example title')'''
# Option 2
# emitter = Emitter(endpoint=SNOWPLOW_COLLECTOR_URI, protocol=SNOWPLOW_COLLECTOR_PROTOCOL, port=SNOWPLOW_COLLECTOR_PORT)
emitter = AsyncEmitter(
    endpoint=SNOWPLOW_COLLECTOR_URI, 
    protocol=SNOWPLOW_COLLECTOR_PROTOCOL, 
    port=SNOWPLOW_COLLECTOR_PORT,
    on_success=lambda payloads: logger.info(payloads),
    on_failure=lambda errorCode, payloads: logger.error(f"Failure: {errorCode}, {payloads}")
)
tracker = Tracker(
    namespace="leos-numismatics-python", 
    app_id="leos-numismatics-python",
    emitters=emitter)

# debug_requests_on() # If necessary to debug the requests, enable it.

@app.get("/")
def read_root():
    # This seems deprecated
    tracker.track_page_view("https://leo-numismatics.com", "example page", "Leo's Numismatics - Python")

    page_view = PageView(
        page_url="https://leo-numismatics.com",
        page_title="Leo's Numismatics - Python",
    )
    page_view_result = tracker.track(page_view)
    tracker.flush(False) # Otherwise it doesn't send the event
    logger.info(page_view_result)

    return {
        "Hello": "World",
        "page_view_result": page_view_result
    }
