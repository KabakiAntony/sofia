class EmailInfo:
    def __init__(self):
        self.__email_object = {}
        self.__email_subject = ""
        self.__customer_email = ""
        self.__transaction_id = ""
        self.__checkout_req_id = ""


    @property
    def checkout_req_id(self):
        return self.__checkout_req_id

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

    @checkout_req_id.setter
    def checkout_req_id(self, req_id):
        self.__checkout_req_id = req_id

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

