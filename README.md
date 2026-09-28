# Jira Command-Line Replica

A command-line-based project management and ticket-tracking system inspired by the core workflow of tools like Jira.

This project replicates the basic ticket creation, project management, team management, and organisation-level access control used in IT project management systems.

---

## 📌 Project Overview

The **Jira Command-Line Replica** is a Python and MySQL-based application designed to simulate a basic issue/ticket tracking system used in the IT industry.

Users register under an **Organisation (Company)**, create and manage projects, form teams, assign responsibilities, and track project-related tickets.

The application implements a role-based access system consisting of:

- Super Admin
- Admin
- Manager
- Employee

Each role has different permissions based on its responsibilities within the organisation.

---

## 🏢 Organisation Management

The application follows an organisation-based structure.

Users must register under an organisation before they can access the system.

Once an organisation is created:

- The **first registered employee** of the organisation automatically becomes the **Super Admin**.
- The Super Admin can create projects for the organisation.
- Projects can have multiple managers and employees.
- Users and projects remain associated with their respective organisation.

This provides a basic representation of a **multi-organisation project management system**.

---

## 👨‍💼 Role-Based Access Control

The application implements different levels of permissions for different users.

### 🔴 Super Admin

The Super Admin has the highest level of privileges within an organisation.

Responsibilities and permissions include:

- Create projects for the organisation
- Assign Managers to projects
- Assign Admins within the organisation
- Edit project information
- Remove Admins from the organisation
- Manage organisation-level administration

The first registered employee of an organisation is automatically assigned the Super Admin role.

---

### 🟠 Admin

The Admin has most of the project and organisation management capabilities of a Super Admin.

An Admin can:

- Create projects
- Assign Managers to projects
- Edit project information
- Manage project-related activities

However, an Admin **cannot add or remove Admins** from the organisation.

---

### 🟡 Manager

Managers are responsible for managing individual projects and their teams.

Managers can:

- View projects assigned to them
- Add Employees to their projects
- Remove Employees from their projects
- Create tickets
- Edit tickets
- View tickets
- Track project-related work

Managers are assigned to projects by an Admin or Super Admin.

---

### 🟢 Employee

Employees have limited permissions compared to Managers.

Employees can:

- View tickets
- Create tickets
- Edit tickets

Employees cannot manage project members or perform administrative operations.

---

## 🎫 Ticket Management

Tickets are the primary tracking mechanism within a project.

They are used to record and track different types of work, issues, and improvements.

Each ticket can contain information such as:

- Ticket title
- Description
- Ticket type
- Assigned employee
- Due date
- Project
- Other relevant tracking information

Tickets can be modified as the project progresses.

### Ticket Types

Currently, the application supports the following ticket types:

- 🐞 **Bug** – Used to track defects or issues.
- 🚀 **Improvement** – Used to track improvements to existing functionality.
- 📋 **Task** – Used to track a specific piece of work.

At the current stage of development, all ticket types follow the same basic workflow.

Additional ticket-specific functionality can be introduced in future versions.

---

## 🔄 Basic Application Flow

```text
Organisation Registration
          │
          ▼
 First Employee Registers
          │
          ▼
    Becomes Super Admin
          │
          ▼
     Create Projects
          │
          ▼
 Assign Admins / Managers
          │
          ▼
    Managers Build Teams
          │
          ▼
 Employees Added to Projects
          │
          ▼
     Create Tickets
          │
          ▼
 Assign / Edit / Track Tickets



 ## 🛠️ Skills & Technologies Used

### 💻 Programming

* **Python**
* Python Fundamentals
* Object-Oriented Programming (OOP)
* Classes and Objects
* Encapsulation
* Inheritance
* Polymorphism
* Functions and Modular Programming
* Conditional Statements and Loops
* Exception Handling
* Application Flow & Logic Building

### 🗄️ Database & SQL

* **MySQL**
* **SQL**
* Database Design
* Relational Database Concepts
* CRUD Operations
* Primary Keys & Foreign Keys
* Table Relationships
* Data Retrieval & Manipulation
* Database-driven Application Development

### 🔐 Application Design

* **Role-Based Access Control (RBAC)**
* User & Role Management
* Organisation Management
* Project Management
* Ticket / Issue Management
* Business Logic Implementation

### 🖥️ Software Development

* Command-Line Interface (CLI) Application Development
* Modular Application Design
* Input Validation
* Error Handling
* Workflow Design
* Connecting Python Applications with MySQL

### 🔧 Version Control & Development Tools

* **Git**
* **GitHub**
* Version Control
* Code Commit & History Management

### 📌 Core Skill Stack

```text
Python
  │
  ├── OOP
  ├── Application Logic
  ├── CLI Development
  └── MySQL Connectivity
          │
          ▼
        MySQL
          │
          ├── SQL
          ├── Database Design
          └── CRUD Operations
          │
          ▼
   Project Management System
          │
          ├── Organisation Management
          ├── Role-Based Access Control
          ├── Project Management
          ├── Team Management
          └── Ticket Management
          │
          ▼
     Git & GitHub
```

### 🧰 Technology Stack

| Category              | Technologies / Skills                            |
| --------------------- | ------------------------------------------------ |
| Language              | Python                                           |
| Programming           | OOP, Functions, Control Flow, Exception Handling |
| Database              | MySQL                                            |
| Query Language        | SQL                                              |
| Application Type      | Command-Line Interface (CLI)                     |
| Architecture Concepts | RBAC, CRUD, Entity Relationships                 |
| Version Control       | Git                                              |
| Repository Hosting    | GitHub                                           |