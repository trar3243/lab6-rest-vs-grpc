#!/usr/bin/env python3

# Adapted from the gRPC Python examples:
#   https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
#   https://grpc.io/docs/tutorials/basic/python/

from concurrent import futures
import argparse
import base64
import io

import grpc
from PIL import Image

import my_proto_pb2 as proto 
import my_proto_pb2_grpc


class Lab6Servicer(my_proto_pb2_grpc.Lab6Servicer):

    def Add(self, request, context):
        # request is an addRequest; return an addResponse
        response = proto.addResponse() 
        response.c = (request.a + request.b)

        return response 

    def RawImage(self, request, context):
        # request is a rawImageRequest; return an imageResponse
        response = proto.imageResponse()
        try:
          ioBuffer = io.BytesIO(request.img)
          img = Image.open(ioBuffer)
        except Exception as e:
          # context.abort raises, so nothing below runs on bad input
          context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Could not decode image: {e}")
        response.width = img.size[0]
        response.height = img.size[1]
        return response 

    def DotProduct(self, request, context):
        # request is a dotProductRequest; return a dotProductResponse
        a = request.a
        b = request.b
        if(len(a) != len(b)):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "A and B input to dotproduct are not of same size")
        c = sum([item_a * item_b for (item_a, item_b) in zip(a,b)])

        response = proto.dotProductResponse() 
        response.dotproduct = c 
        return response 

    def JsonImage(self, request, context):
        # request is a jsonImageMsg; return an imageResponse
        try:
          img_bytes = base64.b64decode(request.img)
          img = Image.open(io.BytesIO(img_bytes))
        except Exception as e:
          context.abort(grpc.StatusCode.INVALID_ARGUMENT, f"Could not decode image: {e}")

        response = proto.imageResponse() 

        response.width = img.size[0]
        response.height = img.size[1] 
        return response 


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='gRPC server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=50051,
        help='Port on which to run the server (default: 50051)'
    )

    args = parser.parse_args()

    # Start gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_proto_pb2_grpc.add_Lab6Servicer_to_server(Lab6Servicer(), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    print(f"gRPC server listening on port {args.port}")
    server.wait_for_termination()
