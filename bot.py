import discord
from discord.ext import commands
from discord import app_commands

import os
import random
from dotenv import load_dotenv

from keep_alive import keep_alive

import psycopg2

import asyncio

from discord.ui import Button, View

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

NEW_YEAR = datetime(2025, 1, 1, 0, 0, 0)
scheduler = AsyncIOScheduler()
countdown_channel = None

load_dotenv()

keep_alive()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)
tree = bot.tree  

DATABASE_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_db_connection():
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        print("Database connected.")
        return connection
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_resolution(user_id, resolution):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("INSERT INTO resolutions (user_id, resolution) VALUES (%s, %s)", (user_id, resolution))
    connection.commit()
    cur.close()
    connection.close()

def read_resolution(user_id):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("SELECT resolution FROM resolutions WHERE user_id = %s", (user_id,))
    result = cur.fetchall()
    cur.close()
    connection.close()
    return result

def update_resolution(user_id, old_resolution, new_resolution):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("UPDATE resolutions SET resolution = %s WHERE user_id = %s AND resolution = %s", 
                (new_resolution, user_id, old_resolution))
    connection.commit()
    cur.close()
    connection.close()

def delete_resolution(user_id, resolution):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("DELETE FROM resolutions WHERE user_id = %s AND resolution = %s", 
                (user_id, resolution))
    connection.commit()
    cur.close()
    connection.close()


@bot.event
async def on_ready():
    print("-------------------------------------")
    print(f"Logged in as {bot.user}")
    print("-------------------------------------")
    await tree.sync()
    scheduler.add_job(update_countdown, "interval", seconds=60)
    scheduler.start()

def split_message(message, max_length=100):
    return [message[i:i + max_length] for i in range(0, len(message), max_length)]

@tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    display_name = interaction.user.display_name
    await interaction.response.send_message(f"Hello, {display_name}!")


@tree.command(name="ping", description="Test the bot's response time.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!!")


@tree.command(name="echo", description="Echo a message back to you.")
@app_commands.describe(message="The message to echo.")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f" Echoing, {message}")

@tree.command(name="wish", description="Send a personalized new year wish to the user.")
@app_commands.describe(message="Send a personalized new year greeting to the user.")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f" {message}")


@tree.command(name="greet", description="Send a personalized greeting to the user.")
async def greet(interaction: discord.Interaction):
    display_name = interaction.user.display_name
    current_time = datetime.now()
    current_hour = current_time.hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    await interaction.response.send_message(f"{greeting}, {display_name}!")


@tree.command(name="static-countdown", description="Show a static countdown timer to the New Year.")
async def staticcountdown(interaction: discord.Interaction):
    display_name = interaction.user.display_name
    greeting ="🎉✨ Wishing you an amazing 2025"
    greeting_message = "🥳✨🍀 May your year be filled with endless smiles, big dreams, and unforgettable moments! 🌟🎆🎊"
    now = datetime.now()
    if now >= NEW_YEAR:
        await interaction.response.send_message(f"{greeting}, {display_name}! {greeting_message}")
    else:
        delta = NEW_YEAR - now
        days, hours, minutes, seconds = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60, delta.seconds % 60
        countdown_message = (
            f"🎉 The New Year is almost here! 🌟\n"
            f"⏳ Only **{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds** to go! 🕒✨"
        )
        await interaction.response.send_message(countdown_message)  


@tree.command(name="automated-countdown", description="Show a automated countdown timer to the New Year.")
async def autocountdown(interaction: discord.Interaction):
    global countdown_channel
    countdown_channel = interaction.channel
    display_name = interaction.user.display_name
    greeting ="🎉✨ Wishing you an amazing 2025"
    greeting_message = "🥳✨🍀 May your year be filled with endless smiles, big dreams, and unforgettable moments! 🌟🎆🎊"
    now = datetime.now()
    if now >= NEW_YEAR:
        await interaction.response.send_message(f"{greeting}, {display_name}! {greeting_message}")
    else:
        delta = NEW_YEAR - now
        days, hours, minutes, seconds = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60, delta.seconds % 60
        countdown_message = (
            f"🎉 The New Year is almost here! 🌟\n"
            f"⏳ Only **{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds** to go! 🕒✨"
        )
        await interaction.response.send_message(countdown_message)


