# Medical Store Management System

## Overview
The Medical Store Management System is a console-based application built using Python that allows users to manage medicines in a medical store. This system supports various functionalities such as adding medicines, searching for medicines, checking expiry status, managing bills, and more. The application uses a SQLite database to store data.

## Features
- **Add Medicines**: Add new medicines to the database with details like product code, name, packing, expiry date, company, batch number, quantity, and rate.
- **Display Medicines**: View all medicines stored in the database.
- **Search Medicines**: Search for a specific medicine by its name.
- **Check Expired Stock**: Check for medicines that are past their expiry date.
- **Display Medicines Company-wise**: View medicines from a specific company.
- **Delete Medicines**: Remove medicines from the database using the product code.
- **Add New Bill**: Create a new bill by entering the bill number, customer name, doctor name, product code, and quantity.
- **Display Bills**: View all bills stored in the database.
- **Search Bill**: Search for a specific bill by its number.

## Technologies Used
- Python
- SQLite3

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/medical-store-management-system.git
   cd medical-store-management-system
   ```
2. Install Python if you haven't already.
3. Run the application
   ```bash
   python main.py
   ```
## Usage
Once the application is running, you'll see a menu with various options. Enter the corresponding number to access the desired functionality. Follow the promppts to enter or retrieve information as needed. 

## Database Structure
The system uses a SQLite database to store the following tables :
- Medicines : Stores details of each medicine.
- Bills: Stores details of each bill generated
