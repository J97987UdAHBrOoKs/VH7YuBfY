# 代码生成时间: 2025-08-02 15:47:32
import cherrypy
def bubble_sort(lst):
    # Bubble sort algorithm
    n = len(lst)
    for i in range(n):
        for j in range(0, n-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst
def selection_sort(lst):
    # Selection sort algorithm
    for i in range(len(lst)):
        min_idx = i
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst
def insertion_sort(lst):
    # Insertion sort algorithm
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >= 0 and key < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst
def quick_sort(lst):
    # Quick sort algorithm using Lomuto partition scheme
    if len(lst) <= 1:
        return lst
    else:
        pivot = lst[0]
        less = [x for x in lst[1:] if x <= pivot]
        greater = [x for x in lst[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)
def merge_sort(lst):
    # Merge sort algorithm
    if len(lst) > 1:
        mid = len(lst) // 2
        L = lst[:mid]
        R = lst[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            lst[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            lst[k] = R[j]
            j += 1
            k += 1
    return lst
def sort_algorithms():
    # Function to demonstrate different sorting algorithms
    lst = [64, 34, 25, 12, 22, 11, 90]
    print("Original List: ", lst)
    print("Sorted by Bubble Sort: ", bubble_sort(lst.copy()))
    print("Sorted by Selection Sort: ", selection_sort(lst.copy()))
    print("Sorted by Insertion Sort: ", insertion_sort(lst.copy()))
    print("Sorted by Quick Sort: ", quick_sort(lst.copy()))
    print("Sorted by Merge Sort: ", merge_sort(lst.copy()))
def main():
    # Main function to start the CherryPy server
    cherrypy.quickstart(sort_algorithms)
def run_sort_service():
    # Entry point for the sorting service
    if __name__ == "__main__":
        try:
            main()
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

# Uncomment the following line to test the service
# if __name__ == "__main__": run_sort_service()