async def update_countdown():
    global countdown_channel
    if countdown_channel is None:
        print("Countdown channel not set. Skipping update.")
        return
    now = datetime.now()
    if now >= NEW_YEAR:
        await countdown_channel.send("🎊🌟 Wishing you an amazing 2025, Alvin! 🥳 May your year be filled with endless smiles, big dreams, and unforgettable moments! ✨🍀🎉")
        scheduler.shutdown()
    else:
        delta = NEW_YEAR - now
        days, hours, minutes, seconds = delta.days, delta.seconds // 3600, (delta.seconds // 60) % 60, delta.seconds % 60
        countdown_message = (
            f"🎉 The New Year is almost here! 🌟\n"
            f"⏳ Only **{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds** to go! 🕒✨"

        )
        await countdown_channel.send(countdown_message)

@tree.command(name="quotes", description="Gives out a motivational or festive message")
async def ask(interaction: discord.Interaction):
    motivation_button = Button(label="Motivational message", style=discord.ButtonStyle.primary, custom_id="motivation")
    festive_button = Button(label="Festive message", style=discord.ButtonStyle.primary, custom_id="festive")
    
    async def button_callback(interaction: discord.Interaction):
        motivation_messages = [
        "Believe in yourself! Every step forward is progress, and you're capable of achieving great things!",
        "Success doesn't come from what you do occasionally, it comes from what you do consistently.",
        "Don't wait for opportunities to come to you. Create your own success.",
        "Your potential is limitless. Keep pushing forward, and you'll see amazing results!",
        "The only limit to your success is the one you set for yourself. Keep going!",
        "Challenges are what make life interesting, and overcoming them is what makes life meaningful.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "Don't watch the clock; do what it does. Keep going.",
        "Hardships often prepare ordinary people for an extraordinary destiny.",
        "You are braver than you believe, stronger than you seem, and smarter than you think.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Dream big and dare to fail.",
        "It does not matter how slowly you go as long as you do not stop.",
        "The only way to do great work is to love what you do.",
        "Start where you are. Use what you have. Do what you can.",
        "Believe you can, and you're halfway there.",
        "The harder you work for something, the greater you’ll feel when you achieve it.",
        "Your only limit is your mind. Push it to go beyond.",
        "Stay positive, work hard, and make it happen.",
        "Great things never come from comfort zones. Keep striving!"
        ]

        festive_messages = [
        "Wishing you a bright and prosperous New Year! May it bring joy, health, and endless opportunities.",
        "Happy New Year! May this year be your best yet, filled with new adventures and cherished moments.",
        "As we step into the New Year, may your dreams take flight, and all your goals come true!",
        "Cheers to a fresh start and another chance to make your dreams a reality. Happy New Year!",
        "May the New Year bring you peace, love, and success in everything you do. Have an amazing year ahead!",
        "Here's to new beginnings, great achievements, and all the happiness you can imagine. Happy New Year!",
        "Out with the old, in with the new—may the coming year be filled with endless joy and positivity.",
        "Wishing you a year filled with blessings, laughter, and unforgettable memories. Happy New Year!",
        "May every day of the New Year bring you closer to your dreams and fill your life with happiness!",
        "As the calendar flips, may this New Year be the start of something extraordinary for you. Happy New Year!",
        "This New Year, embrace change, seek new horizons, and let your aspirations soar!",
        "May your New Year be as bright as the fireworks lighting up the sky—full of wonder and excitement!",
        "Celebrate endings, for they precede new beginnings. Wishing you a fantastic year ahead!",
        "In the New Year, may you find the strength to achieve everything your heart desires.",
        "Let the New Year inspire you to be your best self and reach new heights!",
        "With every sunrise comes a fresh chance to grow and shine. Here's to a wonderful New Year!",
        "May the New Year bring you countless reasons to smile and endless moments of joy.",
        "Step into the New Year with courage, determination, and a heart full of gratitude.",
        "This year, may you achieve all you’ve been working for and discover new passions along the way.",
        "As the New Year dawns, may it bring you closer to success and fill your heart with contentment."
        ]

        if interaction.data["custom_id"] == "motivation":
            message = random.choice(motivation_messages)
        elif interaction.data["custom_id"] == "festive":
            message = random.choice(festive_messages)

        await interaction.response.defer()
        try:
            for chunk in split_message(message):
                await interaction.followup.send(chunk)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")

    motivation_button.callback = button_callback
    festive_button.callback = button_callback

    view = View()
    view.add_item(motivation_button)
    view.add_item(festive_button)

    await interaction.response.send_message("Choose a type of quote:", view=view)


