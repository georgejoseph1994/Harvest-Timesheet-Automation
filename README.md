# Harvest Timesheet Automation

Automate filling your Harvest timesheet

## Features

-   Automatically fills your Harvest timesheet for a given date.
-   Easily configurable with environment variables and a config file.

## Setup

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/georgejoseph1994/Harvest-Timesheet-Automation.git
    cd Harvest-Timesheet-Automation
    ```

2.  **Create and activate a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**

    -   Copy `.env.example` to `.env`

        ```sh
        cp .env.example .env
        ```

    -   Fill in the credentials

        ```
        HARVEST_ACCOUNT_ID=your_account_id
        HARVEST_ACCESS_TOKEN=your_access_token
        ```

5.  **Configure your timesheet entries:**
    -   Edit `config/harvest_config.py` to define your daily timesheet entries.

## Usage

You can now run the script with flexible date options:

-   **For a specific date:**

    ```sh
    python main.py --date=17/05/2025
    ```

-   **For a date range:**

    ```sh
    python main.py --start=12/05/2025 --end=16/05/2025
    ```

-   **For the current week (Monday to Friday):**
    ```sh
    python main.py
    ```

If no parameters are provided, the script will fill your timesheet for the current week's Monday to Friday.

### Example

```sh
python main.py --date=20/05/2025
python main.py --start=13/05/2025 --end=15/05/2025
python main.py
```

**Note:**  
Date format should be `DD/MM/YYYY`.
