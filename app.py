import os
import threading

import discord
from discord import app_commands
from flask import Flask, jsonify, render_template_string

# ===== CONFIGURACIÓN =====
DISCORD_TOKEN = os.getenv("MTU2NzAzNTYxMDEzNTI3MzU3Nw.GnONqv.Rj_B4yuoLnZfbxLua4EK_ikph1DHVcePCQZ6zY")
DISCORD_CLIENT_ID = os.getenv("1567035610135273577")
DISCORD_GUILD_ID = int(os.getenv("1559455132821753856", "0"))
PORT = int(os.getenv("PORT", "5000"))

if not DISCORD_TOKEN:
    raise ValueError("Falta DISCORD_TOKEN en Railway")
if not DISCORD_CLIENT_ID:
    raise ValueError("Falta DISCORD_CLIENT_ID en Railway")
if DISCORD_GUILD_ID == 0:
    raise ValueError("Falta DISCORD_GUILD_ID en Railway")

INVITE_URL = (
    "https://discord.com/oauth2/authorize"
    f"?client_id={DISCORD_CLIENT_ID}"
    "&permissions=8858438710"
    "&response_type=code"
    "&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorized"
    "&integration_type=0"
    "&scope=applications.commands+bot"
)

guild = discord.Object(id=DISCORD_GUILD_ID)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
web = Flask(__name__)

# ===== BOT =====
@client.event
async def on_ready():
    print(f"Bot conectado como: {client.user}")
    try:
        await tree.sync(guild=guild)
        print("Comandos sincronizados")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

@tree.command(name="ping", description="Comprueba si el bot responde", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! ✅")

@tree.command(name="hola", description="Saluda al usuario", guild=guild)
async def hola(interaction: discord.Interaction):
    await interaction.response.send_message(f"¡Hola, {interaction.user.mention}! 👋")

@tree.command(name="ayuda", description="Muestra los comandos disponibles", guild=guild)
async def ayuda(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Comandos disponibles:**\n"
        "`/ping` — Comprueba el bot\n"
        "`/hola` — Te saluda\n"
        "`/ayuda` — Muestra esta ayuda"
    )

# ===== WEB =====
@web.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Bressh.Bot</title>
      <style>
        :root {
          --bg1: #071620;
          --bg2: #0d2333;
          --cyan: #66e9ff;
          --cyan2: #bff8ff;
          --text: #ecfeff;
          --muted: #9cc4cf;
        }

        * { box-sizing: border-box; }
        body {
          margin: 0;
          min-height: 100vh;
          display: grid;
          place-items: center;
          background: linear-gradient(135deg, var(--bg1), var(--bg2));
          color: var(--text);
          font-family: Arial, sans-serif;
          padding: 24px;
        }
        .card {
          width: min(100%, 700px);
          background: rgba(9, 19, 28, 0.9);
          border: 1px solid rgba(102, 233, 255, 0.4);
          border-radius: 24px;
          text-align: center;
          padding: 36px 22px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        }
        .badge {
          display: inline-block;
          padding: 8px 14px;
          border-radius: 999px;
          background: rgba(102, 233, 255, 0.08);
          border: 1px solid rgba(102, 233, 255, 0.5);
          color: var(--cyan2);
          letter-spacing: 0.18em;
          text-transform: uppercase;
          font-size: 11px;
          font-weight: bold;
        }
        .icon {
          width: 100px;
          height: 100px;
          margin: 22px auto 18px;
          display: grid;
          place-items: center;
          border-radius: 28px;
          background: linear-gradient(135deg, #133b4d, #0c1821);
          border: 1px solid rgba(102, 233, 255, 0.7);
          font-size: 46px;
        }
        h1 {
          margin: 0;
          font-size: clamp(40px, 8vw, 68px);
          letter-spacing: -0.06em;
        }
        h1 span { color: var(--cyan); }
        .subtitle {
          margin-top: 12px;
          color: var(--cyan2);
          font-size: 12px;
          letter-spacing: 0.22em;
          text-transform: uppercase;
        }
        .desc {
          max-width: 560px;
          margin: 18px auto 0;
          color: var(--muted);
          font-size: 16px;
          line-height: 1.7;
        }
        .button {
          display: inline-block;
          margin-top: 28px;
          padding: 16px 26px;
          text-decoration: none;
          background: linear-gradient(90deg, #aaf8ff, #61ebff);
          color: #03151d;
          font-weight: 900;
          border-radius: 12px;
          letter-spacing: 0.05em;
          text-transform: uppercase;
        }
        .grid {
          margin-top: 34px;
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 16px;
        }
        .item {
          padding: 16px 12px;
          border: 1px solid rgba(102, 233, 255, 0.18);
          border-radius: 14px;
          background: rgba(2, 13, 20, 0.6);
        }
        .item strong { display: block; margin-bottom: 6px; }
        .item span { color: var(--muted); font-size: 12px; line-height: 1.5; }
        @media (max-width: 640px) {
          .grid { grid-template-columns: 1fr; }
        }
      </style>
    </head>
    <body>
      <div class="card">
        <div class="badge">Discord bot</div>
        <div class="icon" aria-hidden="true">🤖</div>
        <h1>Bressh<span>.</span>Bot</h1>
        <div class="subtitle">Tryhard mode activated</div>

        <p class="desc">
          Añade el bot a tu servidor de Discord para usar comandos y
          acompañar a tu comunidad con un acceso rápido y limpio.
        </p>

        <a class="button" href="{{ invite_url }}" target="_blank" rel="noopener noreferrer">
          Invitar a Discord
        </a>

        <div class="grid">
          <div class="item">
            <strong>Fácil</strong>
            <span>Elige tu servidor directamente en Discord.</span>
          </div>
          <div class="item">
            <strong>Rápido</strong>
            <span>Comandos slash listos para usar.</span>
          </div>
          <div class="item">
            <strong>Online</strong>
            <span>Activo en Railway con la web y el bot.</span>
          </div>
        </div>
      </div>
    </body>
    </html>
    """, invite_url=INVITE_URL)

@web.route("/api/health")
def health():
    return jsonify({
        "web": "ok",
        "bot_online": client.is_ready()
    })

# ===== ARRANQUE =====
def start_web():
    web.run(host="0.0.0.0", port=PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=start_web, daemon=True).start()
    print(f"Web disponible en http://0.0.0.0:{PORT}")
    client.run(DISCORD_TOKEN)
