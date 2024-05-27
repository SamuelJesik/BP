import unittest
from temp_code_7 import EventProcessor, EmailEvent, SMSEvent

class TestEventProcessing(unittest.TestCase):

    def test_email_event(self):
        event = EmailEvent("user@example.com")
        processor = EventProcessor()
        self.assertEqual(processor.process_event(event), "Sending email to user@example.com")

    def test_sms_event(self):
        event = SMSEvent("1234567890")
        processor = EventProcessor()
        self.assertEqual(processor.process_event(event), "Sending SMS to 1234567890")

if __name__ == '__main__':
    unittest.main()
