import warnings

warnings.filterwarnings("ignore", category=Warning)

# Import necessary libraries and tools
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, time
from pytz import timezone
import psycopg2
import os
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

# Create Flask app and Slack client objects
app = Flask(__name__)
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# Connect to the PostgreSQL database
conn = psycopg2.connect(host=os.environ['PG_HOST'],
                        database=os.environ['PG_DB'],
                        user=os.environ['PG_USER'],
                        password=os.environ['PG_PASSWORD'])


# Get all tasks from the database
def get_tasks():
  cur = conn.cursor()
  cur.execute("SELECT * FROM task")
  tasks = []
  for row in cur.fetchall():
    task_id, task_title, task_description = row
    tasks.append({
      "id": task_id,
      "title": task_title,
      "description": task_description
    })
  return tasks


# Add a new task to the database
def add_task(title, description):
  cur = conn.cursor()
  cur.execute(
    "INSERT INTO task (title, description) VALUES (%s, %s) RETURNING id",
    (title, description))
  task_id = cur.fetchone()[0]
  conn.commit()
  return task_id


# Mark a task as completed in the database
def complete_task(task_id):
  cur = conn.cursor()
  cur.execute("UPDATE task SET completed = true WHERE id = %s", (task_id, ))
  conn.commit()


# Route to get all tasks
@app.route('/tasks')
def get_all_tasks():
  tasks = get_tasks()
  return jsonify(tasks)


# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task_route():
  data = request.json
  title = data.get('title')
  description = data.get('description')

  if not title or not description:
    return jsonify({'error': 'Title and description are required'}), 400

  task_id = add_task(title, description)
  return jsonify({'id': task_id})


# Route to mark a task as complete
@app.route('/tasks/<int:task_id>', methods=['POST'])
def complete_task_route(task_id):
  complete_task(task_id)
  return jsonify({'id': task_id})


# Function to send a message to Slack
def send_slack_message(channel_id, message):
  try:
    response = client.chat_postMessage(channel=channel_id, text=message)
    return response['ts']
  except SlackApiError as e:
    print(f"Error sending message to {channel_id}: {e}")
    return None


# Route to receive events from Slack
@app.route('/events', methods=['POST'])
def slack_event_received():
  data = request.json
  if data.get('type') == 'event_callback':
    event = data.get('event')
    if event.get('type') == 'message':
      user = event.get('user')
      text = event.get('text')
      channel_id = event.get('channel')
      message_ts = event.get('ts')

      # If message starts with "Task:", add a new task based on title and description in message
      if text.startswith('Task:'):
        title, description = text.split(':', 1)[1].split('\n', 1)
        task_id = add_task(title, description)
        send_slack_message(user, f'Task "{title}" added with ID {task_id}')

      # If message starts with "Completed:", mark the task with the given ID as complete
      elif text.startswith('Completed:'):
        task_id = int(text.split(':', 1)[1])
        complete_task(task_id)
        send_slack_message(user, f'Task {task_id} completed successfully')
      else:
        pass

  return jsonify({'success': True})


# Function to send a daily reminder message to Slack
def send_reminder():
  try:
    message = "Don't forget to submit your daily testing questions!"
    channel_id = os.environ['SLACK_CHANNEL_ID']
    response = client.chat_postMessage(channel=channel_id, text=message)
    return response['ts']
  except SlackApiError as e:
    print(f"Error sending message to {channel_id}: {e}")
    return None


# Route to send a daily reminder message
@app.route('/reminder', methods=['POST'])
def send_reminder_route():
  send_reminder()
  return jsonify({'success': True})


# Set up an apscheduler to send the daily reminder message at a specific time
sched = BlockingScheduler(timezone='UTC')
sched.add_job(send_reminder, 'cron', hour=13, minute=0)

if __name__ == "__main__":
  # Start the Flask app and the apscheduler
  app.run(debug=True)
  sched.start()
