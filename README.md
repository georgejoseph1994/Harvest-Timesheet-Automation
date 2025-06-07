# Harvest Timesheet Automation

## Features

-   Bulk fill your Harvest time sheet with pre configured time sheet records.
-   Auto skip public holidays and weekends when giving date ranges based on your location

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
    -   Copy the example config file:
        ```sh
        cp src/config/harvest_config.example.py src/config/harvest_config.py
        ```
    -   Edit `src/config/harvest_config.py` to define your daily time sheet entries. For TaskId and Project Id inspect your network request when viewing a filled in harvest page

## Usage

You can now run the script with flexible date options:

-   **For the current week (Monday to Friday):**
       If no parameters are provided, the script will fill your timesheet for the current week's Monday to Friday.

    ```sh
    python main.py
    ```

-   **For a specific date:**

    ```sh
    python main.py --date=17/05/2025
    ```

-   **For a date range:**

    ```sh
    python main.py --start=12/05/2025 --end=16/05/2025
    ```

-   **View existing time entries:**

    ```sh
    python main.py --show --start=12/05/2025 --end=16/05/2025
    ```

-   **Delete time entries for a date range:**

    ```sh
    python main.py --delete --start=12/05/2025 --end=16/05/2025
    ```

## Disclaimer

**⚠️ USE AT YOUR OWN RISK ⚠️**

This software is provided "as is" without warranty of any kind. The authors and contributors are not responsible for any data loss, incorrect time entries, or any other issues that may arise from using this automation tool.

Please:
- Test thoroughly with a small date range before using on larger datasets
- Verify your time entries after running the automation
- Keep backups of your existing timesheet data
- Ensure you comply with your organization's policies regarding automated timesheet filling

By using this software, you acknowledge that you understand the risks and agree to use it at your own discretion.


