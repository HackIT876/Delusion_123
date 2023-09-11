#Imports
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from model import search_video,hot_words,query
#App
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Test
@app.get('/')
def test():
	return 'Not the correct way to connect to API'

@app.post("/video")
#Function
async def image_result(request: Request):
    #Required parameters
    try:
        query=dict(await request.json())['query']
        link=dict(await request.json())['link']
        type=dict(await request.json())['type']
    except:
        return {"Error":"Please enter all the required parameters"}
    if len(query)==0 or len(link)==0 or len(type)==0:
        return {"Error":"Please enter all the required parameters"}
    else:
        try:
            timestamps={"times_in_sec":search_video(query,link,type)}
            return timestamps
        except:
            return {"Error":"Something went wrong"}
        
@app.post("/audio_time")
#Function
async def audio_results(request: Request):
    try:
        file=dict(await request.json())['file']
        q=dict(await request.json())['query']
    except:
        return {"Error":"Please enter all the required parameters"}
    if  len(file)==0 or len(q)==0:
        return {"Error":"Please enter all the required parameters"}
    else:
            timestamp={"timestamps":query(file,q)}
            return timestamp
@app.post("/audio")
#Function
async def hot_word(request: Request):
    try:
        link=dict(await request.json())['link']
        type=dict(await request.json())['type']
    except:
        return {"Error":"Please enter all the required parameters"}
    if  len(link)==0 or len(type)==0:
        return {"Error":"Please enter all the required parameters"}
    else:
            file,hot_word=hot_words(link,type)
            hot={"hot_words":hot_word,"file":file}
            # print(hot)
            return hot
        
if __name__ == "__main__":
    uvicorn.run("fastapi_code:app")