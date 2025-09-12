# Permissions and Groups Setup

This project demonstrates managing permissions and groups in **Django**.

---

## 📌 Custom Permissions

The **Book** model defines the following permissions:

- `can_view` → Can view book records  
- `can_create` → Can create book records  
- `can_edit` → Can edit book records  
- `can_delete` → Can delete book records  

---

## 👥 Groups

- **Viewers** → `can_view`  
- **Editors** → `can_view`, `can_create`, `can_edit`  
- **Admins** → all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`)  

---

## 🔒 Views Protection

Views are protected using `@permission_required`:

- `book_list` → requires **can_view**  
- `book_create` → requires **can_create**  
- `book_edit` → requires **can_edit**  
- `book_delete` → requires **can_delete**  

---

## 🧪 Testing

1. Create users via **Django Admin**  
2. Assign them to appropriate **groups**  
3. Try accessing book pages to verify **permissions enforcement**  

---
