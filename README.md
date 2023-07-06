
# Inventory and Monitoring System
A web-based software that tracks and monitors withdrawal, deposit, and
delivery of materials in conjunction with logging the creation and acceptance of quotations across multiple projects and satellite warehouses 



## Tech Stack

**Client:** HTML, TailwindCSS

**Server:** Node, Django, JS, SQLite


## Features

- Responsive
- Role-based per user group within the organization
  - Varying access depending on job responsibility
- Custom administrator panel to modify access and permissions
#### Profile Management
  - Update location / project location 
  - Change password 
#### Custom dashboard 
  - Summarized or pending tasks that require action
#### Inventory Management
- View inventory
    - Filter table by current location or all
- Add new inventory items or deposit 
- Withdraw inventory
    - From users location 
    - View history
- Recount inventory 
- Settings per item
    - Can set minimum amount of an item before auto filling PR form 
    - Can set amount to be restocked when hitting the minimum 
- Transfer Inventory between locations 
    - Verify and delete transfers between locations 
#### Quotation Management 
- Automatically generate depending on supply count 
- View pending and completed purchase requests
    - View and create quotations within a purchase request      
- Approve or reject quotations 
#### Report Damaged Inventory 
- Verify and Unverify reported damages 
#### Delivery Management 
- View list of accomplished and pending deliveries 
- Confirm delivery arrivals 
- View contents of delivery and date of arrival 
- Set Single or Multiple delivery for an approve quotation
#### Supplier Management 
- View list of suppliers 
- View list of previous transactions with a specific supplier
## Run Locally

Clone the project

```bash
  git clone https://github.com/Havoc-1/aceainventory.git
```

Go to the project directory

```bash
  cd ./inventoryproject/
```

Install dependencies

```bash
  pip -r requirements.txt
```

Start the server

```bash
  python manage.py runserver
```


## Access
Account credentials 

| Account Name  | Password |
| ------------- |-------------| 
| admin      | pass | 
| Engineering     | Department00 | 
| Finance     | Department00 | 
| Management     | Department00 | 

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Used By

This project is used by the following companies:

- ACEA Engineering Services
## Authors

- [@Meepster212](https://github.com/Meepster212)
- [@Havoc-1](https://github.com/Havoc-1)
