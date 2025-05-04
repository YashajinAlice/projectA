# ProjectA

ProjectA is a Python-based application that serves as a task manager and bug tracker, featuring a user-friendly interface and music integration. The application includes functionalities for managing to-do items, tracking bugs, launching applications and games, and displaying announcements.

## Features

- **Home Page**: Displays the current time, version number, and operating system information.
- **To-Do List**: Allows users to add, edit, delete, and mark tasks as complete, moving them to a history section.
- **Bug Tracker**: Records bugs with details such as project name, error description, severity, and priority, allowing users to mark them as resolved.
- **Application Launcher**: Displays an icon for launching applications, tracking their runtime.
- **Game Launcher**: Displays an icon for launching games, tracking their runtime.
- **About Page**: Provides information about the author, version number, update date, and a feature to check for updates and display announcements.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/projectA.git
   ```
2. Navigate to the project directory:
   ```
   cd projectA
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Updates

The application checks for updates from the GitHub repository on startup. If an update is available, it will automatically apply the update and display the new version number.

## Announcements

For the latest announcements, refer to the `data/announcements.md` file, which is updated with each release.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.