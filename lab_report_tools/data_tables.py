import csv

class DataTable:
    """This class is used to create data tables. The structure is very much like a dictionary of equal lengnth lists.
    Additional methods allow for row-wise operations to generate a new potential column based on values in the existing columns.
    """
    def __init__(self, labels: dict[str, str] = None, /, **columns: list) -> None:
        if labels == None:
            labels = {}
        self.labels = labels.copy()
        self._headers = [key for key in columns.keys()]
        self._columns = {key: list(val).copy() for key, val in columns.items()}
        if len(self._headers) == 0:
            self._row_count = 0
        else:
            self._row_count = len(columns[self._headers[0]])
        if not self._check_rectangular():
            raise ValueError("The data lists in each column all need to be of the same length.")

    def __repr__(self) -> str:
        """Method to return a string representing the DataTable object instance."""
        sorted_colmuns = {key: val for key, val in self.items()}
        return f"DataTable({self.labels}, **{sorted_colmuns})"
    
    def __str__(self) -> str:
        """Return a pretty string representation of the table."""
        line_list = [""] * (self._row_count + 2)
        for head, col in self.items():
            label = str(self.labels.get(head, head))
            str_list = [str(cell) for cell in col]
            max_len = max(3, len(label), *(len(item) for item in str_list))
            justified_str_list = [item.rjust(max_len) for item in str_list]
            justified_str_list.insert(0, ("-" * max_len))
            justified_str_list.insert(0, label.ljust(max_len))
            for i, item in enumerate(justified_str_list):
                line_list[i] += f"| {item} "
        return str.join("|\n", line_list) + "|"

    def __getitem__(self, key: str) -> list:
        """Get a shallow copy of the column data identified by the column key string."""
        if not isinstance(key, str):
            raise TypeError("Column keys must be strings.")
        if key not in self._columns:
            raise KeyError("Column key not found.")
        column_data = self._columns[key]
        return column_data.copy()
    
    def __setitem__(self, key: str, value: list):
        """Set the data for the column at the identified key string."""
        if not isinstance(key, str):
            raise TypeError("Column keys must be strings.")
        value = list(value)
        if self._row_count == 0:
            self._row_count = len(value)
        elif len(value) != self._row_count:
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
        if key in self.labels:
            del self.labels[key]
        if len(self._headers) == 0:
            self._row_count = 0
    
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
        self._headers.remove(name)
        self._headers.insert(i, name)
    
    def rename_column(self, old_name: str, new_name: str):
        """Rename the identified column to the *new_name*, if it is available. This changes the column key.
        Keep the column in the same position and with the same label if it had one.
        """
        old_name = str(old_name)
        new_name = str(new_name)
        if old_name not in self._headers:
            raise ValueError("*old_name* is not a valid column key.")
        if new_name in self._headers:
            raise ValueError("*new_name* already in use.")
        if old_name in self.labels:
            self.labels[new_name] = self.labels[old_name]
            del self.labels[old_name]
        self._columns[new_name] = self._columns[old_name]
        del self._columns[old_name]
        self._headers[self._headers.index(old_name)] = new_name

    def create_column(self, data_or_func, name: str, *, index: int = None, label: str = None, use_dict: bool = True):
        """Create a column and add it to the table. 
        If *data_or_func* is callable, it will be passed into calc and used to generate the table. If not, it will be turend into a list to be used as column data.
        *name* is the name to be given to the column and used as an identifying key. It should be unique in the table.
        *index* is the position where the column will show up in the string representation of the table. If left unspecified, the column will be placed at the end of the table.
        *label* is what will show up in the string representation of the table as the header for the column. If left unspecified, name will be used instead.
        The callback function will be passed the current row data as a dictionary by default, and a list if *use_dict* is set to False.
        """
        if callable(data_or_func):
            data = self.calc(data_or_func, use_dict=use_dict)
        else:
            data = list(data_or_func)
        self[name] = data
        if index != None:
            self.move_column(name, index)
        if label != None:
            self.labels[name] = label
    
    def calc(self, func, use_dict: bool = True):
        """Perform a row-wise operation to generate a list of data based on the existing content in the columns.
        A function should be passed in that accepts one or two positional parameters. 
        The callback function will be passed the current row data as a dictionary by default, and a list if *use_dict* is set to False.
        """
        if not callable(func):
            raise TypeError("func should be callable in the DataTable calc() method.")
        result = []
        for row in self.rows(use_dict=use_dict):
            val = func(row)
            result.append(val)
        return result


    def get_row(self, i: int, use_dict: bool = True):
        """Get the values of table at the given row index.
        By default, the row item is returned as a list.
        If *use_dict* is set to True, the row is returned in a dictionary.
        """
        if use_dict:
            row = {name:self._columns[name][i] for name in self._headers}
        else:
            row = [self._columns[name][i] for name in self._headers]
        return row
    
    def rows(self, use_dict: bool = True):
        """Iterate through the table by rows.
        By default, each row item returned as a list.
        If *use_dict* is set to True, the rows are returned in dictionaries.
        """
        for i in range(self._row_count):
            row = self.get_row(i, use_dict)
            yield row

    def add_row(self, data: list, i: int = None, use_dict: bool = True):
        """Add the row of data to the table. The data must have the same length as the number of columns in the table.
        *i* is the index to insert the row. If unspecified, it defaults to the last row of the table.
        If *use_dict* is set to True, the rows are returned in dictionaries.
        """
        if len(data) != len(self._headers):
            raise ValueError("Data length must match the number of columns in the table.")
        if i == None:
            i = self._row_count
        if use_dict:
            data_list = []
            for col in self._headers:
                data_list.append(data[col])
        else:
            data_list = data
        for j, col in enumerate(self._headers):
            self._columns[col].insert(i, data_list[j])
        self._row_count += 1

    def delete_row(self, i: int) -> list:
        """Delete the identified row in the table. The deleted data is returned in a list."""
        data = self.get_row(i, False)
        for col in self._headers:
            del self._columns[col][i]
        self._row_count -= 1
        return data

    def substitute(self, column: str, i: int, value):
        """
        Replace the cell at the specified column and index with the given value.
        Return the replaced value.
        """
        data = self[column]
        old_value = data[i]
        data[i] = value
        self[column] = data
        return old_value


    def get_html(self, *, id = None, right_header_columns: int = 0, caption: str = None) -> str:
        """
        Generate a string with the HTML representation of the table.
        *id*, if specified, will be set as the id for the table element.
        *right_header_columns* specifies how many columns on the right will be set to table headers.
        *caption*, if specified, will add the caption to the table with the input content.
        """
        def html_escape(text: str) -> str:
            """Replace <, >, &, and " with the corresponding HTML entities"""
            text = text.replace("&", "&amp;")
            text = text.replace("<", "&lt;")
            text = text.replace(">", "&gt;")
            text = text.replace('"', "&quot;")
            return text

        table_html = ""
        indent = "  "
        # Start the <table> with the id
        if id == None:
            table_html += "<table>\n"
        else:
            table_html += f'<table id="{id}">\n'
        # Add the <caption>
        if caption != None:
            table_html += f"{indent}<caption>{html_escape(str(caption))}</caption>\n"
        # Add the <thead>
        table_html += f"{indent}<thead>\n{indent*2}<tr>\n"
        for head in self.keys():
            label = html_escape(str(self.labels.get(head, head)))
            table_html += f"{indent*3}<th>{label}</th>\n"
        table_html += f"{indent*2}</tr>\n{indent}</thead>\n"
        # Add the <tbody>
        table_html += f"{indent}<tbody>\n"
        for row in self.rows(use_dict=False):
            table_html += f"{indent*2}<tr>\n"
            for i, data in enumerate(row):
                data = html_escape(str(data))
                cell_type = "th" if i < right_header_columns else "td"
                table_html += f"{indent*3}<{cell_type}>{data}</{cell_type}>\n"
            table_html += f"{indent*2}</tr>\n"
        table_html += f"{indent}</tbody>\n"
        # Close the <table>
        table_html += "</table>"
        return table_html

    @property
    def row_count(self):
        """Get the number of rows in the table. A read-only property."""
        return self._row_count
    
    @property
    def column_count(self):
        """Get the number of columns in the table. A read-only property."""
        return len(self._columns)

    @staticmethod
    def from_csv(file_location):
        """Create a DataTable instance from a csv file."""
        with open(file_location, "r") as file:
            csv_reader = csv.DictReader(file)
            result = {name:[] for name in csv_reader.fieldnames}
            for row in csv_reader:
                for name in csv_reader.fieldnames:
                    result[name].append(row[name])
        return DataTable(**result)    
