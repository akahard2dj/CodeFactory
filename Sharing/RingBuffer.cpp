#include <iostream>
#include <algorithm>
#include <cstring>
#include <string>
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

int main() {
    RingBuffer rb = RingBuffer(MAX_BUF);

    char chValue[MAX_BUF];
    string strValue = "Hello From Host";
    strcpy(chValue, strValue.c_str());
    rb.write(chValue, strlen(chValue));
    cout << "Host Message   : " << chValue << endl;

    char chRecValue[MAX_BUF];
    rb.read(chRecValue, MAX_BUF);
    cout << "Client Recived : " << chRecValue << endl;

    return 0;
}
