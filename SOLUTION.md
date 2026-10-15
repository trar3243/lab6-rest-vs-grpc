# Lab 6 Solution - REST vs gRPC

All times are milliseconds per operation.

|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|
|   REST add	| 2.65 | 3.51 | 321.57 |
|   gRPC add	| 0.83 | 1.29 | 164.31 |
|   REST rawimg	| 5.25 | 8.10 | 1284.75 |
|   gRPC rawimg	| 13.39 | 12.01 | 205.43 |
|   REST dotproduct	| 3.30 | 4.00 | 322.18 |
|   gRPC dotproduct	| 0.91 | 1.37 | 146.23 |
|   REST jsonimg	| 28.53 | 31.31 | 1421.90 |
|   gRPC jsonimg	| 29.03 | 31.11 | 228.45 |
|   PING        | 0.052 | 0.462 | 161.854 |

## Observations
On localhost and within the same zone, network latency (PING of .052 and .462) is mostly negligible. Therefore, for local host and same-zone metrics, performance must be dominated by the software overhead. gRPC was much faster for add and dotproduct (which use small payloads); this is likely because of the requests.post() overhead for REST, which requires the generation of an entirely new connection, while gRPC uses the same connection repeatedly. However, REST was much faster for rawimg. This is likely because a larger payload makes a raw body cheaper than the splitting of the message into many smaller pieces for such a large payload in gRPC. jsonIMG was about equal for both gRPC and REST; I imagine that this is likely because this time (which is much larger in gRPC and REST than their rawimg counterparts) is dominated by the conversion from image to string, and back again. 

Across regions, network latency (PING of 162) begins to dominate the overall time. With a 162 ping, the add method takes about the time of two round trips for REST (162 * 2 = 324 ~= 321) and one round trip for gRPC (162 vs. 164). The tworound trips for the REST add is likely the result of the new TCP connection for each query (requiring a round trip), while gRPC, as mentioned before, reuses a single connection. With the rawImg and jsonimg functions, the gap between gRPC and REST widens. This is again likely caused by gRPC's use of a single connection, while REST uses requests.post() for each, which starts a new connection. The new TCP connection, when starting up, sends data cautiously; when there is a lot of data to send, this means that the data is sent piecemeal, with each piece waiting on the prior piece's acknowledgement. This is called 'slow start' and means that as the amount of data grows, REST requires more and more network communication. gRPC, on the other hand, sends all the data in the single connection. 

In summary, gRPC's advanatage grows with network latency because it pays connection setup once rather than on every call. 
