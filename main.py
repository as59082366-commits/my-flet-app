import flet as ft
import json, os, asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

# --- إعدادات الـ API ---
API_ID = 34896368
API_HASH = '169aae4e70bd61dabbf33069a0b04e04'

async def main(page: ft.Page):
    page.title = "Telegram Manager Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    page.window_width = 450
    page.window_height = 800
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # العداد دلوقتي بيعد ملفات الـ json بس (اللي كملت بنجاح)
    def get_count():
        return len([f for f in os.listdir('.') if f.endswith('.json')])

    # --- عناصر الواجهة ---
    counter_val = ft.Text(value=str(get_count()), size=50, weight="bold", color="white")
    
    counter_card = ft.Container(
        content=ft.Column([
            ft.Text("☁️", size=40),
            counter_val,
            ft.Text("Active Sessions", color="white", size=14, opacity=0.8)
        ], horizontal_alignment="center"),
        bgcolor="#1E88E5", padding=20, border_radius=20, width=320,
        shadow=ft.BoxShadow(blur_radius=15, color="#1E88E5", spread_radius=-5)
    )

    phone_input = ft.TextField(label="Phone Number (+20...)", border_radius=15)
    otp_input = ft.TextField(label="OTP Code", visible=False, border_radius=15)
    password_input = ft.TextField(label="2FA Password", password=True, visible=False, border_radius=15)
    status_text = ft.Text("Status: Ready to work", color="grey", size=12)

    # دالة الإلغاء مع مسح الملف المؤقت
    async def reset_ui(e):
        phone = phone_input.value.strip()
        # لو كنسلت، بنمسح ملف الـ session اللي اتعمل بالخطأ
        if os.path.exists(f"{phone}.session"):
            try:
                if page.client: await page.client.disconnect()
                os.remove(f"{phone}.session")
            except: pass
            
        otp_input.visible = False
        password_input.visible = False
        btn_verify.visible = False
        btn_cancel.visible = False
        btn_send.visible = True
        status_text.value = "Status: Canceled & Cleaned"
        status_text.color = "grey"
        page.update()

    async def start_login(e):
        phone = phone_input.value.strip()
        if not phone:
            status_text.value = "Error: Enter phone number!"
            status_text.color = "red"
            page.update()
            return

        status_text.value = "Status: Connecting..."
        page.update()
        
        page.client = TelegramClient(phone, API_ID, API_HASH)
        await page.client.connect()
        
        try:
            await page.client.send_code_request(phone)
            otp_input.visible = True
            btn_send.visible = False
            btn_verify.visible = True
            btn_cancel.visible = True
            status_text.value = "Status: Code sent successfully"
            status_text.color = "blue"
        except Exception as ex:
            status_text.value = f"Error: {str(ex)}"
            status_text.color = "red"
        page.update()

    async def verify_login(e):
        try:
            if password_input.visible:
                await page.client.sign_in(password=password_input.value)
            else:
                await page.client.sign_in(phone_input.value, otp_input.value)
            
            # حفظ الـ JSON (ده اللي بيأكد إن الحساب "تحول" فعلاً)
            user_data = {"phone": phone_input.value, "api_id": API_ID, "api_hash": API_HASH}
            with open(f"{phone_input.value}.json", "w") as f:
                json.dump(user_data, f)
            
            counter_val.value = str(get_count())
            status_text.value = f"✅ Success: Account Converted!"
            status_text.color = "green"
            
            # إخفاء الأزرار والرجوع للبداية
            otp_input.visible = password_input.visible = btn_verify.visible = btn_cancel.visible = False
            btn_send.visible = True
            phone_input.value = ""
        except SessionPasswordNeededError:
            password_input.visible = True
            status_text.value = "Status: 2FA Required"
        except Exception as ex:
            status_text.value = f"Error: {str(ex)}"
            status_text.color = "red"
        page.update()

    btn_send = ft.ElevatedButton("SEND OTP CODE", width=320, height=50, on_click=start_login)
    btn_verify = ft.ElevatedButton("VERIFY & EXPORT", width=320, height=50, bgcolor="green", color="white", visible=False, on_click=verify_login)
    btn_cancel = ft.TextButton("❌ CANCEL", visible=False, on_click=reset_ui)

    page.add(
        ft.Text("Telegram Manager Pro", size=24, weight="bold"),
        ft.Divider(height=20, color="transparent"),
        counter_card,
        ft.Divider(height=20, color="transparent"),
        phone_input, otp_input, password_input,
        ft.Divider(height=10, color="transparent"),
        btn_send, btn_verify, btn_cancel,
        status_text
    )

ft.app(target=main)
