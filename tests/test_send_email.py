import os
from datetime import datetime
from support.test_config import test_config


def test_send_email(poms) -> None:
    email_subject = f"Test Email {datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    file_upload_path = os.path.abspath("test_data/attachment.txt")
    email_body = "Hi,\n\nthis is a test email.\n\nKind Regards\n\nJaroslav"    
    
    poms.login_page.open(test_config["BaseUrl"])
    poms.login_page.login_to_email(test_config["Username"], test_config["Password"])
    poms.home_page.send_email(
        test_config["RecipientEmail"], email_subject, email_body, file_upload_path)
    poms.home_page.check_that_email_was_sent(
        test_config["RecipientEmail"], email_subject)
    poms.gmail_client.check_that_email_was_received(
        test_config["UserEmail"], email_subject, 30)
    poms.home_page.log_out()
