import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import database as db

API_TOKEN = '8497987358:AAEK_boy0TrEu7mJ20qEGaWNAEU3R1mp1Wo'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db.init_db()

def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📱 Termux Akademi", callback_data="menu_termux"),
        InlineKeyboardButton("🐉 Kali Linux", callback_data="menu_kali"),
        InlineKeyboardButton("🛠️ Güvenlik Araçları", callback_data="menu_tools"),
        InlineKeyboardButton("🧠 Quiz & Puanım", callback_data="menu_profile")
    )
    return keyboard

def termux_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("1️⃣ Temel Kurulum & Güncelleme", callback_data="termux_1"),
        InlineKeyboardButton("2️⃣ Depolama İzinleri & Dosya Yönetimi", callback_data="termux_2"),
        InlineKeyboardButton("3️⃣ Paket Yönetimi (pkg / apt)", callback_data="termux_3"),
        InlineKeyboardButton("⬅️ Ana Menü", callback_data="main_menu")
    )
    return keyboard

def kali_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("1️⃣ Temel Terminal Komutları", callback_data="kali_1"),
        InlineKeyboardButton("2️⃣ Dosya İzinleri (chmod/chown)", callback_data="kali_2"),
        InlineKeyboardButton("3️⃣ Kullanıcı & Ağ Yönetimi", callback_data="kali_3"),
        InlineKeyboardButton("⬅️ Ana Menü", callback_data="main_menu")
    )
    return keyboard

def tools_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔍 Nmap (Ağ Taraması)", callback_data="tool_nmap"),
        InlineKeyboardButton("💉 SQLMap (SQLi Testi)", callback_data="tool_sqlmap"),
        InlineKeyboardButton("🔑 Hydra (Brute-Force)", callback_data="tool_hydra"),
        InlineKeyboardButton("🎯 Metasploit", callback_data="tool_msf"),
        InlineKeyboardButton("⬅️ Ana Menü", callback_data="main_menu")
    )
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    db.add_user(message.from_user.id, message.from_user.username)
    await message.reply(
        "🚀 **Siber Güvenlik & Terminal Eğitim Botuna Hoş Geldin!**\n\n"
        "Aşağıdaki menüleri kullanarak Kali Linux, Termux ve popüler güvenlik araçlarının komutlarını ve ne işe yaradıklarını öğrenebilirsin:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)

    if data == "main_menu":
        await bot.edit_message_text("🚀 **Ana Menü**", chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=main_menu(), parse_mode="Markdown")

    elif data == "menu_termux":
        await bot.edit_message_text("📱 **Termux Eğitim Modülleri**", chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=termux_menu(), parse_mode="Markdown")

    elif data == "menu_kali":
        await bot.edit_message_text("🐉 **Kali Linux Eğitim Modülleri**", chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=kali_menu(), parse_mode="Markdown")

    elif data == "menu_tools":
        await bot.edit_message_text("🛠️ **Siber Güvenlik & OSINT Araçları**", chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=tools_menu(), parse_mode="Markdown")

    elif data == "termux_1":
        text = (
            "📱 **Termux 101: Kurulum & Güncelleme**\n\n"
            "• `pkg update && pkg upgrade -y`\n"
            "👉 *Ne İşe Yarar:* Termux paket deposunu günceller ve kurulu yazılımları en son sürüme yükseltir.\n\n"
            "• `pkg install python git nano -y`\n"
            "👉 *Ne İşe Yarar:* Python dili, Git sürüm kontrolcüsü ve Nano metin düzenleyicisini tek komutla kurar."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Termux Menüsü", callback_data="menu_termux"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "kali_1":
        text = (
            "🐉 **Kali Linux: Temel Komutlar**\n\n"
            "• `pwd`\n👉 *Ne İşe Yarar:* Şu an hangi klasör içinde olduğunu gösterir.\n\n"
            "• `ls -la`\n👉 *Ne İşe Yarar:* Gizli dosyalar dahil tüm dosya ve klasörleri detaylıca listeler.\n\n"
            "• `cd /var/www/html`\n👉 *Ne İşe Yarar:* Belirtilen dizine/klasöre geçiş yapar."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Kali Menüsü", callback_data="menu_kali"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "tool_nmap":
        text = (
            "🔍 **Nmap (Network Mapper)**\n"
            "Ağ kuralama, port tarama ve sistem tespiti aracıdır.\n\n"
            "• `nmap -sV target.com`\n"
            "👉 *Ne İşe Yarar:* Hedef sunucudaki açık portları ve çalışan servislerin sürümlerini tespit eder.\n\n"
            "• `nmap -A 192.168.1.1`\n"
            "👉 *Ne İşe Yarar:* İşletim sistemi tespiti, versiyon tespiti ve script taramasını bir arada (Agressif) yapar."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Araçlar Menüsü", callback_data="menu_tools"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "tool_sqlmap":
        text = (
            "💉 **SQLMap**\n"
            "Web sitelerindeki SQL Injection zafiyetlerini otomatik tespit ve istismar eden araçtır.\n\n"
            "• `sqlmap -u \"http://site.com/page.php?id=1\" --dbs`\n"
            "👉 *Ne İşe Yarar:* Hedef URL'deki SQLi zafiyetini tarar ve mevcut veritabanı isimlerini çeker.\n\n"
            "• `sqlmap -u \"http://site.com/page.php?id=1\" -D db_name --tables`\n"
            "👉 *Ne İşe Yarar:* Belirtilen veritabanı içindeki tabloları listeler."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Araçlar Menüsü", callback_data="menu_tools"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "tool_hydra":
        text = (
            "🔑 **THC-Hydra**\n"
            "Çeşitli protokollere (SSH, FTP, HTTP vb.) karşı parola denemesi (Brute-Force) yapan araçtır.\n\n"
            "• `hydra -l admin -P passlist.txt ssh://192.168.1.50`\n"
            "👉 *Ne İşe Yarar:* 'admin' kullanıcı adı için kelime listesi (passlist.txt) kullanarak SSH servisine şifre kırma saldırısı dener."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Araçlar Menüsü", callback_data="menu_tools"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "tool_msf":
        text = (
            "🎯 **Metasploit Framework**\n"
            "Sızma testleri ve exploit geliştirmek için kullanılan en popüler framework'tür.\n\n"
            "• `msfconsole`\n"
            "👉 *Ne İşe Yarar:* Metasploit komut satırı arayüzünü başlatır.\n\n"
            "• `search vsftpd`\n"
            "👉 *Ne İşe Yarar:* Veritabanında belirtilen servise ait exploit'leri arar."
        )
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Araçlar Menüsü", callback_data="menu_tools"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "menu_profile":
        score = db.get_user_score(user_id)
        text = f"👤 **Kullanıcı Profili**\n\n🆔 Telegram ID: `{user_id}`\n🏆 Quiz Puanı: `{score}` Puan"
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Ana Menü", callback_data="main_menu"))
        await bot.edit_message_text(text, chat_id=user_id, message_id=callback_query.message.message_id, reply_markup=keyboard, parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
  
