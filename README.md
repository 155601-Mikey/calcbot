````markdown
# CalcBot: A Versatile Discord Math and Conversion Bot

This is CalcBot, a powerful Discord bot that empowers you to perform various mathematical tasks and conversions directly within your server and DMs. Streamline your workflow and enhance mathematical exploration with its diverse capabilities!

**Features:**

* **Math Powerhouse:** Solve simple and complex expressions/equations using `/math`. Supports basic arithmetic, exponentiation, radicals, pi (π), and more.
* **Visualization Maestro:** Generate plots of mathematical functions with the intuitive `/plot` command.
* **Unit & Currency Guru:** Effortlessly convert between various units and currencies using `/convert`.
* **Calculation History:** Access your recent interactions with `/history`.
* **Custom Variable Wizard:** Define and manage custom variables with `/setvar` for streamlined calculations.
* **Help at Hand:** Get this help message and detailed instructions with `/help`.

**Installation (Prerequisites):**

1. **Python 3.x:** Ensure you have Python 3.x installed ([https://www.python.org/downloads/](https://www.google.com/url?sa=E&source=gmail&q=https://www.google.com/url?sa=E%26source=gmail%26q=https://www.python.org/downloads/)). Check with `python3 --version` in your terminal.

2. **Required Libraries:** Install necessary libraries using `pip`:

   ```bash
   pip install discord sympy matplotlib flask requests python-dotenv
````

**Setup:**

1.  **Create a Discord Application:** Visit the Discord Developer Portal ([https://discord.com/developers/applications](https://www.google.com/url?sa=E&source=gmail&q=https://www.google.com/url?sa=E%26source=gmail%26q=https://www.google.com/url?sa=E%26source=gmail%26q=https://www.google.com/url?sa=E%26source=gmail%26q=https://discord.com/developers/applications)) and create a new application.

2.  **Bot Token:** In the "Bot" section of your application, create a bot user and copy the generated token (needed later).

3.  **Currency Conversion API Key (Optional):** If you plan to use currency conversions, sign up for a free API key at [https://exchangerate-api.com/](https://www.google.com/url?sa=E&source=gmail&q=https://www.google.com/url?sa=E%26source=gmail%26q=https://www.google.com/url?sa=E%26source=gmail%26q=https://exchangerate-api.com/).

**Configuration (Create a `.env` file):**

  - Create a file named `.env` in the root directory of your project.

  - Paste the following lines, replacing placeholders with your actual values:

    ```
    DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
    CURRENCY_API_KEY=YOUR_CURRENCY_API_KEY (Optional)
    ```

**Running the Bot:**

1.  Open your terminal or command prompt and navigate to your project directory.

2.  Run the following command:

    ```bash
    python calcbot.py
    ```

This will start CalcBot and connect it to your Discord server.

**Using the Bot:**

All commands in CalcBot utilize the prefix `!`. Here's a breakdown of the available commands:

  * `!ping`: Checks the bot's latency.
  * `!math [expression]`: Solves a math expression or equation (e.g., `!math 2+2`, `!math x^2 + 3x = 5`).
  * `!plot [equation]`: Creates a plot of a mathematical function (e.g., `!plot y=sin(x)`).
  * `!convert [query]`: Performs unit or currency conversion (e.g., `!convert 10 cm to inches`, `!convert 10 USD to EUR`).
  * `!history`: Shows your recent math history.
  * `!setvar [name] [value]`: Sets a custom variable (e.g., `!setvar a 5`, `!math a + 3`).
  * `!help`: Displays a list of commands and their descriptions.

**Invite Link:**

Click the link below to invite CalcBot to your Discord server:

[Invite Bot](https://discord.com/oauth2/authorize?client_id=1088234408894550118&permissions=412317211712&integration_type=0&scope=bot+applications.commands)

**Permissions Required:**

  * **Add Reactions:** To react to user messages for confirmation.
  * **Send Messages:** To send calculation results and messages.
  * **Use External Emojis:** To use emojis for displaying plots and conversions.
  * **View Channel History:** To access user messages for commands like `/history`.
  * **Manage Messages:**  To delete user messages after successful calculations (optional).

**Contributing:**

Feel free to fork this repository and contribute improvements or additional features.

**License:**

This project is licensed under the MIT License.

```
```
