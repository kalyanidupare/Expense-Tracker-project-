# Expense-Tracker-project-

A modern, full-featured web application for tracking personal expenses with a clean and responsive user interface.

![Expense Tracker](https://raw.githubusercontent.com/yourusername/expense-tracker/main/screenshots/expense-tracker.png)

## Features

- 💰 **Expense Management**: Add, edit, and delete expenses
- 🔍 **Real-time Search**: Search expenses by description or category
- 📊 **Data Export**: Export expenses to CSV format
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 📅 **Date Tracking**: Automatically tracks when expenses are added or modified
- 💾 **Data Persistence**: Stores all data in MongoDB database
- ⚡ **Real-time Updates**: Instant updates without page refresh
- 🎨 **Modern UI**: Clean and intuitive user interface with Bootstrap 5

## Technologies Used

- **Backend**:
  - Python 3.x
  - Flask (Web Framework)
  - PyMongo (MongoDB Driver)
  - Pandas (Data Processing)

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript (ES6+)
  - Bootstrap 5
  - Font Awesome Icons

- **Database**:
  - MongoDB

## Prerequisites

Before running this application, make sure you have the following installed:
- Python 3.x
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running on your system:
```bash
# Default MongoDB connection URL
mongodb://localhost:27017/
```

5. Run the application:
```bash
python app.py
```

6. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### Adding an Expense
1. Fill in the description, amount, and category fields
2. Click "Add Expense"

### Searching Expenses
1. Use the search box at the top of the page
2. Type any text to search in descriptions and categories
3. Results update in real-time as you type

### Editing an Expense
1. Click the "Edit" button next to the expense
2. Modify the details in the popup modal
3. Click "Save Changes"

### Deleting an Expense
1. Click the "Delete" button next to the expense
2. Confirm the deletion when prompted

### Exporting Data
1. Click the "Export Monthly Statement" button
2. The file will be downloaded as 'monthly_statement.csv'

## Project Structure

```
expense-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/
│   ├── script.js         # Frontend JavaScript
│   └── styles.css        # Additional styles
├── templates/
│   └── index.html        # Main HTML template
└── README.md             # Project documentation
```

## API Endpoints

- `GET /`: Main application page
- `GET /get_expenses`: Retrieve all expenses
- `POST /add_expense`: Add a new expense
- `PUT /update_expense/<id>`: Update an existing expense
- `DELETE /delete_expense/<id>`: Delete an expense
- `GET /search_expenses`: Search expenses
- `GET /export_monthly_statement`: Export expenses to CSV

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Bootstrap for the responsive design framework
- Font Awesome for the icons
- MongoDB for the database
- Flask for the web framework

## Contact

Your Name - [kalyanidupare143@gmail.com](mailto:your.email@example.com)

Project Link: [https://github.com/kalyanidupare/expense-tracker](https://github.com/yourusername/expense-tracker)

---
⭐️ If you found this project helpful, please give it a star on GitHub! 
