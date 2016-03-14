#include <stdio.h>
#include <math.h>

void print_array(int arr[], int size)
{
	for (int i=0; i<size; i++) 
		printf("%d ", arr[i]);
	
	printf("\n");
}

double log2(double value)
{
	return log10(value) / log10(2.0);
}

void max_heapify(int arr[], int size, int index)
{
	int left = ((index+1) << 1) -1 ;
	int right = (((index+1) << 1) + 1) - 1;
	
	int largest;
	if (left <= (size-1) && arr[left] > arr[index])
		largest = left;
	else
		largest = index;
	
	if (right <= (size-1) && arr[right] > arr[largest])
		largest = right;
	
	if (largest != index) {
		int tmp;
		tmp = arr[index];
		arr[index] = arr[largest];
		arr[largest] = tmp;
		max_heapify(arr, size, largest);
	}
}

void build_max_heap(int arr[], int size)
{
	int heapsize = size;
	for (int i=size/2-1; i>=0; i--) {
		max_heapify(arr, size, i);
	}
}

void heapsort(int arr[], int size)
{
	build_max_heap(arr, size);
	print_array(arr, size);
	int loop_size = size;
	for (int i=size-1; i>=1; i--) {	
		int tmp = arr[0];
		arr[0] = arr[i];
		arr[i] = tmp;
		loop_size = loop_size - 1;
		print_array(arr, size);
		max_heapify(arr, loop_size, 0);
	}
}

int main(void)
{
	int array[] = {16, 14, 10, 8, 7, 9, 3, 2, 4, 1};
	int size = sizeof(array)/sizeof(array[0]);
	heapsort(array, size);
	print_array(array, size);
}
