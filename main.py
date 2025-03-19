
from typing import Union
import logging

from fastapi import FastAPI
from faker import Faker

import logging
import contextlib
from http.client import HTTPConnection

from snowplow_tracker import PageView, SelfDescribing, SelfDescribingJson
from dependencies.snowplow_tracker import tracker

fake = Faker()

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

app = FastAPI()

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

@app.get("/self-describing")
def read_page():
    url = fake.uri()
    self_describing = SelfDescribing(
        SelfDescribingJson(
            "iglu:com.snowplowanalytics.self-desc/schema/jsonschema/1-0-0",
            {
                "targetUrl": url
            },
        ),
    )

    tracker.track(self_describing)
    tracker.flush(False)

    return {
        "url": url
    }
