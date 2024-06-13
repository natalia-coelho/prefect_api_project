# Consuming APIs with Prefect ✨

This is a simple app to demonstrate the Prefect workflow orchestration using the Rick and Morty API.

### Features

- Fetch characters and locations from the Rick and Morty API.
- Simulate random timeouts to demonstrate retry functionality.
- Use Prefect to orchestrate the workflow.

### Why Rick and Morty API?

I chose to use the Rick and Morty API because I'm a big fan of the series and it provides a fun and interesting dataset to work with.

### Implementation Details

- Implemented tasks to fetch characters and locations.
- Used Prefect to handle workflow orchestration, including retrying on timeout errors.
- Added logging to track the number of characters and locations found.

### My Impressions

I really enjoyed using Prefect; it's a powerful tool for orchestrating workflows and monitoring services.

### How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/prefect-api-example.git
   cd prefect-api-example

2. Install necessary packages
    ```bash
    pip install -r requirements.txt
    ```

3. Run the prefect flow
    ```bash
    python main.py
    ```