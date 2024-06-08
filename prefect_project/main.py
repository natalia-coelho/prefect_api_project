from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import requests

API_BASE_URL = "https://jsonplaceholder.typicode.com"

@task(retries=3, retry_delay_seconds=5)
def fetch_users():
    try:
        response = requests.get(f"{API_BASE_URL}/users", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as e:
        raise ValueError("Timeout occurred") from e

@task(retries=3, retry_delay_seconds=5)
def fetch_posts():
    try:
        response = requests.get(f"{API_BASE_URL}/posts", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout as e:
        raise ValueError("Timeout occurred") from e

@task
def process_data(users, posts):
    user_posts = {user['id']: [] for user in users}
    for post in posts:
        user_posts[post['userId']].append(post)
    return user_posts

@flow
def api_data_flow():
    users = fetch_users()
    posts = fetch_posts()
    processed_data = process_data(users, posts)
    print(processed_data)

if __name__ == "__main__":
    api_data_flow()
