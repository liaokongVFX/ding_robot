from plugins.plugin_base import PluginBase
from message_utils import make_text


class TestPlugin(PluginBase):
    keyword = '测试'
    description = '这是一个测试程序'

    def process(self, data):
        print(data)

        return make_text('hello', at_user_ids=[data.senderStaffId])


def register():
    return [TestPlugin]
