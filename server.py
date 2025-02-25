import sys
from pathlib import Path
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import proofread as prf

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sample_text = '''
궁중보다는 주로 민간에서 쓰였던 것으로, 조선시대 천이 귀하던 시절에 옷이나 이불을 만들고 남은 자투리 천을 모아 붙여 물건을 싸거나 밥상을 덮는데 쓰였다.

대부분 비단이나 모시 등 쉽게 상하는 천연소재로 만들어져, 현존하는 조각보는 주로 조선 후기에 만들어진 것들이다.

독창적이고 고유한 한국적 디자인 소재로 평가받아, 조각보의 색상과 면구성 형태를 재가공하여 현대 복식이나 가구, 공예, 건축 등에 다양하게 응용되고 있다. 조각보에는 옛날 사람들의 생활모습과 헝겊자투리 하나도 아껴 다시 사용하였던 생활의 지혜가 담겨있다. 조각보는 크게 만들어 이불보나 문에 치는 발로 이용하였고, 멋을 내어 예단이나 혼수품을 싸는데 이용하기도 하였다. 일반사람들은 상보로 많이 썼다.
'''

@app.get("/")
def root():
    results = prf.main(sample_text, ' '.join([x[0] for x in prf.spell_rules + prf.spacing_rules]), type="text")
    return {"result": results}


@app.post('/spellcheck')
async def get_answer(request: Request):
    body = await request.json()
    text = body['text']
    results = prf.main(text, ' '.join([x[0] for x in prf.spell_rules + prf.spacing_rules]), type="text")
    return {
        'result' : results
    }
