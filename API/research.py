# from fastapi import APIRouter
from fastapi import File, UploadFile, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from AI_module.AI_module import Module
# from schemes.TPKC import User, UpdateUser, Rack, UpdateRack, ResponseCaches
# from app.module.TPKC_smb import TPKCSmb
import zipfile
import io
import os
from fastapi.responses import FileResponse, StreamingResponse
import jieba
import numpy as np


class ResearchEngine(Module):
    def __init__(self) -> None:
        self.temp = None
        Module.__init__(self)
        # self.current_path = os.getcwd()
        # self.data = self.get_data_json()
        # self.caches_data = self.get_caches_json()
        # self.config = config

    def create(self):
        router = APIRouter(
            prefix="/research",
            tags=["research"],
            dependencies=[]
        )

        # 01/05 OK
        @router.get('research/{key_word}')
        async def get_all_user(key_word: str):
            '''
            取得與關鍵字有關的文件
            return:: List[{"uuid":1, "user_name":"name1"}, {"uuid":2, "user_name":"name2"}]
            '''
            # 將使用者輸入依照關鍵字分段
            cut_text_list = list(jieba.cut_for_search(key_word))
            l = []
            score_list = []
            result = []

            for item in cut_text_list:
                if item not in self.keyword:
                    print(f"word not found in keyword {item}")
                    continue
            for word in self.keyword:
                if word in cut_text_list:
                    l.append(1)
                else:
                    l.append(0)
            l_np = np.array(l)

            for i in self.tfidf:
                s = 0.0
                score = l_np * i
                score = score.tolist()
                for j in score:
                    s = s + j
                score_list.append(s)
            zip_score = zip(self.document_path, score_list)
            score_dict = dict(zip_score)

            for i in sorted(score_dict.items(), key=lambda d: d[1], reverse=True):
                if i[1] > 0:
                    result.append(i)

            return result

        # 01/05 OK

        @router.get('research_response_file/{key_word}')
        async def get_all_user(key_word: str):
            '''
            取得與關鍵字有關的文件
            return:: List[{"uuid":1, "user_name":"name1"}, {"uuid":2, "user_name":"name2"}]
            '''
            # 將使用者輸入依照關鍵字分段
            cut_text_list = list(jieba.cut_for_search(key_word))
            l = []
            score_list = []
            result = []

            for item in cut_text_list:
                if item not in self.keyword:
                    print(f"word not found in keyword {item}")
                    continue
            for word in self.keyword:
                if word in cut_text_list:
                    l.append(1)
                else:
                    l.append(0)
            l_np = np.array(l)

            for i in self.tfidf:
                s = 0.0
                score = l_np * i
                score = score.tolist()
                for j in score:
                    s = s + j
                score_list.append(s)
            zip_score = zip(self.document_path, score_list)
            score_dict = dict(zip_score)

            for i in sorted(score_dict.items(), key=lambda d: d[1], reverse=True):
                if i[1] > 0:
                    result.append(f"data/{i[0].replace('.wrd', '.txt')}")

            return self.zipfiles(result)

        @router.post('/upload')
        async def get_all_user():
            '''
            上傳資料 重新建立權重檔案
            '''
            pass
        return router

    def zipfiles(self, filenames):
        # zip_subdir = "data/"
        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
            for fpath in filenames:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(fdir, fname)
                # Add file, at correct path
                temp_zip.write(fpath, zip_path)
        return StreamingResponse(
            iter([zip_io.getvalue()]),
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment; filename=result.zip"}
        )
