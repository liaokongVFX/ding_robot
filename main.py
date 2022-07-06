from typing import Optional
from fastapi import FastAPI, Header, HTTPException

import utils

app = FastAPI()


@app.get('/')
def index():
    return 'hello ding!'


@app.post('/ding')
async def ding(data: dict, timestamp: Optional[int] = Header(None), sign: Optional[str] = Header(None)):
    if not utils.verify_sign(timestamp, sign):
        raise HTTPException(status_code=401, detail='Unauthorized')

    # todo: 主动发送通过webhook
    return {
        'at': {
            'atUserIds': [
                data['senderStaffId']
            ],
        },
        'text': {
            'content': f'您刚发送的消息是 {data["text"]["content"]}'
        },
        'msgtype': 'text'
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=8080, reload=True, debug=True)
