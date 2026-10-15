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
|   PING        | 0.052 | 0.462 | 141.177 |

## Observations

