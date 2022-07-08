from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from addict import Dict

import utils
import message_utils

app = FastAPI()
plugins = utils.init_plugins()


@app.get('/')
def index():
    return 'hello ding!'


@app.post('/ding')
async def ding(data: dict, timestamp: Optional[int] = Header(None), sign: Optional[str] = Header(None)):
    if not utils.verify_sign(timestamp, sign):
        raise HTTPException(status_code=401, detail='Unauthorized')

    data = Dict(data)
    message = data.text.content.strip().split(' ', 1)

    if len(message) != 2:
        return message_utils.make_text('您输入的命令不符合规范，eg:关键字 详细信息', at_user_ids=[data.senderStaffId])

    if message[0] not in plugins:
        return message_utils.make_text('当前关键字没有可执行的命令', at_user_ids=[data.senderStaffId])

    return plugins[message[0]].process(data)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8080, reload=True, debug=True)
