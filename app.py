import javax.jws.WebService;

@WebService
public class HelloService {
    public String sayHello(String name) {
        return "Hello " + name + ", Welcome to SOAP Web Service";
    }
}
import javax.xml.ws.Endpoint;

public class HelloPublisher {
    public static void main(String[] args) {
        Endpoint.publish("http://localhost:8080/hello", new HelloService());
        System.out.println("SOAP service running...");
    }
}
-------------------------------------------------------------------------
-------------------------------------------------------------------------
from flask import Flask

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello from REST API"

if __name__ == '__main__':
    app.run(debug=True)
-------------------------------------------------------------------------
-------------------------------------------------------------------------
from multiprocessing import Process, Pipe

def child(conn):
    msg = conn.recv()
    print("Child received:", msg)
    conn.send(msg.upper() + " from child")

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()

    p = Process(target=child, args=(child_conn,))
    p.start()

    parent_conn.send("hello child")
    print("Parent received:", parent_conn.recv())

    p.join()
-------------------------------------------------------------------------
-------------------------------------------------------------------------
from multiprocessing import Process, Queue
import time

def worker(id, task_q, result_q):
    while True:
        task = task_q.get()
        if task is None:
            break
        time.sleep(1)
        result_q.put(f"Task {task} done by worker {id}")

if __name__ == "__main__":
    task_q = Queue()
    result_q = Queue()

    workers = []
    for i in range(3):
        p = Process(target=worker, args=(i, task_q, result_q))
        p.start()
        workers.append(p)

    for i in range(5):
        task_q.put(i)

    for _ in workers:
        task_q.put(None)

    for _ in range(5):
        print(result_q.get())

    for p in workers:
        p.join()
-------------------------------------------------------------------------
-------------------------------------------------------------------------
5. Message-Oriented Communication (Request/Reply)
from multiprocessing import Process, Queue

def server(req_q, res_q):
    while True:
        req = req_q.get()
        if req == "STOP":
            break
        cid, msg = req
        res_q.put((cid, msg[::-1]))

def client(cid, req_q, res_q):
    req_q.put((cid, "hello"))
    while True:
        rcid, resp = res_q.get()
        if rcid == cid:
            print(f"Client {cid} got:", resp)
            break

if __name__ == "__main__":
    req_q = Queue()
    res_q = Queue()

    Process(target=server, args=(req_q, res_q)).start()

    for i in range(3):
        Process(target=client, args=(i, req_q, res_q)).start()
___________________________________________________________________________
---------------------------------------------------------------------------
6. Publish/Subscribe Simulation (Threading)
import threading, queue

class Broker:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, q):
        self.subscribers.setdefault(topic, []).append(q)

    def publish(self, topic, msg):
        for q in self.subscribers.get(topic, []):
            q.put(msg)

def subscriber(name, broker, topic):
    q = queue.Queue()
    broker.subscribe(topic, q)
    while True:
        msg = q.get()
        if msg == "STOP":
            break
        print(name, "received:", msg)

def publisher(broker, topic):
    for msg in ["Hello", "World"]:
        broker.publish(topic, msg)

broker = Broker()

threading.Thread(target=subscriber, args=("A", broker, "news")).start()
threading.Thread(target=publisher, args=(broker, "news")).start()
--------------------------------------------------------------------
------------------------------------------------------------------------
7.RabbitMQ (Distributed IPC Pub/Sub)
PIP INSTALL PIKA
import pika

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()

ch.exchange_declare(exchange='logs', exchange_type='fanout')
result = ch.queue_declare('', exclusive=True)
queue = result.method.queue

ch.queue_bind(exchange='logs', queue=queue)

def callback(ch, method, properties, body):
    print("Received:", body.decode())

ch.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
ch.start_consuming()
#sender second progam

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
ch = conn.channel()

ch.exchange_declare(exchange='logs', exchange_type='fanout')

ch.basic_publish(exchange='logs', routing_key='', body='Hello RabbitMQ')
print("Sent")

conn.close()


-----------------------------------------------------------------
------------------------------------------------------------------
8. ZeroMQ (ØMQ Pub/Sub)
Subscriber
pip install pyzmq
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
    msg = socket.recv_string()
    print("Received:", msg)
    
    
    Publisher
import zmq, time

context = zmq.Context()
socket = context.socket(zmq.PUB)

socket.bind("tcp://127.0.0.1:5555")

while True:
    socket.send_string("Hello ZeroMQ")
    time.sleep(1)
