#include <iostream>
#include <algorithm>
#include <cstring>
#include <string>
#include <vector>
#include <queue>
#include <functional>
#include <condition_variable>
#include <thread>
#define MAX_BUF 1024
using namespace std;

class RingBuffer {
public:
    RingBuffer(size_t capacity);
    ~RingBuffer();
    size_t size() const { return _size; }
    size_t capacity() const { return _capacity; }
    size_t write(const char *data, size_t bytes);
    size_t read(char *data, size_t bytes);
private:
    size_t _begin_index, _end_index, _size, _capacity;
    char *_data;
};

RingBuffer::RingBuffer(size_t capacity) {
    _begin_index = 0;
    _end_index = 0;
    _size = 0;
    _capacity = capacity;
    _data = new char[capacity];
}

RingBuffer::~RingBuffer() {
    delete [] _data;
}

size_t RingBuffer::write(const char *data, size_t bytes) {
    if (bytes == 0) return 0;

    size_t capacity = _capacity;
    size_t bytesToWrite = min(bytes, capacity - _size);

    if (bytesToWrite <= capacity - _end_index) {
        memcpy(_data + _end_index, data, bytesToWrite);
        _end_index += bytesToWrite;
        if (_end_index == capacity) _end_index = 0;
    } else {
        size_t size_1 = capacity - _end_index;
        memcpy(_data + _end_index, data, size_1);
        size_t size_2 = bytesToWrite - size_1;
        memcpy(_data, data + size_1, size_2);
        _end_index = size_2;
    }
    _size += bytesToWrite;
    return bytesToWrite;
}
size_t RingBuffer::read(char *data, size_t bytes) {
    if (bytes == 0) return 0;

    size_t capacity = _capacity;
    size_t bytesToRead = min(bytes, _size);

    if (bytesToRead <= capacity - _begin_index) {
        memcpy(data, _data + _begin_index, bytesToRead);
        _begin_index += bytesToRead;
        if (_begin_index == capacity) _begin_index = 0;
    } else {
        size_t size_1 = capacity - _begin_index;
        memcpy(data, _data + _begin_index, size_1);
        size_t size_2 = bytesToRead - size_1;
        memcpy(data + size_1, _data, size_2);
        _begin_index = size_2;
    }
    _size -= bytesToRead;
    return bytesToRead;
}

class ThreadPool {
public:
    ThreadPool(size_t numThreads);
    ~ThreadPool();
    void EnqueueJob(std::function<void()> job);
private:
    size_t _num_threads;
    vector<thread> _worker_threads;
    queue<function<void()>> _jobs;
    condition_variable _cv_job_q;
    mutex _m_job_q;
    bool stop_all;
    void WorkerThread();
};

ThreadPool::ThreadPool(size_t num_threads) {
    _num_threads = num_threads;
    stop_all = false;
    _worker_threads.reserve(_num_threads);
    for (size_t i=0; i<_num_threads; i++)
        _worker_threads.emplace_back([this]() {this->WorkerThread(); });
}

ThreadPool::~ThreadPool() {
    stop_all = true;
    _cv_job_q.notify_all();

    for (auto& t : _worker_threads) {
        t.join();
    }
}
void ThreadPool::WorkerThread() {
    while(true) {
        unique_lock<mutex> lock(_m_job_q);
        _cv_job_q.wait(lock, [this]() {return !this->_jobs.empty() || stop_all; });
        if (stop_all && this->_jobs.empty()) return;

        function<void()> job = move(_jobs.front());
        _jobs.pop();
        lock.unlock();
        job();
    }
}

void ThreadPool::EnqueueJob(function<void()> job) {
    if (stop_all) throw runtime_error("ThreadPool is stopped");

    {
        lock_guard<mutex> lock(_m_job_q);
        _jobs.push(move(job));
    }
    _cv_job_q.notify_one();
}

RingBuffer rb = RingBuffer(MAX_BUF);
size_t writeBytes;

void read_work(int id) {
    char chRecValue[MAX_BUF];
    rb.read(chRecValue, MAX_BUF);
    if (strlen(chRecValue) != writeBytes) {
        cout << "Client Recived : ( " << id << " ) - Failed" << endl;
    } else {
        cout << "Client Recived : ( " << id << " ) - " << chRecValue << endl;
    }
}

int main() {

    char chValue[MAX_BUF];
    string strValue = "Hello From Host";
    strcpy(chValue, strValue.c_str());
    rb.write(chValue, strlen(chValue));
    writeBytes = rb.size();
    cout << "Host Message   : " << chValue << endl;

    ThreadPool pool(3);
    for (int i=0; i<10; i++)
        pool.EnqueueJob([i]() { read_work(i); });
    return 0;
}

/* output 
./ringbuffer_multiplt_thread
Host Message   : Hello From Host
Client Recived : ( Client Recived : ( 0 ) - Hello From Host1 ) - Hello From Host
Client Recived : ( 3 ) - Hello From Host
Client Recived : ( 4 ) - Hello From Host
Client Recived : ( 5 ) - Hello From Host
Client Recived : ( 6 ) - Hello From Host
Client Recived : ( 7 ) - Hello From Host
Client Recived : ( 8Client Recived : (  ) - Hello From Host
2Client Recived : (  ) - Hello From Host9 ) - Hello From Host

*/
