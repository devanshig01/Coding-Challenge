import json
import argparse
import re

"""

This method loads the json_file and returns the json objects within.

"""
def load_json(json_str):
    with open(json_str, 'r') as file:
        return json.load(file)


"""
Parses the sql query and identifies the appropriate clauses entered. 
Only supports Select, Where and limit clauses.

"""

def parse_sql_query(query):
    
    try:
        select_clause = re.search(r"SELECT (.+?) FROM", query, re.IGNORECASE).group(1).strip()
        where_clause = re.search(r"WHERE (.+?)(?: LIMIT|$)", query, re.IGNORECASE)
        where_clause = where_clause.group(1).strip() if where_clause else None
        limit_clause = re.search(r"LIMIT (\d+)", query, re.IGNORECASE)
        limit = int(limit_clause.group(1)) if limit_clause else None
        return select_clause, where_clause, limit
    except:
        raise ValueError ("Invalid Query - please try again or type 'quit' to quit.")

    
"""

This method evaluates a basic condition on a given item. It parses and evaluates a 
condition expressed in SQL format. The condition should be a string and contain a field name, value
and a operator. Current supported operators are '=', '!=', '>', and '<'.

Params:
item (dict): A dictionary representing a single item of data. Keys are field names and values are the values 
            associated with those fields.

condition (str): A string representing the condition to be evaluated.

Returns:
bool: True if the condition is met for the given item, False otherwise.

Example:
- item = {'age': 22, 'name': 'Devanshi'}
- condition = "age > 21"
- evaluate_basic_condition(item, condition)
--> True
"""

def evaluate_basic_condition(item, condition):
    match = re.match(r"(.*?)\s*(=|!=|>|<)\s*(.*)", condition)

    #if any different operator is entered apart from the ones that are supported. 
    if not match:
        raise ValueError(f"Conditon cannot be evaluated.")

    field, operation, value = match.groups()

    #If attribute not in current data is entered in query.
    if field not in item:
        raise ValueError(f"Attribute not in existing table.")

    left_value = item[field]

    if value.strip("'").isdigit():  
        right_value = int(value.strip("'"))
    elif value in item:  
        right_value = item[value]
    else:  
        right_value = value.strip("'")

    if isinstance(left_value, str):
        right_value = str(right_value)

    operators = {'>': lambda x, y: x > y, '<': lambda x, y: x < y, '=': lambda x, y: x == y, '!=': lambda x, y: x != y}
    return operators[operation](left_value, right_value)


"""
Evaluates a complex condition containing parentheses on a given item.

This method parses and evaluates a condition that may include nested conditions
within parentheses, along with AND and OR operators. It processes
conditions inside parentheses first, then evaluates the remaining outer condition. All conditions
are evaluated using basic operators from the evaluate basic function
   
Params:
item (dict): A dictionary representing a single item of data. Keys are field names and values are the values 
            associated with those fields.

condition (str): A complex string representing the condition to be evaluated.

Returns:
bool: True if the overall condition is met, False otherwise.

Example:
- item = {'age': 22, 'name': 'Devanshi', 'city': 'Atlanta', 'gender': Female}
- condition = "(age > 25 AND city = 'Atlanta') OR gender = Female
- eval_parenthesis_condition(item, condition)
--> True
"""

def eval_parenthesis_condition(item, condition):
    # Evaluate conditions inside parentheses first
    
    # Evaluate the remaining condition
    def evaluate_inner(inner_condition):
        parts = re.split(r'(\bAND\b|\bOR\b)', inner_condition)
        results = []

        for part in parts:
            part = part.strip()
            if part in ('AND', 'OR'):
                results.append(part)
            elif part in ('1', '0'):  # Handle boolean values
                results.append(part == '1')
            else:
                results.append(evaluate_basic_condition(item, part))

        # Combine results based on logical operators
        result = results[0]
        for i in range(1, len(results), 2):
            if results[i] == 'AND':
                result = result and results[i + 1]
            elif results[i] == 'OR':
                result = result or results[i + 1]

        return result
    
    #check for parenthesis and call evaluation.
    while '(' in condition and ')' in condition:
        condition = re.sub(r'\(([^()]+)\)', lambda m: '1' if evaluate_inner(m.group(1)) else '0', condition)


    return evaluate_inner(condition)

"""
Executes the SQL query on the given data.

"""

def execute_query(data, select_clause, where_clause, limit_clause):
    results = []
    for item in data:

        if where_clause and not eval_parenthesis_condition(item, where_clause):
            continue
        
        result_item = {field: item[field] for field in select_clause.split(', ')} if select_clause != '*' else item
        results.append(result_item)

        if limit_clause and len(results) >= limit_clause:
            break

    return results


"""

Main method that takes in the json file and takes in sql 
queries through the command line.

"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file')
    args = parser.parse_args()

    data = load_json(args.json_file)

    print("Enter your SQL query. Type 'quit' to quit.")
    while True:
        try:
            query = input("SQL> ")
            if query.lower() == 'quit':
                break
            select_clause, where_clause, limit = parse_sql_query(query)
            results = execute_query(data, select_clause, where_clause, limit)
            print(json.dumps(results, indent=2))
        
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
