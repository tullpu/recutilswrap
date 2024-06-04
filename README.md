# RecUtilsWrap

A Wrap class to make the use of recutils easier


# Simple example

```python
from recutilswrap import *

# Create a database book in a file book.rec with Id as primary key
r = RecUtilsWrap('Book','book.rec','Id')

# create / overwrite the db file. Should be done once
r.create_db()

# Insert some entries
r.insert(title="The Trial",author="Kafka")
r.insert(title="The Castle",author="Kafka")
r.insert(title="Thus Spoke Zarathustra",author="Nietzsche")
r.insert(title="The Plague", author="Camus")
r.insert(title="The Stranger", author="Camus")

# print a dictionary with the books of Camus
print(r.select(EQ('author',"Camus")))
```

