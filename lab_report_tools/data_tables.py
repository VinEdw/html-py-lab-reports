class DataTable:
    """This class is used to create data tables. The structure is very much like a dictionary of equal lengnth lists.
    Additional methods allow for row-wise operations to generate a new potential column based on values in the existing columns.
    """
    def __init__(self, labels: dict[str, str] = None, /, **columns: list) -> None:
        if labels == None:
            labels = {}
        self.labels = labels.copy()
        self._headers = []
        self._columns = {}
        for key, val in columns.items():
            self._headers.append(key)
            self._columns[key] = list(val).copy()
        self._row_count = len(val)
        if not self._check_rectangular():
            raise ValueError("The data lists in each column all need to be of the same length.")

    def __repr__(self) -> str:
        """Method to return a string representing the DataTable object instance."""
        sorted_colmuns = {key: val for key, val in self.items()}
        return f"DataTable({self.labels}, **{sorted_colmuns})"
    
    def __getitem__(self, key: str) -> list:
        """Get a shallow copy of the column data identified by the column key string."""
        if not isinstance(key, str):
            raise TypeError("Column keys must be strings.")
        if key not in self._columns:
            raise KeyError("Column key not found.")
        column_data: list = self._columns[key]
        return column_data.copy()
    
    def __setitem__(self, key: str, value: list):
        """Set the data for the column at the identified key string."""
        if not isinstance(key, str):
            raise TypeError("Column keys must be strings.")
        value = list(value)
        if len(value) != self._row_count:
            raise ValueError("The input data must have the same length as the other columns in the table.")
        self._columns[key] = value
        if key not in self._headers:
            self._headers.append(key)
    
    def __delitem__(self, key: str):
        """Delete the column at the given key."""
        if not isinstance(key, str):
            raise TypeError("Column keys must be strings.")
        if key not in self._columns:
            raise KeyError("Column key not found.")
        del self._columns[key]
        self._headers.remove(key)
    
    def __iter__(self):
        """Return the headers (column keys) when the table is iterated over."""
        return iter(self._headers)
    
    def __reversed__(self):
        """Return the headers (column keys) in reverse order when called by reversed()."""
        return reversed(self._headers)
    
    def __contains__(self, item) -> bool:
        """Return whether input item is one of the headers (column keys)."""
        return item in self._headers

    def __len__(self) -> int:
        """Return the number of columns in the table."""
        return len(self._headers)
    
    def _check_rectangular(self) -> bool:
        """Check if the data lists in each column are all of the same length. In other words, if the table is rectangular."""
        length_pass_list = (len(val) == self._row_count for val in self._columns.values()) 
        return all(length_pass_list)


    def keys(self):
        """Return an iterator of the headers (column keys)."""
        return iter(self._headers)
    
    def values(self):
        """Return a copy of the data in the table."""
        for key in self._headers:
           yield self._columns[key].copy()
    
    def items(self):
        """Return the keys and values of the columns in pairs."""
        for key in self._headers:
            val = self._columns[key].copy()
            yield (key, val)
    
    def get(self, key, default=None, /):
        """Get the column data at the given key. If the key is invalid, return the default."""
        if key in self._headers:
            return self._columns[key].copy()
        else:
            return default
    
    def copy(self) -> 'DataTable':
        """Return a shallow copy of the table."""
        return DataTable(self.labels.copy(), **self._columns.copy())
    

    def move_column(self, name: str, i: int):
        """Move the column of the input name to the given column index in the table."""
        if name not in self:
            raise ValueError("Column name not in table.")
        self._headers.remove(name)
        self._headers.insert(i, name)

    
    def get_row(self, i: int, return_dict: bool = False):
        """Get the values of table at the given row index.
        By default, the row item is returned as a list.
        If *return_dict* is set to True, the row is returned in a dictionary.
        """
        if return_dict:
            row = {name:self._columns[name][i] for name in self._headers}
        else:
            row = [self._columns[name][i] for name in self._headers]
        return row
    
    def rows(self, return_dict: bool = False):
        """Iterate through the table by rows.
        By default, each row item returned as a list.
        If *return_dict* is set to True, the rows are returned in dictionaries."""
        for i in range(self._row_count):
            row = self.get_row(i, return_dict)
            yield row

    def calc(self, func):
        """Perform a row-wise operation to generate a list of data based on the existing content in the columns.
        A function should be passed in that accepts one or two positional parameters. 
        The first parameter of the callback function will be passed the current row data as a dictionary.
        The second parameter will be passed the index of the current row.
        """
        result = []
        for i, row in enumerate(self.rows()):
            val = func(row, i)
            result.append(val)
        return result