from ..bot import Bot
from . import Mock, patch


def test_user_handle():
    with patch('chatbotmaker.extended_user.ExtendedUser') as mock:
        instance = mock.return_value
        instance.mark_seen.return_value = None
        # Given
        messenger, dispatcher, database = Mock(), Mock(), Mock()
        bot = Bot({}, messenger, dispatcher, database)
        # When
        bot.user_handle('user_id', 'user_message')
        # Then
