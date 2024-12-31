# PuthuVarshamBot🎉

**PuthuVarshamBot** is an interactive Discord bot designed to make your New Year celebrations more exciting and meaningful. It features both static and automated countdowns to the New Year, motivational and festive quotes, sends greetings, resolution management, and much more!

## Features ✨

- **Static Countdown**: Displays a one-time countdown to the New Year for a specified date and time.
- **Automated Countdown**: Updates the countdown in real-time in a specific channel, ensuring users always know how much time is left until the New Year.
- **Motivational Quotes**: Shares daily motivational and festive quotes upon request.
- **Festive Greetings**: Sends personalized New Year greetings to users.
- **Resolutions Management**: Allows users to create, view, update, and delete their New Year resolutions.
- **Interactive Experience**: Engages users with meaningful and fun interactions.

---

## Installation 🚀

### Prerequisites
- Python 3.8+
- Discord bot token (get it from the [Discord Developer Portal](https://discord.com/developers/applications))  

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/alvin-dennis/PuthuVarshamBot.git
    ```

2. Navigate to the project directory:
    ```bash
    cd PuthuVarshamBot
    ```

3. Set up a virtual environment:
    - For **Linux/macOS**:
      ```bash
      python3 -m venv venv
      ```
    - For **Windows**:
      ```bash
      python -m venv venv
      ```

4. Activate the virtual environment:
    - For **Linux/macOS**:
      ```bash
      source venv/bin/activate
      ```
    - For **Windows**:
      ```bash
      venv\Scripts\Activate.ps1
      ```

5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Set up the configuration:
    Create a `.env` file in the root directory and add the following content:
    ```env
    DISCORD_BOT_TOKEN=your_discord_bot_token
    DB_HOST=your_database_host
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    ```

7. (Optional) If necessary, you can install `audioop module` using the following command:
    ```bash
    pip install audioop-lts
    ```

8. Run the bot:
    ```bash
    python3 bot.py
    ```
---

## Commands 📜

### Greetings
- **`/hello`**: Greets the user with a friendly "Hello!"

- **`/greet`**: Sends a personalized greeting to the user or others.

- **`/wish [message]`**: Sends a personalized new year wish message tp the user or others.

- **`/universal-newyear-greet`**: Celebrate the New Year with a greeting in your language! This command sends a personalized New Year greeting based on the language preference of the user.

### Quotes
- **`/quotes`**: Shares a random motivational or festive quote.

### Countdown
- **Static Countdown**:  
  **`/static-countdown`**  
  Displays the countdown to a specific date and time in the format `⏳ Only **{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds** to go! 🕒✨`.

- **Automated Countdown**:  
  **`/automated-countdown`**  
  Starts an automated countdown to the New Year, updating every second.

### Resolutions
- **`/resolutions`**: Opens an interactive menu for managing New Year resolutions:
  - **Create a Resolution**: Add a new resolution.
  - **Read Your Resolutions**: View your current resolutions.
  - **Update a Resolution**: Modify an existing resolution.
  - **Delete a Resolution**: Remove a resolution.

### New Year Predictions
- **`/predict`**: Get a prediction for your zodiac sign for 2025.

### Utility
- **`/ping`**: Checks the bot's status and responds with "Pong!" to confirm the bot is online.

- **`/echo [message]`**: Echoes back the message provided by the user.

---

## License 📝

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.


Let’s make this New Year unforgettable! 🎆

