import os
from i3pystatus.mail import Backend


class MaildirMail(Backend):
    """
    Checks for local mail in Maildir
    """

    settings = (
        "directory",
    )
    required = ("directory",)

    directory = ""

    def init(self):
        self.directory = os.path.expanduser(self.directory)

    @property
    def unread(self):
        path = os.path.join(self.directory, "new")
        return len(os.listdir(path))


Backend = MaildirMail
