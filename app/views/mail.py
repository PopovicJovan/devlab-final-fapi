from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi import Request
from datetime import datetime, timezone
from app.config import Settings
from app.models.user import User
settings = Settings()

class MailView:
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        TEMPLATE_FOLDER='./app/templates/email/'
    )

    @classmethod
    async def register_email(cls, user: User, request: Request):

        env = Environment(
            loader=FileSystemLoader(searchpath=cls.conf.TEMPLATE_FOLDER),
            autoescape=select_autoescape(['html', 'xml'])
        )

        dt = datetime.fromisoformat(str(datetime.now(timezone.utc)))
        formatted_date = dt.strftime("%d %B %Y, %I:%M %p")

        template = env.get_template('register.html')
        html = template.render(
            user=user,
            ip_address=request.client.host,
            time=formatted_date
        )

        message = MessageSchema(
            subject="fastapi",
            recipients=[user.email],
            body=html,
            subtype="html"
        )

        fm = FastMail(cls.conf)
        await fm.send_message(message)