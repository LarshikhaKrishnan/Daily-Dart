# Daily-Dart
An intuitive and interactive web application designed to help users manage their daily tasks, organize their schedules, and stay productive. With features like task management, a month-wise calendar, and a to-do list, this planner ensures users can efficiently track and manage their tasks.
# 🗓️ Daily Planner Web App

A simple and interactive daily planner built using **Flask** and **CSV file storage**. This application allows users to:

- Sign up and log in securely
- View monthly calendars
- Add/view/delete tasks for specific days
- Maintain a full to-do list with deadlines

## 📁 Project Structure
/daily-planner/
│
├── app.py # Flask backend application
├── planner.csv # Stores user tasks
├── users.csv # Stores user credentials (hashed)
├── static/
│ └── bg.jpeg # Background image used across pages
├── templates/
│ ├── login.html
│ ├── signup.html
│ ├── calendar.html
│ ├── day.html
│ ├── todo.html
│ └── index.html # Optional or unused directly
├── README.md # Project documentation


## 🚀 Features

- **User Authentication**: Secure sign-up/login system using SHA-256 password hashing.
- **Calendar View**: Monthly view with clickable dates to manage daily tasks.
- **Day View**: Add and delete tasks for specific days.
- **To-Do List**: See all tasks across days, sorted by date.
- **CSV Storage**: Lightweight storage solution using `planner.csv` and `users.csv`.

## 🧑‍💻 Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python, Flask
- **Data Storage**: CSV files


