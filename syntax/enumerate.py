'''
Often, when dealing with iterators, we also get need to keep a count of iterations.
Python eases the programmersâ€™ task by providing a built-in function enumerate() for this task.
Enumerate() method adds a counter to an iterable and returns it in a form of enumerating object.
This enumerated object can then be used directly for loops or converted into a list of tuples using the list() method.

Syntax:

enumerate(iterable, start=0)
Parameters:

Iterable: any object that supports iteration
Start: the index value from which the counter is to be started, by default it is 0
'''

# Python program to illustrate
if __name__ == '__main__':
    # enumerate function
    l1 = ["eat", "sleep", "repeat"]
    s1 = "geek"

    # creating enumerate objects
    obj1 = enumerate(l1)
    obj2 = enumerate(s1)

    print("Return type:", type(obj1))
    print(list(enumerate(l1)))
    for i, l in enumerate(l1):
        print(i, l)

    # changing start index to 2 from 0
    print(list(enumerate(s1, 2)))
