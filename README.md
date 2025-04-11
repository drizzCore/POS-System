# POS (Point of Sale) System
    #### Video Demo:  <URL HERE>
    #### Description:
    This project is an application for managing inventory and sales records using CSV files as database. This aims to help small businesses in managing their inventory because an actual POS system can cause a lot. This is a prototype that I aim to enhance in the future.

## Key Features

- **Inventory Management**
  - Add/remove items
  - Track quantities and prices
  - View inventory in tabular format
- **Sales Processing**
  - Process transactions with receipts
  - Automatic inventory deduction
  - Unique transaction IDs
- **Reporting**
  - View sales history
  - Generate formatted reports
- **Data Persistence**
  - CSV file storage
  - Automatic data backups
  - Easy data portability

## Usage

### Main Menu

The Main Menu is consists of options as shown below:

| Menu                | Shortcut |
|---------------------|----------|
| Manage Warehouse    |     W    |
| Store Mode          |     S    |
| Transaction Database|     T    |
| Exit Program        |     E    |

- **Manage Warehouse**

    This is the section where you can Add or Remove an Item to your inventory/warehouse. You can also see the overview report of you whole inventory in this section.

    - Add an Item

        This function will ask the user for the item of the item, quantity of the item and the price of the item. This will automatically update the database(CSV File).

    - Remove an Item

        This function will ask the user what item will be remove from the current inventory. If the user enters an item that is not found in the inventory, nothing will happen to the current inventory.

    - View inventory

        This will show the whole inventory in tabulated format.

- **Store Mode**

    This is where the user will initiate all the transactions with your clients/customers. This will ask the user for an item that is purchased and the program will automatically deduct the quantity of that specific item from the inventory and, at the same time, records the price of the item. The program will continue doing this until the user input "Done".

    This will then show the receipt which shows all the items purchased by the customer as well as the total amount billed.

    The program will also generate a unique transaction ID that will be recorded in a CSV file for safe keeping and recording.

- **Transaction Database**

    This option will show all the transactions to date including the Transaction ID, Date of purchase, Items purchased and also the Total bill.


## Function Documentation

### CSVManager Class

#### `__init__(self, file, fieldnames)`
- **Purpose**: Initialize CSV file manager
- **Parameters**:
  - `file` (str): Path to CSV file
  - `fieldnames` (list): Column headers for the CSV file
- **Behavior**:
  - Creates new CSV file with headers if not exists
  - Loads existing data into memory
- **Example**:
  ```python
  inventory = CSVManager("inventory.csv", ["Item", "Quantity", "Price"])

#### `read(self)`
- **Purpose**: Refresh the in-memory data from CSV file
- **Behavior**: Returns the list of dictionaries representing rows
- **Example**:
  ```python
  my_data = inventory.read()

#### `append(self, row)`
- **Purpose**: Add a new data to the CSV file
- **Parameter**:
  - `row` (dict): Data to add to the CSV file (the keys must match the fieldnames)
- **Behavior**: Append to both the file and in-memory data
- **Example**:
  ```python
  inventory.append({"Item": "Apple", "Quantity": "10", "Price": "1.99"})

#### `overwrite(self, new_data)`
- **Purpose**: Replace all the data in the CSV file
- **Parameter**:
  - `new_data` (list): List of dictionaries to be recorded
- **Behavior**: Writes new header and data
- **Example**:
  ```python
  inventory.overwrite([{"Item": "Banana", "Quantity": "5", "Price": "0.99"}, {"Item": "Apple", "Quantity": "10", "Price": "1.99"}])

### Core Functions

#### `main()`
- **Entry Point**: Starts the application
- **Workflow**:
    1. Initializes the CSV managers for inventory and sales
    2. Displays the main menu loop
    3. Routes the user to appropriate modes based on input
- **Features**:
    - Persistent until explicit exit
    - Error handling of invalid user menu inputs

#### `warehouse_mode(shop)`
- **Purpose**: Inventory manager interface
- **Parameter**:
  - `shop` (CSVManager): CSVManager instance that handles the inventory
- **Menu Options**:
  - Add an Item (A): calls `add_item()`
  - Remove an Item (R): calls `deduct_item()`
  - View Inventory (V): calls `report()`
  - Go back to Main Menu (B): returns to `main()`

#### `add_item(shop)`
- **Purpose**: Adds an item to the inventory
- **Parameter**:
  - `shop` (CSVManager): CSVManager instance that handles the inventory
- **Workflow**:
    1. Collects the item, quantity and price the user wants to add
    2. Creates standardized dictionary
    3. Appends to the CSV file
    4. Handles multiple data addition
- **Note**
    - Price is converted to float
    - Quantity is stored as str

#### `deduct_item(shop)`
- **Purpose**: Removes an item to the inventory
- **Parameter**:
  - `shop` (CSVManager): CSVManager instance that handles the inventory
- **Workflow**:
    1. Prompts the user for the item to be remove
    2. Filters out the matching item
    3. Overwrites the CSV File
    4. Handles multiple data removal
- **Note**
    - Item that is not in the CSV file will just be rewritted as is
    - Complete removal of item

#### `report(shop)`
- **Purpose**: Display the formatted data table in the CSV file
- **Parameter**:
  - `shop` (CSVManager): CSVManager instance that handles the inventory or sales
- **Note**
    - Uses tabulate for format
    - Persistent view until the user exits

#### `store_mode(shop, sales)`
- **Purpose**: Process transactions from the customer
- **Parameter**:
  - `shop` (CSVManager): CSVManager instance that handles the inventory
  - `sales` (CSVManager): CSVManager instance that handles the sales record
- **Workflow**:
    1. Generates a unique transaction ID
    2. Process the items until the user inputs "Done"
    3. Updates the quantities of items in the inventory everytime an item is entered
    4. Saves the transactions in CSV file
    5. Prints the receipt
- **Note**
    - The CSV file is updated in real time
    - Shows out-of-stock if the quantity hits 0
    - Transaction ID is formatted by the date of transaction plus 6 random digits
