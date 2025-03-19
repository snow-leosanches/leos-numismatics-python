from decouple import config
# Option 1
# from snowplow_tracker import Snowplow, EmitterConfiguration, Subject, TrackerConfiguration
# Option 2
from snowplow_tracker import Tracker, Emitter, AsyncEmitter, Subject, PageView, SelfDescribing, SelfDescribingJson

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
    # on_success=lambda payloads: logger.info(payloads),
    # on_failure=lambda errorCode, payloads: logger.error(f"Failure: {errorCode}, {payloads}")
)
tracker = Tracker(
    namespace="leos-numismatics-python", 
    app_id="leos-numismatics-python",
    emitters=emitter)