import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.research import ResearchEngine
# from config.merge_config.config import MergeConfig
# from config.merge_config.data import parser_arguments, check_list

app = FastAPI(version="1.0.1", title="research engine",
              description="research engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO multiple worker starup execute once time


@app.on_event("startup")
async def startup():
    print("startup init")
    app.include_router(ResearchEngine().create())
    print('Session setup')


# @app.on_event("shutdown")
# async def shutdown():
#     print("shutdown")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8888,
                workers=1, log_level="info")
