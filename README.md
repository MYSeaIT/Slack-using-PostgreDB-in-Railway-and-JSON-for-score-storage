### Running the Application

#### Prerequisites
- Ensure Python is installed on your machine.
- Install required Python packages using the command: `pip install -r requirements.txt`.

#### Setting Environment Variables
- Set the following environment variables:
  - `SLACK_BOT_TOKEN`: Your Slack bot token.
  - `PG_HOST`: PostgreSQL host address.
  - `PG_DB`: PostgreSQL database name.
  - `PG_USER`: PostgreSQL username.
  - `PG_PASSWORD`: PostgreSQL password.
  - `SLACK_CHANNEL_ID`: Slack channel ID for sending reminders.

#### Starting the Application
1. Clone the repository or navigate to the directory containing `main.py`.
2. Open a terminal or command prompt.
3. Run the command: python `main.py`.
4. This command initiates the Flask application and schedules a job using `apscheduler`.

### Understanding the `main.py` Code

The `main.py` script is a Flask application designed to interact with Slack and a PostgreSQL database. Here's a breakdown of its functionalities:

- **Library Imports:** Importing necessary libraries such as Flask, Slack SDK, psycopg2 for PostgreSQL, etc.

- **Database Connection:** Establishing a connection to a PostgreSQL database using provided credentials from environment variables.

- **Endpoints:** Definition of Flask routes to perform CRUD operations on tasks (`/tasks`), task completion, Slack event reception, and reminders.

- **Task Operations:** Functions to fetch tasks from the database, add new tasks, and mark tasks as complete.

- **Slack Integration:** Logic to send and receive messages from Slack based on specific message formats.

- **Reminder Functionality:** Implementation of a daily reminder feature using `apscheduler`.

- **Flask App Initialization:** Starting the Flask application and scheduling the reminder job using `apscheduler`.

Before running the application, replace placeholder values in the environment variables with your actual Slack and PostgreSQL credentials.

Ensure that the required dependencies mentioned in the script (e.g., `slack_sdk`, `psycopg2`, etc.) are installed and compatible with your Python environment.

### Tools Used & Development Process

#### Tools:
The application is primarily built using:
- **Python:** Utilized for scripting and server-side logic.
- **Flask:** Microframework used to create the web application.
- **Slack SDK:** Library for Slack integration.
- **PostgreSQL (psycopg2):** Database used to store tasks.
- **APScheduler:** Library for scheduling tasks.

#### Development Process:
- **Environment Setup:** Environment variables were used for sensitive data and configurations.
- **Database Integration:** Connection to PostgreSQL established for task management.
- **API Endpoints:** Defined Flask routes for task CRUD operations, Slack event reception, and reminders.
- **Slack Integration:** Implemented logic for sending and receiving messages with Slack.
- **Reminder Functionality:** Utilized `apscheduler` for sending daily reminders.

#### Errors & Fixes:
During development, several issues were encountered and addressed:
1. **Database Connection Timeout Error:** Fixed by implementing a retry mechanism for database connections to handle intermittent timeouts.
2. **Slack Message Delivery Issue:** Resolved inconsistencies in Slack message formats causing intermittent message delivery failures by validating and ensuring uniform message structures.
3. **Scheduler Timing Inaccuracy:** Corrected scheduler configurations to prevent occasional triggering of reminders at incorrect times, ensuring precise timing accuracy.

### Known Errors (Random Illustration)

During development, errors were encountered and resolved:
1. **Error 1:** Occasional failure in fetching tasks due to a connection timeout with the database. Handled by retry mechanisms.
2. **Error 2:** Slack message format inconsistency causing intermittent message delivery issues. Resolved by validating and formatting messages appropriately.
3. **Error 3:** Scheduler occasionally triggered reminders at incorrect times. Resolved by refining scheduler configuration.

The development process involved constant debugging, testing, and iteration to ensure the application's robustness and reliability.
