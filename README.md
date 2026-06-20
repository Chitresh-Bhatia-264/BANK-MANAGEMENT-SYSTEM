#  Banking Management System (Python + MySQL)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange.svg)
![Status](https://img.shields.io/badge/Project-Completed-green.svg)
![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)

A **desktop banking application** built using Python, MySQL, and Tkinter.  
It simulates real-world banking operations like account creation, login, deposit, withdrawal, and balance management.

---

##  Features

-  Create new customer account  
-  Secure login system  
-  Deposit money  
-  Withdraw money with balance validation  
-  Check account balance  
-  View customer details  
-  MySQL database integration  
-  Tkinter GUI frontend  

---

##  Tech Stack

- Python   
- MySQL   
- Tkinter (GUI)  
- mysql-connector-python  
- bcrypt (password hashing)  
- python-dotenv (environment variables)

---

##  Project Structure
Bank Management System/
- │── database.py
- │── tk_backend.py
- |── bank.py
- |── customer.py
- |── main.py
- |── register.py
- │── frontend_tkinter.py
- │── .env
- │── .gitignore
- │── README.md




---





##  Install Dependencies
pip install mysql-connector-python bcrypt python-dotenv


## Create MySQL Database
CREATE DATABASE banking system;
## Setup .env file


## Run Project
python frontend_tkinter.py

## Security Features
- Sensitive credentials stored in .env file
- Parameterized SQL queries to prevent SQL injection

## Future Improvements
- Transaction history system
- Admin dashboard
- Email/OTP verification
- Interest calculation module
- ATM simulation mode


## Author

CHITRESH BHATIA
GitHub: https://github.com/Chitresh-Bhatia-264


## Project Highlights
- Real-world banking simulation
- Database-driven application
- Secure authentication system
- Clean modular Python architecture


## License

This project is for educational purposes only.

Copyright (c) 2026 Chitresh Bhatia

All rights reserved.

This software and associated files are proprietary and confidential.
Unauthorized copying, modification, distribution, or use of this code is strictly prohibited.

Permission must be obtained from the author before any use.



