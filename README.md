## Coding-Challenge
Contains the Parser and Executer in Challenge.py and the data I made up in data.json

# Running the File
To run the file, have the data and the Challenge.py file in the same directory. 
The code must be run in the following format:

```
python SQLParser.py data.json

```

From there, it should prompt you with the following:

```
Enter your SQL query. Type 'quit' to quit.
SQL>  <Enter your SQL Query Here on the Command Line>

```

# Examples:
Valid Nested Query

```
Enter your SQL query. Type 'quit' to quit.
SQL> SELECT * FROM table WHERE pop > 1000000000 OR (pop > 1000000 AND region = 'Midwest')'
[
  {
    "state": "California",
    "region": "West",
    "pop": 2312312321,
    "pop_male": 3123123,
    "pop_female": 123123
  },
  {
    "state": "Texas",
    "region": "South",
    "pop": 1311312121,
    "pop_male": 14477622,
    "pop_female": 14667883
  },
  {
    "state": "New York",
    "region": "Northeast",
    "pop": 4563626172,
    "pop_male": 12839,
    "pop_female": 1222222222
  },
  {
    "state": "Illinois",
    "region": "Midwest",
    "pop": 1284756,
    "pop_male": 6316899,
    "pop_female": 6495611
  }
]
SQL> <Enter Another Query here>
```

Invalid Query

```
SQL> hello
Invalid Query - please try again or type 'quit' to quit.
SQL>

```

