from iqa.messaging.abstract.message import Header, Properties, ApplicationData, ApplicationProperties, Message


class TestMessage:
    def test_message(self):
        header = Header(durable=True, priority=0, ttl=10, first_acquirer='No', delivery_count=0)
        properties = Properties(message_id='389102as123', user_id='', )
        application_data = ApplicationData()
        application_properties = ApplicationProperties()
        message = Message(header, properties, application_data, application_properties)

    def test_message(self):
        message = Message()
        message.header.delivery_count = 0
        message.header.durable = True
        message.header.first_acquirer
        message.header.priority = 0
        message.header.ttl = 0
