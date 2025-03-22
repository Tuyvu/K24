import grpc
import calculator_pb2
import calculator_pb2_grpc
from concurrent import futures

class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        return calculator_pb2.AddResponse(result=request.a + request.b)

    def Subtract(self, request, context):
        return calculator_pb2.SubtractResponse(result=request.a - request.b)

    def Multiply(self, request, context):
        return calculator_pb2.MultiplyResponse(result=request.a * request.b)

    def Divide(self, request, context):
        if request.b == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Không thể chia cho 0")
            return calculator_pb2.DivideResponse(result=0)
        return calculator_pb2.DivideResponse(result=request.a / request.b)
def StreamAdd(self, request_iterator, context):
    total = 0
    for request in request_iterator:
        total += request.a + request.b
    return calculator_pb2.AddResponse(result=total)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
    # server.add_insecure_port("[::]:50051")
    server_credentials = grpc.ssl_server_credentials(((open("server.key").read(), open("server.crt").read()),))
    server.add_secure_port("[::]:50051", server_credentials)
    print("Server đang chạy trên cổng 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()