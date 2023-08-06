# import socket
# import time
# import threading

# SERVER_ADDRESS = ('localhost', 12345)
# HEARTBEAT_INTERVAL = 1

# # 定义消息类型
# MESSAGE_TYPE_HEARTBEAT = 0
# MESSAGE_TYPE_DATA = 1

# class MecordSocket:

#     def _loop(self):
#         threading.Timer(HEARTBEAT_INTERVAL, self._heartBeat).start()

#     def __init__(self, cb):
#         self.callback = cb
#         self.is_connecting = False
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     def start(self, count = 5):
#         try:
#             self.sock.connect(SERVER_ADDRESS)
#             self.is_connecting = True
#             print('Connected to server at', SERVER_ADDRESS)
#             self._loop()
#         except (socket.error, ConnectionError) as e:
#             if count > 0:
#                 print('Error:', e)
#                 print('Retrying in 5 seconds...')
#                 threading.Timer(5, self.start, (count-1,)).start()
#             else:
#                 self.is_connecting = False
#                 print('connect fail!')
#         except Exception as e:
#             print('Error:', e)
    
#     def isRunning(self):
#         return self.is_connecting

#     def _heartBeat(self):
#         if self.is_connecting == False:
#             return
        
#         try:
#             # 发送心跳消息
#             heartbeat_msg = b'\x00'  # 使用字节0表示心跳消息
#             self.sock.sendall(heartbeat_msg)
#             print('Sent heartbeat at', time.time())
            
#             # 等待接收消息
#             data = self.sock.recv(1024)
#             if data:
#                 message_type = data[0]
#                 if message_type == MESSAGE_TYPE_DATA:
#                     # 如果收到数据消息，则调用回调函数处理数据
#                     data = data[1:].decode('utf-8')
#                     self.callback(data)
#         except Exception as e:
#             print('Error:', e)
#         self._loop()

#     def sendData(self, data):
#         if self.is_connecting == False:
#             return
        
#         try:
#             data_msg = b'\x01' + data.encode('utf-8')  # 使用字节1表示数据消息
#             self.sock.sendall(data_msg)
#             print('Sent data at', time.time())
#         except Exception as e:
#             print('Error:', e)

#     def close(self):
#         if self.is_connecting == False:
#             return
        
#         try:
#             self.timer.close()
#             print('Closing connection')
#             self.sock.close()
#         except Exception as e:
#             print('Error:', e)
        
