import logging

import yagmail
from jinja2 import Template

from app.settings import settings

logger = logging.getLogger(__name__)


TEMPLATES = {
    "verify_account": settings.EMAIL_TEMPLATES_DIR / "verify-account.html",
}


def send_email(to: str, subject: str, contents: str, **kwargs):
    """Sends an email with the project defined SMTP settings."""
    # Using a context manager here ensures the SMTP connection is closed,
    # even if there is an exception.
    with yagmail.SMTP(
        user=settings.SMTP.USER,
        password=settings.SMTP.PASSWORD.get_secret_value(),
        host=settings.SMTP.HOST,
        port=settings.SMTP.PORT,
        smtp_starttls=settings.SMTP.TLS,
        smtp_ssl=settings.SMTP.SSL,
    ) as client:
        client.send(to=to, subject=subject, contents=contents, **kwargs)


def send_verify_account_email(to: str, first_name: str) -> True:
    template_path = TEMPLATES["verify_account"]
    with open(str(template_path)) as file:
        template_str = file.read()

    subject = f"{settings.PROJECT_NAME} - Verify Email"
    kwargs = {
        "project_name": settings.PROJECT_NAME,
        "first_name": first_name.title(),
        "link": settings.SERVER_HOST,
    }
    rendered_template = Template(template_str).render(kwargs)

    return send_email(to=to, subject=subject, contents=rendered_template)
