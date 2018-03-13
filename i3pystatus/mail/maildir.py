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
        def check_seen_flag(msgname):
            """
            Return false if (S)een flag set

            The code of this funciton was partialy extrated from
            Pythons Maildir and MaildirMessage classes. Which are not used
            because they cannot read the message flags without reading the entire message.
            """
            maildir_info = msgname.split(':')[-1]
            # This is a logical implication if maildir_info starts with '2,'
            # it must not contain S if it does not start with '2,' the rest of
            # its content does not matter because no flags are set
            return not maildir_info.startswith('2,') or 'S' not in maildir_info[2:]

        path_new = os.path.join(self.directory, "new")
        new_messages = len(os.listdir(path_new))

        path_cur = os.path.join(self.directory, "cur")
        unread_messages = len(list(filter(check_seen_flag, os.listdir(path_cur))))

        return new_messages + unread_messages


Backend = MaildirMail
