class Bank:
    def __init__(self, acc_no, name, address, phone, balance, pin):
        self.acc_no = acc_no
        self.name = name
        self.address = address
        self.phone = phone
        self.balance = balance
        self.pin = pin

    def verify_pin(self):
        entered_pin = input("Enter your ATM PIN: ")
        if entered_pin == self.pin:
            print("✅ PIN Verified Successfully!\n")
            return True
        else:
            print("❌ Incorrect PIN! Access Denied.\n")
            return False

    def my_details(self):
        print("------ Account Details ------")
        print("Account Number:", self.acc_no)
        print("Name:", self.name)
        print("Address:", self.address)
        print("Phone:", self.phone)
        print("Balance:", self.balance)
        print("-----------------------------\n")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        self.balance += amount
        print(f"💰 {amount} deposited. New balance: {self.balance}\n")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        if amount <= self.balance:
            self.balance -= amount
            print(f"💸 {amount} withdrawn. Remaining balance: {self.balance}\n")
        else:
            print("⚠️ Insufficient balance!\n")

    def check_balance(self):
        print(f"📊 Current Balance: {self.balance}\n")


# Create a Bank object (dummy data)
Bn_obj = Bank(575944959040499, "Bhupesh", "Neemrana", "7357975446", 6000, "1234")

# ATM Menu
if Bn_obj.verify_pin():
    while True:
        print("----- ATM Menu -----")
        print("1. View Account Details")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            Bn_obj.my_details()
        elif choice == "2":
            Bn_obj.deposit()
        elif choice == "3":
            Bn_obj.withdraw()
        elif choice == "4":
            Bn_obj.check_balance()
        elif choice == "5":
            print("Thank you for using our ATM. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice! Please try again.\n")
