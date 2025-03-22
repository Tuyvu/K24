import grpc
import calculator_pb2
import calculator_pb2_grpc

def run():
    channel_credentials = grpc.ssl_channel_credentials(open("server.crt").read())
    channel = grpc.secure_channel("localhost:50051", channel_credentials)
    # channel = grpc.insecure_channel("localhost:50051")
    stub = calculator_pb2_grpc.CalculatorStub(channel)

    # a, b = 10, 5

    # print(f"{a} + {b} = {stub.Add(calculator_pb2.AddRequest(a=a, b=b)).result}")
    # print(f"{a} - {b} = {stub.Subtract(calculator_pb2.SubtractRequest(a=a, b=b)).result}")
    # print(f"{a} * {b} = {stub.Multiply(calculator_pb2.MultiplyRequest(a=a, b=b)).result}")
    # print(f"{a} / {b} = {stub.Divide(calculator_pb2.DivideRequest(a=a, b=b)).result}")

    def request_generator():
        requests = [
            calculator_pb2.AddRequest(a=2, b=3),
            calculator_pb2.AddRequest(a=4, b=5),
            calculator_pb2.AddRequest(a=10, b=20)
        ]
        for req in requests:
            yield req 

    try:
        response = stub.Add(calculator_pb2.AddRequest(a=10, b=5), timeout=3)
        print(response.result)
    except grpc.RpcError as e:
        print(f"Lỗi: {e.code()} - {e.details()}")
if __name__ == "__main__":
    run()
