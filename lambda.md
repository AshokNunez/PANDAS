# Lambda Functions and String Methods in Pandas with Examples

Lambda functions and string methods are powerful tools for data transformation in Pandas. Here's how to use them effectively:

## 1. Lambda Functions with `apply()`

Lambda functions are anonymous functions defined with `lambda` keyword. Combined with `apply()`, they're great for element-wise operations.

### Basic Examples:
```python
import pandas as pd

# Create sample DataFrame
df = pd.DataFrame({
    'Name': ['John Doe', 'Alice Smith', 'Bob Johnson'],
    'Age': [25, 30, 35],
    'Salary': [50000, 60000, 70000]
})

# Example 1: Simple transformation
df['Age_next_year'] = df['Age'].apply(lambda x: x + 1)

# Example 2: Conditional logic
df['Age_Group'] = df['Age'].apply(
    lambda age: 'Young' if age < 30 else 'Senior'
)

# Example 3: Multiple column operation
df['Name_Length'] = df['Name'].apply(lambda x: len(x))
```

## 2. String Methods with `str` Accessor

Pandas provides vectorized string operations through the `.str` accessor.

### Common String Operations:
```python
# Example 4: Case conversion
df['Name_Upper'] = df['Name'].str.upper()
df['Name_Lower'] = df['Name'].str.lower()

# Example 5: Splitting strings
df['First_Name'] = df['Name'].str.split().str[0]
df['Last_Name'] = df['Name'].str.split().str[-1]

# Example 6: String contains
df['Has_Doe'] = df['Name'].str.contains('Doe')

# Example 7: Replace substrings
df['Name_No_Space'] = df['Name'].str.replace(' ', '_')

# Example 8: Extract patterns (regex)
df['Name_Initials'] = df['Name'].str.extract(r'(\b[A-Z])')[0] + \
                      df['Name'].str.extract(r'(\b[A-Z])')[1]
```

## 3. Combining Lambda and String Methods

```python
# Example 9: Complex string operation with lambda
df['Formatted_Name'] = df['Name'].apply(
    lambda x: f"Mr/Ms {x.split()[0]}" if len(x.split()) > 1 else x
)

# Example 10: Multiple string operations
df['Email'] = df['Name'].apply(
    lambda x: f"{x.lower().replace(' ', '.')}@company.com"
)

# Example 11: Conditional string formatting
df['Salary_Formatted'] = df.apply(
    lambda row: f"${row['Salary']:,}" if row['Salary'] > 55000 else "Below threshold",
    axis=1
)
```

## 4. Practical Applications

### Data Cleaning:
```python
# Clean phone numbers
phones = pd.Series(['(123) 456-7890', '555.123.4567', '123-45-6789'])
clean_phones = phones.str.replace(r'[^0-9]', '', regex=True).apply(
    lambda x: f"({x[:3]}) {x[3:6]}-{x[6:]}"
)

# Extract domain from emails
emails = pd.Series(['john@example.com', 'alice@domain.org'])
domains = emails.apply(lambda x: x.split('@')[1])
```

### Text Analysis:
```python
# Count vowels in names
df['Vowel_Count'] = df['Name'].apply(
    lambda x: sum(1 for char in x.lower() if char in 'aeiou')
)

# Categorize by name length
df['Name_Category'] = df['Name'].apply(
    lambda x: 'Short' if len(x) < 8 else ('Medium' if len(x) < 12 else 'Long')
)
```

## 5. Performance Considerations

1. For simple operations, prefer built-in string methods (`str.`) over `apply()`
2. For complex operations, `apply()` with lambda is more flexible
3. For very large datasets, consider vectorized NumPy operations

Would you like me to focus on any specific aspect of lambda functions or string operations in more detail?
