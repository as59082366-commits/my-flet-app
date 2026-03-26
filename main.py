import flet as ft
import asyncio
from telethon import TelegramClient

# --- إعدادات أساسية (ممكن تسيبها كدة وتغيرها من الواجهة) ---
API_ID = '1234567'       # حط الـ API ID بتاعك هنا
API_HASH = 'abcdef12345' # حط الـ API HASH بتاعك هنا

async def main(page: ft.Page):
    page.title = "Saoud Telegram Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    client = None

    # --- عناصر الواجهة ---
    txt_api_id = ft.TextField(label="API ID", value=API_ID, border_color="blue")
    txt_api_hash = ft.TextField(label="API Hash", value=API_HASH, border_color="blue")
    txt_phone = ft.TextField(label="Phone Number (+20...)", border_color="blue")
    txt_code = ft.TextField(label="Verification Code", visible=False, border_color="green")
    
    status_label = ft.Text("برنامج سعود جاهز للعمل ✅", size=14, color="grey")
    
    # --- وظائف التليجرام ---
    async def start_telegram(e):
        nonlocal client
        try:
            # 1. إنشاء الكلاينت
            client = TelegramClient('saoud_session', txt_api_id.value, txt_api_hash.value)
            await client.connect()
            
            # 2. طلب كود التحقق
            if not await client.is_user_authorized():
                await client.send_code_request(txt_phone.value)
                txt_code.visible = True
                status_label.value = "تم إرسال الكود.. ادخله في الخانة الخضراء"
                status_label.color = "yellow"
                btn_login.text = "تأكيد الكود وتسجيل الدخول"
                btn_login.on_click = verify_code
            else:
                status_label.value = "أنت مسجل دخول بالفعل! جاري العمل..."
                status_label.color = "green"
            
            page.update()
        except Exception as ex:
            status_label.value = f"خطأ: {str(ex)}"
            status_label.color = "red"
            page.update()

    async def verify_code(e):
        try:
            await client.sign_in(txt_phone.value, txt_code.value)
            status_label.value = "تم تسجيل الدخول بنجاح يا سعود! 🎉"
            status_label.color = "green"
            # هنا تقدر تبعت رسالة لنفسك للتجربة
            await client.send_message('me', 'تم تشغيل برنامج سعود بنجاح من ملف EXE!')
            page.update()
        except Exception as ex:
            status_label.value = f"كود خطأ: {str(ex)}"
            status_label.color = "red"
            page.update()

    btn_login = ft.ElevatedButton(
        text="اتصال بحساب تليجرام",
        icon=ft.icons.TELEGRAM,
        on_click=start_telegram,
        style=ft.ButtonStyle(color="white", bgcolor="blue")
    )

    # --- بناء الصفحة ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon(name=ft.icons.SETTINGS_SUGGEST, size=50, color="blue"),
                ft.Text("Telegram Userbot v1.0", size=24, weight="bold"),
                ft.Divider(),
                txt_api_id,
                txt_api_hash,
                txt_phone,
                txt_code,
                ft.VerticalDivider(height=10),
                btn_login,
                status_label,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.BLACK12
        )
    )

# السطر ده هو اللي بيخليه يفتح كبرنامج ويندوز
if __name__ == "__main__":
    ft.app(target=main)
