class EmailInfo:
    def __init__(self):
        self.__email_object = {}
        self.__email_subject = ""
        self.__customer_email = ""
        self.__transaction_id = ""
        self.__checkout_req_url = ""
        self.__admin_email_object = ""


    @property
    def admin_email_object(self):
        return self.__admin_email_object

    @property
    def checkout_req_url(self):
        return self.__checkout_req_url

    @property
    def email_object(self):
        return self.__email_object

    @property
    def email_subject(self):
        return self.__email_subject

    @property
    def customer_email(self):
        return self.__customer_email

    @property
    def transaction_id(self):
        return self.__transaction_id

    @checkout_req_url.setter
    def checkout_req_url(self, req_url):
        self.__checkout_req_url = req_url

    @email_object.setter
    def email_object(self, object):
        self.__email_object = object

    @email_subject.setter
    def email_subject(self, subject):
        self.__email_subject = subject

    @customer_email.setter
    def customer_email(self, email):
        self.__customer_email = email

    @transaction_id.setter
    def transaction_id(self, id):
        self.__transaction_id = id


    @admin_email_object.setter
    def admin_email_object(self, object):
        self.__admin_email_object = object

