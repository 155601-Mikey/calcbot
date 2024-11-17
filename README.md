# CalcBot - A Discord Calculator Bot

This is a Discord bot that allows you to perform various mathematical tasks and conversions directly within your server.

**Features:**

* **Basic Calculations:** Solve simple and complex math expressions using the `/math` command. Supports basic arithmetic operations, exponentiation, radicals, pi (π), and more. 
* **Equation Solving:** Solve simple linear equations (e.g., `x+6=8`).
* **Function Plotting:**  Visualize mathematical functions using the `/plot` command. 
* **Unit & Currency Conversion:** Convert between different units and currencies with the `/convert` command.
* **Calculation History:** Access your recent calculations using the `/history` command.
* **Custom Variables:** Define and use custom variables with the `/setvar` command.
* **Help:** Get this help message with the `/help` command.

**Invite Link:**

Click the link below to invite the bot to your Discord server:

[Invite Bot](https://discord.com/oauth2/authorize?client_id=1088234408894550118&permissions=412317211712&integration_type=0&scope=bot+applications.commands)

**Permissions Required:**

* **Add Reactions:** To react to user messages for confirmation.
* **Send Messages:** To send calculation results and messages.
* **Use External Emojis:** To use emojis for displaying plots and conversions.
* **View Channel History:** To access user messages for commands like `/history`.
* **Manage Messages:**  To delete user messages after successful calculations (optional).

**Usage:**

Each command requires a prefix followed by the specific arguments:

* Prefix: `/` (forward slash)
* Arguments: Additional information needed for the command. 

For detailed information on each command and its syntax, refer to the **Commands** section below.

**Commands:**

| Command                | Description                                          | Examples                                         |
|------------------------|-----------------------------------------------------|-------------------------------------------------|
| `/ping`                 | Checks if the bot is online.                          | `/ping`                                         |
| `/math [expression]`     | Solves math expressions or equations.                 | `/math 2+2`, `/math x+6=8`, `/math √4`,           |
|                          |                                                    | `/math π*2`, `/math 3²`                          |
| `/plot [equation]`      | Plots a mathematical function.                       | `/plot y=x**2`                                 |
| `/convert [query]`      | Converts between units or currencies.                | `/convert 10 cm to inches`, `/convert USD to EUR` |
| `/history`              | View your recent math history.                        | `/history`                                         |
| `/setvar [name] [value]`  | Define custom variables for calculations.           | `/setvar a 5`, `/math a + 3`                      |
| `/help`                 | Get this help message.                               | `/help`                                         |

**Contributing:**

Feel free to fork this repository and contribute improvements or additional features.

**License:**

This project is licensed under the MIT License.  Refer to the LICENSE file for details.
