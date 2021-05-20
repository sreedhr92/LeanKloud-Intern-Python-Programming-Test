import csv
import sys
import heapq

filename = sys.argv[1]

topper_dict ={} # stores the highest marks in each subject
name_dict ={}   # stores the name of the student who got the highest mark in each subject
fields = []     # stores subject names
heap = []       # stores the top 3 rank holder in a heap 
heapq.heapify(heap)
number_of_toppers= 3

with open(filename,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)

    for i in range(1,len(fields)):
        topper_dict[fields[i]]=-1;
        name_dict[fields[i]]=""

    for row in csvreader:
        total_sum = 0
        for i in range(1,len(row)):
            if int(row[i]) > topper_dict[fields[i]]:
                topper_dict[fields[i]] = int(row[i])
                name_dict[fields[i]] = row[0]
            total_sum += int(row[i])
            
        
        # Here the time complexity is log(k) for push and pop operations
        # the time complexity for searching the top 3 rank is O(N log(k)) and space complexity is O(k)(where k=3) ~ constant.

        if len(heap) < number_of_toppers:              
            heapq.heappush(heap,(total_sum,row[0]))
        else:
            heapq.heappushpop(heap,(total_sum,row[0]))     
    
# Finding the topper in each subject is done while the reading the file itself.
# Hence the time complexity is O(N*M) (where N - rows and M - columns) for reading and finding the toppers
# Space complexity is O(M) (where M = 5) ~ constant

for i in range(1,len(fields)):
    print(f"\nTopper in {fields[i]} is {name_dict[fields[i]]}.")

print(f'\nBest Students in the class are {heap[1][1]}, {heap[2][1]} and {heap[0][1]}.\n')

#The time Complexity of this program is O(N*M) (where N - rows and M - columns)

'''
            Heap Structure

          (488, 'Manodhar')


(478, 'Sourav')       (484, 'Bhavana')


'''


            