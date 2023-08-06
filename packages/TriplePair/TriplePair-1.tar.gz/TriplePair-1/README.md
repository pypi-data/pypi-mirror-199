# TriplePair

**TriplePair** is a Python data type which represents a tuple of three values.

## How to Use?

**b = TriplePair(4, 5, 6)**

The code above initialises TriplePair object 'b' with left value of 4, middle value of 5, and right value of 6.

**a = TriplePair(1, 2, 3)**
**b = TriplePair(4, 5, 6)**
**c = a.sum(b)  # TriplePair(7, 8, 9)**

The code above gets the sum of the corresponding elements of the TriplePair objects 'a' and 'b'.

**a = TriplePair(1, 2, 3)**
**b = TriplePair(4, 5, 6)**
**c = a.zip(b)  # TriplePair((1, 4), (2, 5), (3, 6))**

The code above zips both TriplePair objects 'a' and 'b'.
