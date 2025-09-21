# Ecommerce
# 🥖 Django Bakery Cart System

A full-featured **Bakery Cart Management System** built with Django.  
This project allows users to browse bakery products, add them to a cart, update quantities, checkout securely with **Razorpay integration**, and download invoices as **PDFs** after purchase.  

---

## 🚀 Features

- 🏠 **Homepage**
  - Carousel banner
  - Product listing with category filters
  - Add-to-cart functionality
  - Blog section

- 🛒 **Cart System**
  - Add/remove products
  - Update product quantities with increment/decrement buttons
  - Session-based cart management
  - Real-time subtotal & final price updates

- 💳 **Checkout**
  - Customer information form
  - Razorpay payment gateway integration
  - Dynamic subtotal and total amount calculation
  - Save checkout data in the database

- 📄 **Invoice Generation**
  - Automatically generate and download PDF invoices after successful payment

- ⚙️ **Admin Panel**
  - Manage products, categories, and customers
  - View and track orders

---

## 🛠️ Tech Stack

- **Backend:** Django, Python
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite / MySQL
- **Payments:** Razorpay API
- **PDF Generation:** ReportLab

---

## 📂 Project Structure

bakery_cart/
│── bakery_cart/ # Main project settings
│── app/ # Core application (products, cart, checkout, etc.)
│ ├── models.py # Database models
│ ├── views.py # Business logic
│ ├── urls.py # App URLs
│ ├── templates/ # HTML templates
│ └── static/ # CSS, JS, Images
│── templates/ # Global templates
│── manage.py # Django management script
