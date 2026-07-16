"""
Email Service
"""

import os

from flask_mail import Message

from app import mail


def send_report(

    to_email,

    subject,

    body,

    attachment=None

):

    msg = Message(

        subject=subject,

        recipients=[to_email]

    )

    msg.body = body

    if attachment is not None:

        with open(

            attachment,

            "rb"

        ) as f:

            msg.attach(

                os.path.basename(
                    attachment
                ),

                "application/pdf",

                f.read()

            )

    mail.send(msg)