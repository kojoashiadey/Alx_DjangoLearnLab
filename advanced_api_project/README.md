# 📚 Advanced API Project

This project demonstrates building a **Django REST Framework (DRF) API** with advanced features.

---

## 🚀 Features
- **Custom Serializers**  
  - Nested relationships  
  - Validation  

- **Generic Views**  
  - CRUD operations for books  

- **Permissions**  
  - **Read-only** for public users  
  - **Write access** (create/update/delete) for authenticated users  

---

## 📡 API Endpoints

### Books
- `GET /api/books/` → List all books (**public**)  
- `GET /api/books/<id>/` → Retrieve book by ID (**public**)  
- `POST /api/books/create/` → Create a new book (**authenticated only**)  
- `PUT /api/books/<id>/update/` → Update a book (**authenticated only**)  
- `DELETE /api/books/<id>/delete/` → Delete a book (**authenticated only**)  

---

## 🔐 Permissions
- **Read** → Open to everyone  
- **Write** (Create/Update/Delete) → Requires authentication  

---

## 🧪 Testing
1. Use the **Django Admin Panel** to add authors/books.  
2. Test endpoints with **Postman** or `curl`.  

Example:

```bash
curl -X GET http://127.0.0.1:8000/api/books/
