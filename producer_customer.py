# -*-coding:utf8-*-

__author__ = 'user'

import threading
import time
import Queue
import socket

# 模拟两个队列，设备监听队列和网络监听队列
# Producer为设备监听队列的生产者，网络监听队列的消费者
# Consumer为设备监听队列的消费者，网络监听队列的生产者

net_queue = Queue.Queue()
dev_queue = Queue.Queue()
# mylock = threading.RLock()

import logging

# 配置日志文件格式
logging.basicConfig(level=logging.DEBUG,
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt= '%a, %d %b %Y %H:%M:%S',
                    filename= 'myproject.log',
                    filemode='a')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('127.0.0.1', 9999))
except BaseException:
    print 'can not connect to the local host'

class Producer(threading.Thread):
    def __init__(self,net_que,dev_que,sock):
        threading.Thread.__init__(self)
        self._net_que = net_que
        self._dev_que = dev_que
        self.sock = sock

    def run(self):
        while True:
            str_rec = self.sock.recv(1024)
            if str_rec != '':
                if self._dev_que.qsize() > 100:
                    pass
                else:
                    self._dev_que.put({
                        'from':self.name,
                        'data':str_rec
                    })
                    print '存入 %s 设备监听队列 queue 还有%d' % (str_rec, self._dev_que.qsize())
                # self._dev_que.task_done()

            if self._net_que.qsize():
                net_order = self._net_que.get(timeout=1)
                try:
                    self.sock.send(net_order)
                    print '发送命令 %s，网络监听队列还剩 %d' % (net_order, self._net_que.qsize())
                except BaseException:
                    print '命令 %s 未发送，网络监听队列还剩 %d' % (net_order, self._net_que.qsize())

            time.sleep(0.1)
            print 'the net thread is still working'
            logging.info('the net thread is still working')


class Consumer(threading.Thread):
    def __init__(self,net_que,dev_que):
        threading.Thread.__init__(self)
        self._net_que = net_que
        self._dev_que = dev_que
        self._time = time.time()

    def run(self):
        while True:
            if self._net_que.qsize() > 100:
                pass
            else:
                if time.time() - self._time > 5:
                    self._net_que.put('laoxu')
                    print '存入 laoxu 到网络监听队列'+" queue 还剩%d" % self._net_que.qsize()
                    self._time = time.time()

            if self._dev_que.qsize():
                print '执行命令'+self._dev_que.get(timeout=1).get('data')+' 设备监听队列还剩 %d' % self._dev_que.qsize()

            time.sleep(0.1)
            print 'the device queue is still working'
            logging.info('the device queue is still working')

def test():
    for i in range(5):
        dev_queue.put({'from':threading.current_thread().name,
                       'data':str(i)
                    })
        net_queue.put('xuxubin'+str(i))
        print '%s=>队列' % threading.current_thread().name
    for i in range(1):
        p = Producer(net_queue,dev_queue,s)
        p.start()
    for i in range(1):
        c = Consumer(net_queue,dev_queue)
        c.start()

if __name__ == '__main__':
    test()