@tree.command(name="resolutions", description="Manage your New Year's resolutions")
async def resolutions(interaction: discord.Interaction):
    create_button = Button(label="Create a Resolution", style=discord.ButtonStyle.primary, custom_id="create_resolution")
    read_button = Button(label="Read Your Resolutions", style=discord.ButtonStyle.green, custom_id="read_resolutions")
    update_button = Button(label="Update a Resolution", style=discord.ButtonStyle.blurple, custom_id="update_resolution")
    delete_button = Button(label="Delete a Resolution", style=discord.ButtonStyle.danger, custom_id="delete_resolution")

    view = View()
    view.add_item(create_button)
    view.add_item(read_button)
    view.add_item(update_button)
    view.add_item(delete_button)

    async def create_resolution_callback(interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("What is your New Year's resolution?", ephemeral=True)
        try:
            response = await bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30.0)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond.", ephemeral=True)
            return
        create_resolution(str(interaction.user.id), response.content)
        await interaction.followup.send(f"Your resolution has been set to: {response.content}", ephemeral=True)

    async def read_resolutions_callback(interaction: discord.Interaction):
        resolutions = read_resolution(str(interaction.user.id))
        if resolutions:
            resolution_list = "\n".join([f"{i+1}. {res[0]}" for i, res in enumerate(resolutions)])
            await interaction.response.send_message(f"Your resolutions:\n{resolution_list}", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have any resolutions set yet.", ephemeral=True)

    async def update_resolution_callback(interaction: discord.Interaction):
        resolutions = read_resolution(str(interaction.user.id))
        if resolutions:
            resolution_list = "\n".join([f"{i+1}. {res[0]}" for i, res in enumerate(resolutions)])
            await interaction.response.send_message(f"Your current resolutions:\n{resolution_list}\nWhich resolution number would you like to update? (Enter the number)", ephemeral=True)
            try:
                response = await bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30.0)
                resolution_number = int(response.content.strip()) - 1
                if 0 <= resolution_number < len(resolutions):
                    old_resolution = resolutions[resolution_number][0]
                    await interaction.followup.send(f"Your current resolution is: {old_resolution}\nWhat would you like to update it to?", ephemeral=True)
                    new_response = await bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30.0)
                    new_resolution = new_response.content
                    update_resolution(str(interaction.user.id), old_resolution, new_resolution)
                    await interaction.followup.send(f"Your resolution has been updated to: {new_resolution}", ephemeral=True)
                else:
                    await interaction.followup.send("Invalid resolution number. Please enter a valid number.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("You took too long to respond.", ephemeral=True)
            except ValueError:
                await interaction.followup.send("Please enter a valid number.", ephemeral=True)
        else:
            await interaction.followup.send("You don't have any resolutions set yet. Use the 'Create a Resolution' button first.", ephemeral=True)

    async def delete_resolution_callback(interaction: discord.Interaction):
        resolutions = read_resolution(str(interaction.user.id))
        if resolutions:
            resolution_list = "\n".join([f"{i+1}. {res[0]}" for i, res in enumerate(resolutions)])
            await interaction.response.send_message(f"Your current resolutions:\n{resolution_list}\nWhich resolution number would you like to delete? (Enter the number)", ephemeral=True)
            try:
                response = await bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30.0)
                resolution_number = int(response.content.strip()) - 1
                if 0 <= resolution_number < len(resolutions):
                    resolution_to_delete = resolutions[resolution_number][0]
                    delete_resolution(str(interaction.user.id), resolution_to_delete)
                    await interaction.followup.send(f"Resolution '{resolution_to_delete}' has been deleted.", ephemeral=True)
                else:
                    await interaction.followup.send("Invalid resolution number. Please enter a valid number.", ephemeral=True)
            except asyncio.TimeoutError:
                await interaction.followup.send("You took too long to respond.", ephemeral=True)
            except ValueError:
                await interaction.followup.send("Please enter a valid number.", ephemeral=True)
        else:
            await interaction.followup.send("You don't have any resolutions set yet. Use the 'Create a Resolution' button first.", ephemeral=True)

    create_button.callback = create_resolution_callback
    read_button.callback = read_resolutions_callback
    update_button.callback = update_resolution_callback
    delete_button.callback = delete_resolution_callback

    await interaction.response.send_message("Choose an option to manage your New Year's resolutions:", view=view, ephemeral=True)

bot.run(DISCORD_BOT_TOKEN)
