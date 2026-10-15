#!/usr/bin/env python3

# Adapted from rest-client.py and the gRPC Python examples:
#   https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_client.py
#   https://grpc.io/docs/tutorials/basic/python/

import time
import base64
import random
import argparse

import grpc

import my_proto_pb2 as proto 
import my_proto_pb2_grpc


def doRawImage(stub, debug=False):
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    request = proto.rawImageRequest() 
    request.img = img 
    response = stub.RawImage(request)
    if(debug):
        print(response.width, response.height)


def doAdd(stub, debug=False):
    request = proto.addRequest()
    request.a=5 
    request.b=10 
    response = stub.Add(request) 
    if(debug):
        print(response.c)


def doDotProduct(stub, debug=False):
    a = [random.random() for i in range (100)]
    b = [random.random() for i in range (100)]
    
    request = proto.dotProductRequest() 

    request.a.extend(a) 
    request.b.extend(b) 

    response = stub.DotProduct(request)

    if(debug):
      print(response.dotproduct)
    

def doJsonImage(stub, debug=False):
    # build a jsonImageMsg, call stub.JsonImage, print reply if debug
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    img_base64 = base64.b64encode(img).decode('utf-8') # https://docs.python.org/3/library/base64.html#base64.b64encode
    request = proto.jsonImageMsg()
    request.img = img_base64

    response = stub.JsonImage(request)
    if(debug):
      print(response.width, response.height) 


# ---------------------------------------------------------
# Parse command-line arguments
# ---------------------------------------------------------

parser = argparse.ArgumentParser(
    description='gRPC client for measuring server operations'
)

parser.add_argument(
    'host',
    help='IP address or hostname of the gRPC server'
)

parser.add_argument(
    'cmd',
    choices=['add', 'rawImage', 'dotProduct', 'jsonImage'],
    help='Operation to perform'
)

parser.add_argument(
    'reps',
    type=int,
    help='Number of repetitions for measurement'
)

parser.add_argument(
    '-p', '--port',
    type=int,
    default=50051,
    help='Server port (default: 50051)'
)

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help='Print the response from the server'
)

args = parser.parse_args()


# ---------------------------------------------------------
# Connect to server (one channel, reused for every rep)
# ---------------------------------------------------------

addr = f"{args.host}:{args.port}"
channel = grpc.insecure_channel(addr)
stub = my_proto_pb2_grpc.Lab6Stub(channel)

print(f"Running {args.reps} reps against {addr}")


# ---------------------------------------------------------
# Perform requested operation
# ---------------------------------------------------------

if args.cmd == 'rawImage':

    start = time.perf_counter()

    for x in range(args.reps):
        doRawImage(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")


elif args.cmd == 'add':

    start = time.perf_counter()

    for x in range(args.reps):
        doAdd(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")


elif args.cmd == 'jsonImage':

    start = time.perf_counter()

    for x in range(args.reps):
        doJsonImage(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")


elif args.cmd == 'dotProduct':

    start = time.perf_counter()

    for x in range(args.reps):
        doDotProduct(stub, debug=args.debug)

    delta = ((time.perf_counter() - start) / args.reps) * 1000
    print("Took", delta, "ms per operation")
