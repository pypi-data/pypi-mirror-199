import requests
import traceback
from ratelimit import limits, sleep_and_retry

class RateLimitedRequests:
  __CALLS_PER_MINUTE = 400
  __PERIOD = 60
  
  def __init__(self, cpm, period):
    self.__CALLS_PER_MINUTE = cpm
    self.__PERIOD = period
  
  @sleep_and_retry
  @limits(calls=__CALLS_PER_MINUTE, period=__PERIOD)
  def safe_get(self, **params):
    try:
      r = requests.get(**params)
      return r.json()
    except Exception:
      traceback.print_exc()
      return {}
    
  @sleep_and_retry
  @limits(calls=__CALLS_PER_MINUTE, period=__PERIOD)
  def safe_post(self, **params):
    try:
      r = requests.post(**params)
      return r.json()
    except Exception:
      traceback.print_exc()
      return {}