import discord
from discord.ext import commands
from discord import app_commands
import sympy as sp
import math
import random
import os
import requests
import logging
import ast
import re
from typing import Dict, Any
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MathBot')

# Flask app for uptime monitoring
app = Flask('')

@app.route('/')
def home():
    return "Math Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Start Flask in a separate thread
Thread(target=run_flask, daemon=True).start()

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

# Global constants
DEFAULT_THEME = 0x00FF00
MAX_HISTORY_LENGTH = 10
SUPPORTED_THEMES = {"green": 0x00FF00, "blue": 0x0000FF, "red": 0xFF0000}

# Improved calculation function with safer parsing
def safe_evaluate(expression: str) -> float:
    """
    Safely evaluate mathematical expressions using ast module
    Supports basic math operations and some mathematical functions
    """
    # Replace mathematical notation
    expression = expression.replace("√", "sqrt").replace("π", "pi") \
                           .replace("²", "**2").replace("³", "**3")
    
    # Allowed nodes and functions
    allowed_nodes = {
        ast.Num, ast.BinOp, ast.UnaryOp, 
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow
    }
    
    allowed_funcs = {
        'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 
        'tan': math.tan, 'log': math.log, 'exp': math.exp,
        'pi': math.pi, 'e': math.e
    }

    def is_safe(node):
        """Check if the AST node is safe"""
        return type(node) in allowed_nodes

    try:
        parsed = ast.parse(expression, mode='eval')
        
        # Validate AST
        for node in ast.walk(parsed):
            if not is_safe(node):
                raise ValueError("Unsafe expression")
        
        # Compile and evaluate
        compiled = compile(parsed, '<string>', 'eval')
        result = eval(compiled, {"__builtins__": {}}, allowed_funcs)
        
        return round(result, 10)  # Limit decimal precision
    
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return f"Error: {e}"

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

# User data storage (consider moving to a persistent database in production)
user_data: Dict[int, Dict[str, Any]] = {}

@client.event
async def on_ready():
    """Bot startup and command synchronization"""
    logger.info(f"Bot is ready! Logged in as {client.user}")
    try:
        synced = await client.tree.sync()
        logger.info(f"Synced {len(synced)} commands")
    except Exception as e:
        logger.error(f"Command sync error: {e}")

def update_user_history(user_id: int, calculation: str):
    """Update user's calculation history"""
    user_data.setdefault(user_id, {
        "history": [], 
        "theme": DEFAULT_THEME
    })
    
    # Maintain a max history length
    if len(user_data[user_id]["history"]) >= MAX_HISTORY_LENGTH:
        user_data[user_id]["history"].pop(0)
    
    user_data[user_id]["history"].append(calculation)

# Math Commands
@tree.command(name="calculate", description="Perform calculations safely")
@app_commands.describe(expression="Mathematical expression to calculate")
async def calculate_command(interaction: discord.Interaction, expression: str):
    """Safe calculator command"""
    try:
        result = safe_evaluate(expression)
        
        # Update user's history
        update_user_history(
            interaction.user.id, 
            f"{expression} = {result}"
        )
        
        await interaction.response.send_message(f"Result: `{result}`")
    except Exception as e:
        await interaction.response.send_message(f"Calculation error: {e}")

@tree.command(name="solve", description="Solve mathematical equations")
@app_commands.describe(equation="Equation to solve (e.g., x**2 + 5 = 10)")
async def solve_command(interaction: discord.Interaction, equation: str):
    """Equation solver using SymPy"""
    try:
        # Replace common mathematical notations
        equation = equation.replace("=", "-").replace("²", "**2")
        
        solutions = sp.solve(equation)
        
        if not solutions:
            await interaction.response.send_message("No solutions found.")
        else:
            formatted_solutions = ", ".join(str(sol) for sol in solutions)
            await interaction.response.send_message(f"Solutions: `{formatted_solutions}`")
    
    except Exception as e:
        await interaction.response.send_message(f"Equation solving error: {e}")

@tree.command(name="convert", description="Unit conversion")
@app_commands.describe(
    amount="Amount to convert", 
    from_unit="Original unit", 
    to_unit="Target unit"
)
async def convert_command(
    interaction: discord.Interaction, 
    amount: float, 
    from_unit: str, 
    to_unit: str
):
    """Robust unit conversion"""
    try:
        converted = sp.convert_to(amount * sp.Unit(from_unit), sp.Unit(to_unit))
        await interaction.response.send_message(
            f"{amount} {from_unit} = {converted:.4f} {to_unit}"
        )
    except sp.errors.UnitError:
        await interaction.response.send_message(
            f"Invalid units. Check '{from_unit}' and '{to_unit}'."
        )
    except Exception as e:
        await interaction.response.send_message(f"Conversion error: {e}")

@tree.command(name="history", description="View recent calculations")
async def history_command(interaction: discord.Interaction):
    """Display user's calculation history"""
    user_history = user_data.get(interaction.user.id, {}).get("history", [])
    
    if user_history:
        history_text = "\n".join(user_history[-5:])
        embed = discord.Embed(
            title="📊 Calculation History", 
            description=f"```\n{history_text}```", 
            color=DEFAULT_THEME
        )
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("No calculation history found.")

# Run the bot
def main():
    if not TOKEN:
        logger.error("No Discord bot token provided!")
        return
    
    try:
        client.run(TOKEN)
    except Exception as e:
        logger.error(f"Bot runtime error: {e}")

if __name__ == "__main__":
    main()
