import os
from dotenv import load_dotenv
load_dotenv()
from nucleos.atlas_nucleo import _chamar_ia, _SYSTEM_ATLAS
r = _chamar_ia('quem criou o tik tok', _SYSTEM_ATLAS)
print('Resultado:', r)
