#!/usr/bin/env python
# -*- coding: utf8 -*-

#导入socket库
import socket

#创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

input_str = ''

#注意参数是一个Tuple
# s.connect(('www.sina.com.cn',80))

# s.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# # 接收数据:
# buffer = []
# while True:
#     # 每次最多接收1k字节:
#     d = s.recv(1024)
#     if d:
#         buffer.append(d)
#     else:
#         break
# data = ''.join(buffer)

# s.close()

# header, html = data.split('\r\n\r\n', 1)
# print header
# # 把接收的数据写入文件:
# with open('sina.html', 'wb') as f:
#     f.write(html)

s.connect(('127.0.0.1', 9999))

print s.recv(1024)

while input_str != 'q':
	input_str = raw_input('please:')
	s.send(input_str)
	print s.recv(1024)
s.send('exit')
s.close()