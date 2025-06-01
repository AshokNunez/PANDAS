# Pandas Functions Cheatsheet

A quick reference guide to commonly used Pandas functions with descriptions and examples. Pandas is an open-source data analysis and manipulation tool, built on top of the Python programming language.

---

## Contents

1.  [DataFrame and Series Attributes & Methods](#dataframe-and-series-attributes--methods)
2.  [Reshaping and Pivoting](#reshaping-and-pivoting)
3.  [Grouping and Aggregation](#grouping-and-aggregation)
4.  [Lambda Functions (General Python, used with Pandas)](#lambda-functions-general-python-used-with-pandas)
5.  [Date and Time](#date-and-time)
6.  [Other Useful Functions](#other-useful-functions)

---

## DataFrame and Series Attributes & Methods

These functions and attributes are used to inspect, access, and manipulate data within Pandas DataFrames and Series.

### 1. `iloc` (Integer-location based indexing)
   - **Purpose:** Access a group of rows and columns by their integer position(s).
   - **Example:**
     ```python
     import pandas as pd
     data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
     df = pd.DataFrame(data)
     # Select the first row
     print(df.iloc[0])
     # Output:
     # col1    1
     # col2    4
     # Name: 0, dtype: int64

     # Select the first two rows and the first column
     print(df.iloc[0:2, 0])
     # Output:
     # 0    1
     # 1    2
     # Name: col1, dtype: int64
     ```

### 2. `loc` (Label-based indexing)
   - **Purpose:** Access a group of rows and columns by label(s) or a boolean array.
   - **Example:**
     ```python
     import pandas as pd
     data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
     df = pd.DataFrame(data, index=['a', 'b', 'c'])
     # Select row with index 'a'
     print(df.loc['a'])
     # Output:
     # col1    1
     # col2    4
     # Name: a, dtype: int64

     # Select rows 'a' and 'b', and column 'col1'
     print(df.loc[['a', 'b'], 'col1'])
     # Output:
     # a    1
     # b    2
     # Name: col1, dtype: int64
     ```

### 3. `axes`
   - **Purpose:** Returns a list representing the axes of the DataFrame (row axis and column axis).
   - **Example:**
     ```python
     import pandas as pd
     data = {'col1': [1, 2], 'col2': [3, 4]}
     df = pd.DataFrame(data)
     print(df.axes)
     # Output: [RangeIndex(start=0, stop=2, step=1), Index(['col1', 'col2'], dtype='object')]
     ```

### 4. `empty`
   - **Purpose:** An attribute that is `True` if the DataFrame or Series is empty (has no items), `False` otherwise.
   - **Example:**
     ```python
     import pandas as pd
     df_empty = pd.DataFrame()
     print(f"Is df_empty empty? {df_empty.empty}") # Output: Is df_empty empty? True

     df_not_empty = pd.DataFrame({'col1': [1]})
     print(f"Is df_not_empty empty? {df_not_empty.empty}") # Output: Is df_not_empty empty? False
     ```

### 5. `dropna()`
   - **Purpose:** Remove missing values (NaN).
   - **Example:**
     ```python
     import pandas as pd
     import numpy as np
     data = {'col1': [1, 2, np.nan], 'col2': [np.nan, 5, 6]}
     df = pd.DataFrame(data)
     print("Original DataFrame:\n", df)

     # Drop rows with any missing values
     print("\nDataFrame after dropping rows with NaN:\n", df.dropna())

     # Drop columns with any missing values
     print("\nDataFrame after dropping columns with NaN:\n", df.dropna(axis='columns'))
     ```

### 6. `astype()`
   - **Purpose:** Cast a pandas object to a specified dtype.
   - **Example:**
     ```python
     import pandas as pd
     data = {'col1_int': [1, 2, 3], 'col2_str_float': ['4.0', '5.5', '6.7']}
     df = pd.DataFrame(data)
     print("Original dtypes:\n", df.dtypes)

     df['col2_str_float'] = df['col2_str_float'].astype(float)
     print("\nNew dtypes after astype:\n", df.dtypes)
     ```

### 7. `at`
   - **Purpose:** Access a single value for a row/column label pair. Faster for scalar lookups than `loc`.
   - **Example:**
     ```python
     import pandas as pd
     data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
     df = pd.DataFrame(data, index=['a', 'b', 'c'])
     value = df.at['a', 'col1']
     print(f"Value at row 'a', column 'col1': {value}") # Output: Value at row 'a', column 'col1': 1
     ```

### 8. `iat`
   - **Purpose:** Access a single value for a row/column pair by integer position. Faster for scalar lookups than `iloc`.
   - **Example:**
     ```python
     import pandas as pd
     data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
     df = pd.DataFrame(data)
     value = df.iat[0, 0]
     print(f"Value at integer position [0, 0]: {value}") # Output: Value at integer position [0, 0]: 1
     ```

### 9. `keys()` (or `columns` / `index`)
   - **Purpose:** For DataFrames, `df.keys()` is an alias for `df.columns`. For Series, it returns the index.
   - **Example (DataFrame):**
     ```python
     import pandas as pd
     data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
     df = pd.DataFrame(data)
     print("DataFrame keys (columns):", df.keys()) # Output: DataFrame keys (columns): Index(['Name', 'Age'], dtype='object')
     ```
   - **Example (Series):**
     ```python
     import pandas as pd
     s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
     print("Series keys (index):", s.keys()) # Output: Series keys (index): Index(['a', 'b', 'c'], dtype='object')
     ```

### 10. `index`
    - **Purpose:** The index (row labels) of the DataFrame or Series.
    - **Example:**
      ```python
      import pandas as pd
      data = {'col1': [10, 20], 'col2': [30, 40]}
      df = pd.DataFrame(data, index=['row1', 'row2'])
      print("DataFrame index:", df.index) # Output: DataFrame index: Index(['row1', 'row2'], dtype='object')
      ```

### 11. `size`
    - **Purpose:** Return an int representing the number of elements in this object (rows * columns for DataFrame).
    - **Example:**
      ```python
      import pandas as pd
      data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
      df = pd.DataFrame(data)
      print(f"DataFrame size: {df.size}") # Output: DataFrame size: 6

      s = pd.Series([1, 2, 3])
      print(f"Series size: {s.size}") # Output: Series size: 3
      ```

### 12. `ndim`
    - **Purpose:** Return an int representing the number of axes / array dimensions (1 for Series, 2 for DataFrame).
    - **Example:**
      ```python
      import pandas as pd
      s = pd.Series([1, 2, 3])
      print(f"Series ndim: {s.ndim}") # Output: Series ndim: 1

      df = pd.DataFrame({'col1': [1, 2]})
      print(f"DataFrame ndim: {df.ndim}") # Output: DataFrame ndim: 2
      ```

### 13. `shape`
    - **Purpose:** Return a tuple representing the dimensionality of the DataFrame or Series (rows, columns).
    - **Example:**
      ```python
      import pandas as pd
      data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
      df = pd.DataFrame(data)
      print(f"DataFrame shape: {df.shape}") # Output: DataFrame shape: (3, 2)

      s = pd.Series([1, 2, 3, 4])
      print(f"Series shape: {s.shape}") # Output: Series shape: (4,)
      ```

### 14. `items()`
    - **Purpose:** Iterates over (column name, Series) pairs for DataFrames or (index, value) pairs for Series.
    - **Example (DataFrame):**
      ```python
      import pandas as pd
      data = {'Name': ['Alice', 'Bob'], 'Age': [25, 30]}
      df = pd.DataFrame(data)
      print("Iterating over DataFrame items:")
      for label, content in df.items():
          print(f"Column Name: {label}\n{content}\n---")
      ```
    - **Example (Series):**
      ```python
      import pandas as pd
      s = pd.Series([10, 20], index=['a', 'b'])
      print("Iterating over Series items:")
      for index, value in s.items():
          print(f"Index: {index}, Value: {value}")
      ```

### 15. `where()`
    - **Purpose:** Replace values where the condition is `False`.
    - **Example:**
      ```python
      import pandas as pd
      s = pd.Series(range(5)) # 0, 1, 2, 3, 4
      print("Original Series:\n", s)

      # Keep values less than 3, replace others with NaN (by default)
      print("\nSeries.where(s < 3):\n", s.where(s < 3))

      # Keep values less than 3, replace others with 10
      print("\nSeries.where(s < 3, 10):\n", s.where(s < 3, 10))
      ```

### 16. `filter()`
    - **Purpose:** Subset the DataFrame rows or columns according to labels in the specified index.
    - **Example:**
      ```python
      import pandas as pd
      data = {'apples_sales': [10, 15, 12],
              'orange_sales': [8, 10, 9],
              'banana_count': [30, 32, 31]}
      df = pd.DataFrame(data)
      print("Original DataFrame:\n", df)

      # Get columns that contain 'sales' in their name
      print("\nFiltered columns (like='sales'):\n", df.filter(like='sales'))

      # Get columns with specific names
      print("\nFiltered columns (items=['apples_sales', 'banana_count']):\n",
            df.filter(items=['apples_sales', 'banana_count']))

      # Filter using a regular expression on column names
      print("\nFiltered columns (regex='_s'):\n", df.filter(regex='_s'))
      ```

### 17. `query()`
    - **Purpose:** Query the columns of a DataFrame with a boolean expression.
    - **Example:**
      ```python
      import pandas as pd
      data = {'A': range(1, 6), 'B': range(10, 15)}
      df = pd.DataFrame(data)
      print("Original DataFrame:\n", df)

      # Select rows where column A is greater than 2
      print("\nQuery 'A > 2':\n", df.query('A > 2'))

      # Select rows where column B is less than 13 and A is greater than 1
      print("\nQuery 'B < 13 and A > 1':\n", df.query('B < 13 and A > 1'))
      ```

### 18. `iteritems()` (Use `items()` for modern Pandas)
    - **Purpose:** For Series, iterate over (index, value) pairs. For DataFrames, `iteritems()` is an alias for `items()`. `items()` is generally preferred.
    - **Example (Series):**
      ```python
      import pandas as pd
      s = pd.Series(['apple', 'banana', 'cherry'], index=['a', 'b', 'c'])
      print("Iterating over Series items (using iteritems/items):")
      for index, value in s.items(): # or s.iteritems()
          print(f"Index: {index}, Value: {value}")
      ```

### 19. `get()`
    - **Purpose:** Get item from object for given key (e.g., DataFrame column). Returns a default value if the key is not found, preventing a `KeyError`.
    - **Example:**
      ```python
      import pandas as pd
      data = {'col1': [1, 2], 'col2': [3, 4]}
      df = pd.DataFrame(data)

      print("Getting 'col1':\n", df.get('col1'))
      print("\nGetting 'col3' with default 'Not found':", df.get('col3', default='Not found'))
      ```

### 20. `align()`
    - **Purpose:** Align two objects on their axes with the specified join method, filling in missing values with NaN where necessary.
    - **Example:**
      ```python
      import pandas as pd
      df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}, index=['x', 'y'])
      df2 = pd.DataFrame({'B': [5, 6], 'C': [7, 8]}, index=['y', 'z'])
      print("df1:\n", df1)
      print("df2:\n", df2)

      # Align with an outer join (union of indexes and columns)
      a1, a2 = df1.align(df2, join='outer')
      print("\nAligned df1 (outer join):\n", a1)
      print("Aligned df2 (outer join):\n", a2)

      # Align on columns with an inner join
      a1_inner_col, a2_inner_col = df1.align(df2, join='inner', axis=1)
      print("\nAligned df1 (inner join on columns):\n", a1_inner_col)
      print("Aligned df2 (inner join on columns):\n", a2_inner_col)
      ```

### 21. `transform()`
    - **Purpose:** Call a function on self producing a DataFrame or Series with transformed values, which has the same axis length as self. Especially useful with `groupby`.
    - **Example:**
      ```python
      import pandas as pd
      import numpy as np
      df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
      print("Original DataFrame:\n", df)

      # Transform values by taking their square root
      print("\nDataFrame transformed with np.sqrt:\n", df.transform(np.sqrt))

      # Transform using a lambda function per column
      print("\nDataFrame transformed with lambda x: x * 2:\n", df.transform(lambda x: x * 2))

      df['C'] = ['X', 'Y', 'X']
      print("\nOriginal with group column 'C':\n", df)
      # Broadcasts sum of group 'A' back to original shape
      df['A_group_sum'] = df.groupby('C')['A'].transform('sum')
      print("\nAfter groupby transform (sum of A per group C):\n", df)
      ```

### 22. `insert()`
    - **Purpose:** Insert column into DataFrame at specified integer location.
    - **Example:**
      ```python
      import pandas as pd
      df = pd.DataFrame({'A': [1, 2], 'C': [3, 4]})
      print("Original DataFrame:\n", df)

      # Insert column 'B' with values [10, 20] at index 1 (second position)
      df.insert(loc=1, column='B', value=[10, 20])
      print("\nDataFrame after inserting column 'B':\n", df)
      ```

### 23. `delete()` (Not a direct DataFrame method; use `drop()` or `del`)
   - **Purpose:** Pandas uses `drop()` for removing rows/columns or the `del` keyword for columns. `delete()` is not a standard DataFrame method for this.
   - **Example (using `drop`):**
     ```python
     import pandas as pd
     data = {'col1': [1, 2], 'col2': [3, 4], 'col3': [5, 6]}
     df = pd.DataFrame(data)
     print("Original DataFrame:\n", df)

     # Delete 'col2'
     df_dropped_col = df.drop('col2', axis=1)
     print("\nAfter dropping 'col2':\n", df_dropped_col)

     # Delete row at index 0
     df_dropped_row = df.drop(0, axis=0) # or df.drop(index=0)
     print("\nAfter dropping row 0:\n", df_dropped_row)
     ```
   - **Example (using `del` for columns):**
     ```python
     import pandas as pd
     data = {'col1': [1, 2], 'col2': [3, 4]}
     df = pd.DataFrame(data)
     print("\nOriginal DataFrame for del example:\n", df)
     del df['col1']
     print("\nAfter `del df['col1']`:\n", df)
     ```

### 24. `drop()`
    - **Purpose:** Remove specified labels from rows or columns.
    - **Example:**
      ```python
      import pandas as pd
      data = {'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}
      df = pd.DataFrame(data, index=['a', 'b', 'c'])
      print("Original DataFrame:\n", df)

      # Drop column 'col2'
      print("\nAfter dropping 'col2' (axis=1):\n", df.drop('col2', axis=1))

      # Drop rows with index 'a' and 'c'
      print("\nAfter dropping rows 'a' and 'c' (axis=0):\n", df.drop(['a', 'c'], axis=0))
      ```

### 25. `drop_duplicates()`
    - **Purpose:** Return DataFrame with duplicate rows removed.
    - **Example:**
      ```python
      import pandas as pd
      data = {'col1': ['A', 'B', 'A', 'C', 'A'], 'col2': [1, 2, 1, 3, 1]}
      df = pd.DataFrame(data)
      print("Original DataFrame:\n", df)

      # Drop duplicate rows based on all columns (keeps first occurrence by default)
      print("\nAfter drop_duplicates():\n", df.drop_duplicates())

      # Drop duplicates based on 'col1', keeping the last occurrence
      print("\nAfter drop_duplicates(subset=['col1'], keep='last'):\n",
            df.drop_duplicates(subset=['col1'], keep='last'))
      ```

---

## Reshaping and Pivoting

These functions help in restructuring the layout of your data.

### 26. `stack()`
    - **Purpose:** Stack the prescribed level(s) from columns to index. Returns a Series or DataFrame with a new inner-most level in a MultiIndex.
    - **Example:**
      ```python
      import pandas as pd
      header = pd.MultiIndex.from_product([['Period1','Period2'],['MetricA','MetricB']])
      data_values = [[1,2,3,4],[5,6,7,8]]
      df = pd.DataFrame(data_values, index=['Row1','Row2'], columns=header)
      print("Original DataFrame with MultiIndex columns:\n", df)

      # Stacks the innermost column level ('MetricA', 'MetricB') to become index level
      stacked_df = df.stack()
      print("\nStacked DataFrame (innermost column level stacked):\n", stacked_df)

      # Stacks the 'Period1'/'Period2' level (level=0 of columns)
      stacked_level0_df = df.stack(level=0)
      print("\nStacked DataFrame (column level 0 stacked):\n", stacked_level0_df)
      ```

### 27. `unstack()`
    - **Purpose:** Unstack the prescribed level(s) from index to columns. This is the inverse of `stack()`.
    - **Example:**
      ```python
      import pandas as pd
      index = pd.MultiIndex.from_tuples([('Row1', 'Sub1'), ('Row1', 'Sub2'),
                                         ('Row2', 'Sub1'), ('Row2', 'Sub2')],
                                        names=['MainRow', 'SubRow'])
      s = pd.Series([1, 2, 3, 4], index=index)
      print("Original Series with MultiIndex:\n", s)

      # Unstack the inner-most index level ('SubRow') to columns
      unstacked_s = s.unstack()
      print("\nUnstacked Series (inner-most index level to columns):\n", unstacked_s)

      # Unstack the 'MainRow' level (level=0 of index)
      unstacked_level0_s = s.unstack(level=0)
      print("\nUnstacked Series (index level 0 to columns):\n", unstacked_level0_s)
      ```

### 28. `replace()`
    - **Purpose:** Replace values given in `to_replace` with `value`.
    - **Example:**
      ```python
      import pandas as pd
      import numpy as np
      s = pd.Series([1, 2, 3, 2, 4, 1, np.nan])
      print("Original Series:\n", s)

      # Replace all 2s with 99
      print("\nReplace 2 with 99:\n", s.replace(2, 99))

      # Replace multiple values using a dictionary
      print("\nReplace 1 with 100 and 4 with 400:\n", s.replace({1: 100, 4: 400}))

      # Replace NaN with 0
      print("\nReplace NaN with 0:\n", s.replace(np.nan, 0))
      ```

### 29. `pipe()`
    - **Purpose:** Apply a function (or a chain of functions) to a DataFrame or Series in a more readable way. The DataFrame/Series is passed as the first argument to the function.
    - **Example:**
      ```python
      import pandas as pd

      def add_value(input_df, value_to_add):
          return input_df + value_to_add

      def multiply_by_value(input_df, factor):
          return input_df * factor

      df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
      print("Original DataFrame:\n", df)

      # Chaining operations using pipe
      result = (df.pipe(add_value, value_to_add=5)
                  .pipe(multiply_by_value, factor=2))
      print("\nDataFrame after pipe operations (add 5, then multiply by 2):\n", result)
      # Equivalent to: multiply_by_value(add_value(df, 5), 2)
      ```

### 30. `explode()`
    - **Purpose:** Transform each element of a list-like or iterable to a row, replicating index values.
    - **Example:**
      ```python
      import pandas as pd
      df = pd.DataFrame({'A': [[1, 2, 3], 'foo', [], [4, 5]],
                         'B': 1,
                         'C': [['x','y'], 'a', ['z'], ['p', 'q']]})
      print("Original DataFrame:\n", df)

      exploded_A = df.explode('A')
      print("\nDataFrame exploded on column 'A':\n", exploded_A)

      # Exploding multiple columns (Pandas 1.3.0+)
      # Note: If lengths of list-likes in a row differ, an error might occur
      # or they must be of the same length to explode simultaneously without issues.
      # For this example, let's ensure 'A' and 'C' have compatible structures for simultaneous explosion.
      df_compatible = pd.DataFrame({'A': [[1, 2], [3, 4]],
                                    'C': [['x', 'y'], ['p', 'q']],
                                    'B': ['foo', 'bar']})
      print("\nCompatible DataFrame for multi-column explode:\n", df_compatible)
      exploded_AC = df_compatible.explode(['A', 'C'])
      print("\nDataFrame exploded on columns 'A' and 'C':\n", exploded_AC)
      ```

---

## Grouping and Aggregation

These functions are essential for split-apply-combine operations.

### 31. `groupby()`
    - **Purpose:** Group DataFrame using a mapper or by a Series of columns. It's often followed by an aggregation function (`sum`, `mean`, `count`, `agg`, etc.).
    - **Example:**
      ```python
      import pandas as pd
      data = {'Team': ['A', 'B', 'A', 'B', 'A', 'B'],
              'Player': ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
              'Points': [10, 12, 15, 13, 11, 14],
              'Assists': [5, 7, 8, 6, 7, 5]}
      df = pd.DataFrame(data)
      print("Original DataFrame:\n", df)

      # Group by 'Team' and calculate the sum of 'Points' for each team
      team_points_sum = df.groupby('Team')['Points'].sum()
      print("\nSum of Points per Team:\n", team_points_sum)

      # Group by 'Team' and calculate multiple aggregations
      team_stats = df.groupby('Team').agg(
          total_points=('Points', 'sum'),
          average_assists=('Assists', 'mean'),
          player_count=('Player', 'count')
      )
      print("\nAggregated Stats per Team:\n", team_stats)
      ```

### 32. `pivot()`
    - **Purpose:** Reshape data (produce a "pivot" table) based on column values. It's used when you have unique combinations of `index`, `columns`, and `values`. Use `pivot_table` if aggregation is needed for duplicate entries.
    - **Example:**
      ```python
      import pandas as pd
      data = {'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02', '2023-01-03'],
              'Product': ['A', 'B', 'A', 'B', 'A'],
              'Sales': [100, 150, 120, 180, 110]}
      df = pd.DataFrame(data)
      # Ensure no duplicate index/column pairs for pivot, or use pivot_table
      # For this example, 'Date' and 'Product' combinations are unique.
      print("Original DataFrame:\n", df)

      # Pivot the table to have 'Date' as index, 'Product' as columns, and 'Sales' as values
      pivot_df = df.pivot(index='Date', columns='Product', values='Sales')
      print("\nPivoted DataFrame:\n", pivot_df)
      # Note: NaN will appear where combinations don't exist (e.g., Product B on 2023-01-03)
      ```

### 33. `apply()`
    - **Purpose:** Apply a function along an axis of the DataFrame (row-wise or column-wise) or to elements of a Series.
    - **Example:**
      ```python
      import pandas as pd
      import numpy as np
      df = pd.DataFrame([[4, 9, 16], [25, 36, 49]], columns=['A', 'B', 'C'])
      print("Original DataFrame:\n", df)

      # Apply np.sqrt element-wise (if function works element-wise)
      print("\nApply np.sqrt element-wise:\n", df.apply(np.sqrt))

      # Apply sum column-wise (axis=0, default)
      print("\nApply sum column-wise (sum of each column):\n", df.apply(np.sum, axis=0))

      # Apply sum row-wise (axis=1)
      print("\nApply sum row-wise (sum of each row):\n", df.apply(np.sum, axis=1))

      # Apply a custom lambda function to each column
      print("\nApply lambda (max - min) to columns:\n", df.apply(lambda x: x.max() - x.min(), axis=0))

      # Apply a custom lambda function to each row
      print("\nApply lambda (max - min) to rows:\n", df.apply(lambda x: x.max() - x.min(), axis=1))
      ```

---

## Lambda Functions (General Python, used with Pandas)

### 34. `lambda`
    - **Purpose:** Create small, anonymous (unnamed) inline functions. Often used with Pandas methods like `apply()`, `map()`, `transform()`, `assign()`, etc., for concise operations.
    - **Example (with `Series.apply`):**
      ```python
      import pandas as pd
      s = pd.Series([1, 2, 3, 4, 5])
      # Add 10 to each element in the Series
      s_plus_10 = s.apply(lambda x: x + 10)
      print("Original Series:\n", s)
      print("\nSeries after applying lambda x: x + 10:\n", s_plus_10)
      ```
    - **Example (with `DataFrame.assign`):**
      ```python
      import pandas as pd
      df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
      # Create a new column 'C' which is A + B
      df = df.assign(C = lambda x: x['A'] + x['B'])
      print("\nDataFrame with new column 'C' using lambda in assign:\n", df)
      ```
    - **Example (with `groupby().transform`):**
      ```python
      df_transform = pd.DataFrame({
          'key': ['A', 'B', 'A', 'B', 'A'],
          'value': [10, 20, 30, 40, 50]
      })
      # Calculate group mean and broadcast it back to original shape
      df_transform['group_mean'] = df_transform.groupby('key')['value'].transform(lambda x: x.mean())
      print("\nDataFrame with group mean using lambda in transform:\n", df_transform)
      ```

---

## Date and Time

### 35. `pd.to_datetime()`
    - **Purpose:** Convert argument (Series, list-like, scalar) to datetime objects.
    - **Example:**
      ```python
      import pandas as pd
      date_strings_series = pd.Series(['2023-01-01', '2023-02-15 10:30:00', '03/Mar/2023'])
      print("Original Series of date strings:\n", date_strings_series)

      # Convert to datetime objects
      datetime_objects = pd.to_datetime(date_strings_series, errors='coerce') # errors='coerce' turns unparseable dates to NaT
      print("\nConverted datetime objects:\n", datetime_objects)

      # Access datetime properties (e.g., day name, year)
      if pd.api.types.is_datetime64_any_dtype(datetime_objects):
          print("\nDay names:\n", datetime_objects.dt.day_name())
          print("\nYear:\n", datetime_objects.dt.year)

      # Handling specific formats
      date_str_custom = '04*Jan*2023'
      custom_datetime = pd.to_datetime(date_str_custom, format='%d*%b*%Y')
      print(f"\nCustom format '{date_str_custom}' to datetime: {custom_datetime}")
      ```

---

## Other Useful Functions

### 36. `nlargest()` (and `nsmallest()`)
    - **Purpose:** Get the first `n` rows ordered by specified columns in descending (`nlargest`) or ascending (`nsmallest`) order.
    - **Example:**
      ```python
      import pandas as pd
      data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
              'Score': [85, 92, 78, 92, 88, 78],
              'Age': [23, 25, 22, 24, 25, 22]}
      df = pd.DataFrame(data)
      print("Original DataFrame:\n", df)

      # Get the 3 largest scores
      # If ties, 'first' keeps the first encountered ones. 'all' would keep all tied records.
      print("\nTop 3 largest scores (keeping first for ties):\n", df.nlargest(3, 'Score'))

      # Get the 3 largest scores, considering Age as a secondary sort key for ties in Score
      print("\nTop 3 largest scores (using Score then Age for ties):\n", df.nlargest(3, ['Score', 'Age']))


      # Get the 2 smallest scores
      print("\nBottom 2 smallest scores (keeping first for ties):\n", df.nsmallest(2, 'Score'))

      # Get the 2 smallest scores, keeping all ties for the last rank if present
      print("\nBottom 2 smallest scores (keeping all ties):\n", df.nsmallest(2, 'Score', keep='all'))
      ```

---
