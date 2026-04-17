POS API
Project Overview
The POS API is a backend system designed to manage users, products, sales, and reporting.
This project follows RESTFUL principles to ensure scalability,
maintainability, and ease of integration with front-end applications.

Features
1. User Management
    List:
    Create:
    Update:
    Delete:

1.1. Auth
    Register: Create a new user account.
    Login: Authenticate users and issue access tokens.
    Logout: Revoke user sessions or tokens.
    Reset Password: Securely reset user passwords.

1. Category Management
   List Categories: Retrieve all existing categories.
   Create Category: Add a new product category.
   Update Category: Modify existing category details.
   Delete Category: Remove an existing category.

2. Product Management
   Each product record includes an image column.
   List Products: Retrieve all available products.
   Create Product: Add a new product with details and image.
   Update Product: Edit existing product information or image.
   Delete Product: Remove a product from the database.

3. Invoice Management
   Manages invoices containing customer and transaction details.
   Supports creating, viewing, and managing sales invoices.

4. Invoice Detail Management
   Create Sale: Add sale details to an invoice.
   Update Sale Details: Modify existing sale entries.
   Delete Sale Details: Remove sale records.

5. Reporting
   Sales Reports:
   Daily Sales
   Weekly Sales
   Monthly Sales    by Criteria (SaleBy):
   Generate reports based on specific criteria such as product, category, or user.

Technology Stack
   Backend Framework: Flask
   Database: MySQL / PostgresSQL / SQLite
   Authentication: JWT (JSON Web Token)
   Data Format: JSON-Postman
   
Submit
   Project Source code upload to GitHub
   Record Video Demo
   Send in telegram group's topic
   ** postman_collection **
   ---]]