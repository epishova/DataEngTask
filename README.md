# Donation Analytics Challange

For our solution we used Python 3.6. Directory src contains the following files:

* contribution_statistics.py
* donor_list.py
* recipient_list.py
* data_util.py
* unittests.py

We created separate classes to keep donors and recipients. Although those classes contain just a few methods, which are required to solve the current data task, the classes may be expanded and adapted for the future tasks. 

Each donor is uniquely identified by his/her name and zip code. Additionally, we identify the repeat donor by the year of his/her first donation. In a similar way, a recipient is identified by its id, zip code, and donation year. Both lists use a Python dictionary, which provides a fast access to its elements by a key.

To compute donation amount in a given percentile, for each recipient in the list, we store a sorted list of contributions. We use bisect library to find the n-th element in the sorted list. Although Python uses an array to implement the list, in practice, it should not negatively impact the insertion procedure. We can assume that the insertion would happen in different list locations (in fact, given a normal donation distribution the majority of insertions would happen in the middle of the list). Thus, on average only half of the list elements would be moved. It looks like an expensive operation to do for each new donation. However, in practice, it does not downgrade performance in comparison to linked-list implementation. 

In contribution_statistics.py script we defined a variable named mapping. Its purpose is to map a data column name to its position in a file. Those names are used in contribution_statistics.py for reference. It may be handy to have this type of mapping defined in one place, so, in case of any changes in data file structure, the positions of the data fields could be easily changed in one place. Additionally, the provided column names can be used for fast reference in case they had to be changed in the script.

In addition, scripts donor_list and recipient_list are provided with the corresponding column names. Thus, they are independent of the column names used in the input files. Although this independence could be implemented by passing to the class methods only the necessary parameter values (in our case ids, dates, and amounts), we decided that in future this list of parameters could grow and it would be better to pass a dictionary to the class methods. 

As a further improvement, we would consider using Red-Black Trees to implement the list of recipients. The optimal data structure should support fast insertion into the list because it is the most common operation. Next, there is no need to delete elements from the list. Finally, the search operation should be fast but it can be slower than insertion because the donation amount in a given percentile changes only when the nearest-rank value changed, or when an element was inserted in a position preceding the current value in a percentile. Thus, the donation amount in a given percentile will not be changed every time as we add a new donation, thus, it can be stored for each recipient in the list. Class recipient_list.py implements methods to store and return the current value in a given percentile without searching in the list. Although it is not needed in our current implementation when we use the Python list, it may be handy in future if another data structure would be implemented.
