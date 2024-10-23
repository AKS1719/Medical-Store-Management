import mysql.connector as sqlct
import datetime

class Database:
    def __init__(self):
        self.mycn = sqlct.connect(
            host="localhost",
            user="root",
            password="Juhijain05$",
            database="juhijain1234"
        )
        self.mycur = self.mycn.cursor()

        # Creating tables if they do not exist
        self.mycur.execute("""
            CREATE TABLE IF NOT EXISTS _medicalproject (
                ProductCode INT PRIMARY KEY,
                name CHAR(50) NOT NULL,
                Packing CHAR(50),
                Expirydate DATE,
                Company CHAR(50),
                Batch CHAR(10),
                Quantity INT,
                Rate INT
            )
        """)
        self.mycur.execute("""
            CREATE TABLE IF NOT EXISTS customertable (
                BillNumber INT,
                Customername VARCHAR(50),
                Doctorname VARCHAR(50),
                Productcode INT,
                Quantity INT,
                FOREIGN KEY (Productcode) REFERENCES _medicalproject(ProductCode)
            )
        """)

    def close(self):
        self.mycur.close()
        self.mycn.close()


class Medicine:
    def __init__(self, product_code, name, packing, expiry_date, company, batch, quantity, rate):
        self.product_code = product_code
        self.name = name
        self.packing = packing
        self.expiry_date = expiry_date
        self.company = company
        self.batch = batch
        self.quantity = quantity
        self.rate = rate

    def add_to_database(self, db):
        try:
            cmd = """
                INSERT INTO _medicalproject 
                (ProductCode, name, Packing, Expirydate, Company, Batch, Quantity, Rate) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.mycur.execute(cmd, (self.product_code, self.name, self.packing, self.expiry_date,
                                    self.company, self.batch, self.quantity, self.rate))
            db.mycn.commit()
            print("Record has been added successfully.")
        except Exception as e:
            print(f"Error adding medicine: {e}")

    @staticmethod
    def display_medicines(db):
        try:
            db.mycur.execute("SELECT * FROM _medicalproject")
            records = db.mycur.fetchall()
            print("=================================================================================================================")
            print("| PRODUCT CODE   MEDICINE NAME   PACKING DETAILS   EXPIRY DATE   COMPANY NAME   BILL NUMBER  QUANTITY     RATE  |")
            print("=================================================================================================================")

            for row in records:
                print("| ", end="")
                print(str(row[0]).ljust(15, " "), end="")
                print(row[1].ljust(17, " "), end="")
                print(row[2].ljust(18, " "), end="")
                print(str(row[3]).ljust(14, " "), end="")
                print(row[4].ljust(15, " "), end="")
                print(str(row[5]).ljust(16, " "), end="")
                print(str(row[6]).ljust(10, " "), end="")
                print(str(row[7]).ljust(5, " "), end="|")
                print()
            print("==================================================================================================================")
        except Exception as e:
            print(f"Error displaying medicines: {e}")

    @staticmethod
    def search_medicine(db, med_name):
        cmd = "SELECT * FROM _medicalproject WHERE name LIKE %s"
        db.mycur.execute(cmd, ('%' + med_name + '%',))
        record = db.mycur.fetchone()

        if record is None:
            print("No record found.")
        else:
            print("PRODUCT CODE   MEDICINE NAME   PACKING DETAILS   EXPIRY DATE   COMPANY NAME   BILL NUMBER  QUANTITY     RATE")
            print(str(record[0]).ljust(15, " "), end="")
            print(record[1].ljust(17, " "), end="")
            print(record[2].ljust(18, " "), end="")
            print(str(record[3]).ljust(14, " "), end="")
            print(record[4].ljust(15, " "), end="")
            print(str(record[5]).ljust(16, " "), end="")
            print(str(record[6]).ljust(10, " "), end="")
            print(str(record[7]).ljust(15, " "), end="")
            print()

    @staticmethod
    def check_expiry(db):
        exp_date = datetime.date.today()
        cmd = "SELECT ProductCode, name, Expirydate, Batch FROM _medicalproject WHERE Expirydate <= %s"
        db.mycur.execute(cmd, (exp_date,))
        records = db.mycur.fetchall()

        print("PRODUCT CODE   NAME             EXPIRY DATE   BATCH")
        for row in records:
            print(str(row[0]).ljust(15, " "), end="")
            print(row[1].ljust(17, " "), end="")
            print(str(row[2]).ljust(14, " "), end="")
            print(str(row[3]).ljust(15, " "), end="")
            print()

    @staticmethod
    def display_companywise(db, company_name):
        cmd = "SELECT * FROM _medicalproject WHERE Company = %s"
        db.mycur.execute(cmd, (company_name,))
        records = db.mycur.fetchall()

        if not records:
            print("No record found.")
        else:
            for record in records:
                print(record)

    @staticmethod
    def delete_medicine(db, delete_code):
        cmd = "SELECT COUNT(*) FROM customertable WHERE Productcode = %s"
        db.mycur.execute(cmd, (delete_code,))
        total_record = db.mycur.fetchone()[0]

        if total_record == 0:
            cmd = "DELETE FROM _medicalproject WHERE ProductCode = %s"
            db.mycur.execute(cmd, (delete_code,))
            db.mycn.commit()
            print("Record has been deleted.")
        else:
            cmd = "UPDATE _medicalproject SET Quantity = 0 WHERE ProductCode = %s"
            db.mycur.execute(cmd, (delete_code,))
            db.mycn.commit()
            print("This medicine has already been sold, so it can't be deleted. The quantity has been set to zero.")


class Bill:
    def __init__(self, bill_number, customer_name, doctor_name, product_code, quantity):
        self.bill_number = bill_number
        self.customer_name = customer_name
        self.doctor_name = doctor_name
        self.product_code = product_code
        self.quantity = quantity

    def add_to_database(self, db):
        cmd = "INSERT INTO customertable VALUES (%s, %s, %s, %s, %s)"
        db.mycur.execute(cmd, (self.bill_number, self.customer_name, self.doctor_name, self.product_code, self.quantity))
        db.mycn.commit()
        print("Record has been added.")

    @staticmethod
    def display_bills(db):
        cmd = """
            SELECT CT.BillNumber, CT.Customername, CT.DoctorName, CT.Productcode, MDT.name, CT.Quantity, MDT.Rate, CT.Quantity * MDT.Rate AS Amount 
            FROM customertable CT 
            JOIN _medicalproject MDT ON CT.Productcode = MDT.ProductCode
        """
        db.mycur.execute(cmd)
        records = db.mycur.fetchall()

        print("BILL NUMBER      CUSTOMER NAME       DOCTOR NAME     PRODUCT CODE    MEDICINE NAME     QUANTITY       RATE     AMOUNT")

        for row in records:
            print(str(row[0]).ljust(15, " "), end="")
            print(row[1].ljust(24, " "), end="")
            print(row[2].ljust(17, " "), end="")
            print(str(row[3]).ljust(14, " "), end="")
            print(str(row[4]).ljust(15, " "), end="")
            print(str(row[5]).ljust(13, " "), end="")
            print(str(row[6]).ljust(7, " "), end="")
            print(str(row[7]).ljust(13, " "), end="")
            print()

    @staticmethod
    def search_bill(db, bill_number):
        cmd = """
            SELECT CT.BillNumber, CT.Customername, CT.DoctorName, CT.Productcode, MDT.name, CT.Quantity, MDT.Rate, CT.Quantity * MDT.Rate AS Amount 
            FROM customertable CT 
            JOIN _medicalproject MDT ON CT.Productcode = MDT.ProductCode 
            WHERE BillNumber = %s
        """
        db.mycur.execute(cmd, (bill_number,))
        record = db.mycur.fetchone()

        if record is None:
            print("No record found.")
        else:
            print("BILL NUMBER      CUSTOMER NAME       DOCTOR NAME     PRODUCT CODE    MEDICINE NAME     QUANTITY       RATE     AMOUNT")
            print(str(record[0]).ljust(15, " "), end="")
            print(record[1].ljust(24, " "), end="")
            print(record[2].ljust(17, " "), end="")
            print(str(record[3]).ljust(14, " "), end="")
            print(str(record[4]).ljust(15, " "), end="")
            print(str(record[5]).ljust(13, " "), end="")
            print(str(record[6]).ljust(7, " "), end="")
            print(str(record[7]).ljust(13, " "), end="")
            print()


class MedicalStore:
    def __init__(self):
        self.db = Database()

    def menu(self):
        while True:
            print("\n\n")
            print("1. Add Medicines")
            print("2. Display Medicines")
            print("3. Search Medicines")
            print("4. Check Expired Stock")
            print("5. Display Medicines Company-wise")
            print("6. Delete Medicines")
            print("7. Add New Bill")
            print("8. Display Bills")
            print("9. Search Bill")
            print("0. Exit")

            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.add_medicine()
            elif choice == 2:
                Medicine.display_medicines(self.db)
            elif choice == 3:
                med_name = input("Enter medicine name to search: ")
                Medicine.search_medicine(self.db, med_name)
            elif choice == 4:
                Medicine.check_expiry(self.db)
            elif choice == 5:
                company_name = input("Enter company name: ")
                Medicine.display_companywise(self.db, company_name)
            elif choice == 6:
                delete_code = int(input("Enter the product code to delete: "))
                Medicine.delete_medicine(self.db, delete_code)
            elif choice == 7:
                self.add_new_bill()
            elif choice == 8:
                Bill.display_bills(self.db)
            elif choice == 9:
                bill_number = int(input("Enter bill number to search: "))
                Bill.search_bill(self.db, bill_number)
            elif choice == 0:
                self.db.close()
                print("Thank you for visiting our medical store!")
                break
            else:
                print("Invalid choice! Please choose a valid option.")

    def add_medicine(self):
        product_code = int(input("Enter Product Code: "))
        name = input("Enter Medicine Name: ")
        packing = input("Enter Packing Details: ")
        expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")
        company = input("Enter Company Name: ")
        batch = input("Enter Batch Number: ")
        quantity = int(input("Enter Quantity: "))
        rate = int(input("Enter Rate: "))

        medicine = Medicine(product_code, name, packing, expiry_date, company, batch, quantity, rate)
        medicine.add_to_database(self.db)

    def add_new_bill(self):
        bill_number = int(input("Enter Bill Number: "))
        customer_name = input("Enter Customer Name: ")
        doctor_name = input("Enter Doctor Name: ")
        product_code = int(input("Enter Product Code: "))
        quantity = int(input("Enter Quantity: "))

        bill = Bill(bill_number, customer_name, doctor_name, product_code, quantity)
        bill.add_to_database(self.db)


# Running the program
if __name__ == "__main__":
    store = MedicalStore()
    store.menu()
