# API Requirement

## Services
* Create Input Stream
* Send camera frames (API will put message on topic queue)
* Get Annotatated data (data only)
  * Get Annotated frames (Data and can frame can be embedded both in same message and be filled depending on request)
* Check MQ status (Receive Ready, Messages available, reason)

## Messages
* Create input stream <-> input stream response
* Send Camera Frame <-> Received Frame response (Response from stream and application)
* Request Annotated data (Data/frame/Both) <-> Annotated data response
* Status request <-> status response
