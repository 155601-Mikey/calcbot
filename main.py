import discord
from discord.ext import commands
from discord import app_commands
import sympy as sp  # For solving equations
import math
import matplotlib.pyplot as plt
import os
import io
import requests
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Flask app for uptime monitoring
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

# Initialize the bot
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Global history and variables storage
math_history = []
custom_variables = {}

@client.event
async def on_ready():
    print(f"Bot is ready! Logged in as {client.user}")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Helper function to process and evaluate math expressions
def evaluate_expression(expression):
    global custom_variables

    # Replace common symbols for easier parsing
    expression = expression.replace('√', 'sqrt')  # Square root
    expression = expression.replace('π', 'pi')    # Pi
    expression = expression.replace('²', '**2')  # Squared

    # Include custom variables
    try:
        expression = sp.sympify(expression, locals=custom_variables)
    except Exception:
        return f"Invalid expression: `{expression}`"

    try:
        if "=" in expression:
            lhs, rhs = expression.split("=")
            lhs, rhs = sp.sympify(lhs), sp.sympify(rhs)
            solution = sp.solve(lhs - rhs)
            return f"Solution(s): {solution}"
        else:
            result = eval(expression, {"__builtins__": None}, {**math.__dict__, "pi": math.pi, "sqrt": math.sqrt})
            math_history.append(f"{expression} = {result}")
            return f"Result: {result}"
    except Exception as e:
        return f"Error solving `{expression}`: {e}"

# Ping Command
@client.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency: {round(client.latency * 1000)}ms")

# Math Command
@client.tree.command(name="math", description="Solve a math equation or expression.")
@app_commands.describe(expression="The math expression or equation to solve (e.g., 2+2, √4, π*2, x²+2=5).")
async def math_command(interaction: discord.Interaction, expression: str):
    result = evaluate_expression(expression)
    await interaction.response.send_message(result)

# Graph Plotting Command
@client.tree.command(name="plot", description="Plot a mathematical function.")
@app_commands.describe(equation="The function to plot (e.g., y=x**2).")
async def plot_command(interaction: discord.Interaction, equation: str):
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(equation, locals=custom_variables)
        f = sp.lambdify(x, expr, modules=["math"])
        
        # Generate the plot
        x_vals = range(-10, 11)
        y_vals = [f(x) for x in x_vals]
        plt.plot(x_vals, y_vals)
        plt.title(f"Plot of {equation}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()

        # Save plot to a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()

        # Send the plot as a file
        await interaction.response.send_message(file=discord.File(buffer, filename="plot.png"))
    except Exception as e:
        await interaction.response.send_message(f"Error plotting `{equation}`: {e}")

# Unit and Currency Conversion Command
@client.tree.command(name="convert", description="Convert units or currencies.")
@app_commands.describe(query="The conversion query (e.g., 10 cm to inches, USD to EUR).")
async def convert_command(interaction: discord.Interaction, query: str):
    try:
        if " to " in query:
            amount, target_unit = query.split(" to ")
            if amount.strip().isnumeric():  # Simple unit conversion
                result = sp.convert_to(sp.sympify(amount), target_unit)
                await interaction.response.send_message(f"{query} = {result}")
            else:  # Currency conversion
                amount_value, source_currency = amount.split()
                response = requests.get(f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{source_currency.upper()}")
                data = response.json()
                if response.status_code == 200 and target_unit.upper() in data["conversion_rates"]:
                    rate = data["conversion_rates"][target_unit.upper()]
                    converted = float(amount_value) * rate
                    await interaction.response.send_message(f"{query} = {converted:.2f} {target_unit.upper()}")
                else:
                    await interaction.response.send_message(f"Could not convert currency: `{query}`")
        else:
            await interaction.response.send_message("Invalid query format. Use 'amount unit to target_unit' or 'amount currency to target_currency'.")
    except Exception as e:
        await interaction.response.send_message(f"Error converting `{query}`: {e}")

# Math History Command
@client.tree.command(name="history", description="Show your recent math history.")
async def history_command(interaction: discord.Interaction):
    if math_history:
        history = "\n".join(math_history[-5:])
        await interaction.response.send_message(f"**Recent Math History:**\n{history}")
    else:
        await interaction.response.send_message("No math history found!")

# Custom Variables Command
@client.tree.command(name="setvar", description="Set a custom variable.")
@app_commands.describe(name="Variable name", value="Variable value.")
async def setvar_command(interaction: discord.Interaction, name: str, value: str):
    try:
        custom_variables[name] = sp.sympify(value)
        await interaction.response.send_message(f"Set `{name}` to `{value}` successfully!")
    except Exception as e:
        await interaction.response.send_message(f"Error setting variable `{name}`: {e}")

# Help Command
@client.tree.command(name="help", description="Get a list of commands.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="CalcBot Help",
        description="A powerful math and conversion bot. Below are the available commands:",
        color=0x00FF00
    )
    embed.add_field(name="/ping", value="Check if the bot is online.", inline=False)
    embed.add_field(name="/math [expression]", value="Solve math expressions or equations.", inline=False)
    embed.add_field(name="/plot [equation]", value="Plot a mathematical function.", inline=False)
    embed.add_field(name="/convert [query]", value="Convert units or currencies.", inline=False)
    embed.add_field(name="/history", value="View your recent math history.", inline=False)
    embed.add_field(name="/setvar [name] [value]", value="Define custom variables.", inline=False)
    embed.add_field(name="/help", value="Display this help message.", inline=False)
    embed.add_field(name="Links", value="[Website](https://calcbot.vercel.app) | [Source Code](https://github.com/155601-Mikey/calcbot) | [Issues](https://github.com/155601-Mikey/calcbot/issues)", inline=False)
    await interaction.response.send_message(embed=embed)

# Run the bot
if TOKEN is None or CURRENCY_API_KEY is None:
    print("Error: Missing environment variables for DISCORD_BOT_TOKEN or CURRENCY_API_KEY.")
else:
    client.run(TOKEN)
