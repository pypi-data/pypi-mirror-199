# Setup

How to save your 'GS_SERVICE_ACCOUNT' env-var to use this code
```
Your 'GS_SERVICE_ACCOUNT' needs to be the whole json file as a string instead of the path to the file.
Then, it also needs to be encrypted. To have the correct format, copy the json file contents to your clipboard, then
go in the terminal and execute `pbpaste | base64 | pbcopy`. These commands will encrypt the json content and put it back
to your clipboard. Then just paste the encrypted contents to your local env-var
```
i.e.

copy the content of the `.json` file to your memory and run the  following in terminal:
```shell
pbpaste | base64 | pbcopy
```
this will give you an encrypted string

save this sting as a envar called `GS_SERVICE_ACCOUNT`

# Initiate

```python
from pyKadabra import kinesis

sheet_url = 'https://docs.google.com/spreadsheets/d/1Alaj8Pb6sy3_W2oGb9WUoYznFof5W7kigAx/edit?usp=sharing'
working_sheet = kinesis.gsheets_handler(gsheet_url=sheet_url)
```

## Usage examples

##### create sheet
```python
working_sheet.create_sheet(worksheet='Psybeam')
```

##### delete
```python
working_sheet.delete_sheet(worksheet='Psyshock') # sheet with name
working_sheet.delete_sheet(worksheet=1) # sheet with index
```

##### writ to sheets
```python
working_sheet.write_to_sheet(input_dataframe=df_test, worksheet='Future Sight') # sheet with name
working_sheet.write_to_sheet(input_dataframe=df_test, worksheet=2) # sheet with index
```

##### count rows
```python
working_sheet.count_rows(worksheet='Future Sight')
```
##### clear range
```python
working_sheet.clear_range(worksheet='Future Sight') # entire sheet
working_sheet.clear_range(worksheet='Future Sight', clear_range_str='B2:D4') # subsection only
```

##### read from sheets
```python
df_read = working_sheet.read_sheet(worksheet='Future Sight') # sheet with name
df_read = working_sheet.read_sheet(worksheet=1) # sheet with index
df_read2 = working_sheet.read_sheet(worksheet='Future Sight', target_range_str='B1:C4') # subsection only
```
