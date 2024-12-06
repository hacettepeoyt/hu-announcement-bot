import logging

from . import utils
from .config import DB_STRING, DB_NAME, DEFAULT_LANGUAGE
from .mongo import DepartmentDatabase, UserDatabase, FeedbackDatabase
from .scraper import *

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

# Locale
TRANSLATION_UNIT = utils.create_translation_unit()
LOCALE_DEPARTMENT_MAP = utils.create_locale_department_unit()

# Database objects
DEPARTMENT_DB = DepartmentDatabase(DB_STRING, DB_NAME)
USER_DB = UserDatabase(DB_STRING, DB_NAME)
FEEDBACK_DB = FeedbackDatabase(DB_STRING, DB_NAME)

# Department initialization
AVAILABLE_DEPARTMENTS: list[BaseDepartment] = \
    [
        CS('hu-cs', 'https://cs.hacettepe.edu.tr'),
        SKSDB('hu-sksdb', 'https://sksdb.hacettepe.edu.tr/bidbnew/index.php'),
        IE('hu-ie', 'https://ie.hacettepe.edu.tr'),
        Mat('hu-mat', 'https://mat.hacettepe.edu.tr'),
        BBY('hu-bby', 'https://bby.hacettepe.edu.tr'),
        EE('hu-ee', 'https://ee.hacettepe.edu.tr'),
        Phys('hu-phys', 'http://phys.hacettepe.edu.tr'),
        Edebiyat('hu-edebiyat', 'https://edebiyat.hacettepe.edu.tr'),
        ABOfisi('hu-abofisi', 'https://abofisi.hacettepe.edu.tr'),
        BIDB('hu-bidb', 'https://bidb.hacettepe.edu.tr'),
        JeoMuh('hu-jeomuh', 'https://jeomuh.hacettepe.edu.tr'),
        Hidro('hu-hidro', 'https://hidro.hacettepe.edu.tr'),
        IDE('hu-ide', 'https://ide.hacettepe.edu.tr'),
        SporBilimleri('hu-sporbilimleri', 'https://sporbilimleri.hacettepe.edu.tr'),
        Iletisim('hu-iletisim', 'https://iletisim.hacettepe.edu.tr'),
        Library('hu-library', 'https://library.hacettepe.edu.tr'),
        BaseDepartment('hu-me', 'https://me.hacettepe.edu.tr'),
        BaseDepartment('hu-cheng', 'https://cheng.hacettepe.edu.tr'),
        BaseDepartment('hu-bilisim', 'https://bilisim.hacettepe.edu.tr'),
        BaseDepartment('hu-muhfak', 'https://muhfak.hacettepe.edu.tr'),
        BaseDepartment('hu-chem', 'https://chem.hacettepe.edu.tr'),
        BaseDepartment('hu-tomer', 'https://tomer.hacettepe.edu.tr'),
        BaseDepartment('hu-tip', 'https://tip.hacettepe.edu.tr'),
        BaseDepartment('hu-stat', 'https://stat.hacettepe.edu.tr/tr'),
        BaseDepartment('hu-ydyo', 'https://ydyo.hacettepe.edu.tr'),
        BaseDepartment('hu-oidb', 'https://oidb.hacettepe.edu.tr'),
        BaseDepartment('hu-hukukfakultesi', 'https://hukukfakultesi.hacettepe.edu.tr'),
        BaseDepartment('hu-dis', 'https://dis.hacettepe.edu.tr'),
        BaseDepartment('hu-adk', 'https://adk.hacettepe.edu.tr'),
        BaseDepartment('hu-iibf', 'https://iibf.hacettepe.edu.tr'),
        BaseDepartment('hu-sbky', 'https://sbky.hacettepe.edu.tr'),
        BaseDepartment('hu-eczacilik', 'https://eczacilik.hacettepe.edu.tr'),
        BaseDepartment('hu-ce', 'https://ce.hacettepe.edu.tr'),
        BaseDepartment('hu-cevre', 'https://cevre.hacettepe.edu.tr'),
        BaseDepartment('hu-psikoloji', 'https://psikoloji.hacettepe.edu.tr'),
        BaseDepartment('hu-egitim', 'https://egitim.hacettepe.edu.tr'),
        BaseDepartment('hu-ergoterapi', 'https://ergoterapi.hacettepe.edu.tr'),
        BaseDepartment('hu-geomatik', 'https://geomatik.hacettepe.edu.tr'),
        BaseDepartment('hu-food', 'https://food.hacettepe.edu.tr'),
        BaseDepartment('hu-maden', 'https://maden.hacettepe.edu.tr'),
        BaseDepartment('hu-nuke', 'https://nuke.hacettepe.edu.tr'),
        BaseDepartment('hu-ofmamat', 'https://ofmamat.hacettepe.edu.tr'),
        BaseDepartment('hu-imo', 'https://imo.hacettepe.edu.tr'),
        BaseDepartment('hu-bdb', 'https://bdb.hacettepe.edu.tr'),
        BaseDepartment('hu-hemsirelik', 'https://hemsirelik.hacettepe.edu.tr'),
        BaseDepartment('hu-eob', 'https://eob.hacettepe.edu.tr'),
        BaseDepartment('hu-shmyo', 'https://shmyo.hacettepe.edu.tr'),
        BaseDepartment('hu-sbmy', 'https://sbmy.hacettepe.edu.tr'),
        BaseDepartment('hu-baskentosbtbmyo', 'https://baskentosbtbmyo.hacettepe.edu.tr'),
        BaseDepartment('hu-secmeli', 'https://secmeli.hacettepe.edu.tr'),
        BaseDepartment('hu-sosyalbilimler', 'https://sosyalbilimler.hacettepe.edu.tr'),
        BaseDepartment('hu-pdr', 'https://pdr.hacettepe.edu.tr'),
        BaseDepartment('hu-ade', 'https://ade.hacettepe.edu.tr'),
        BaseDepartment('hu-ake', 'https://ake.hacettepe.edu.tr'),
        BaseDepartment('hu-eeb', 'https://eeb.hacettepe.edu.tr'),
        BaseDepartment('hu-maliye', 'https://maliye.hacettepe.edu.tr'),
        BaseDepartment('hu-history', 'https://history.hacettepe.edu.tr'),
        BaseDepartment('hu-psikolojikdanismabirimi', 'https://psikolojikdanismabirimi.hacettepe.edu.tr'),
        BaseDepartment('hu-biology', 'https://biology.hacettepe.edu.tr'),
        BaseDepartment('hu-ict', 'https://ict.hacettepe.edu.tr'),
        BaseDepartment('hu-idb', 'https://idb.hacettepe.edu.tr'),
        BaseDepartment('hu-mtb', 'https://mtb.hacettepe.edu.tr'),
        BaseDepartment('hu-arkeo', 'https://arkeo.hacettepe.edu.tr'),
        BaseDepartment('hu-antropoloji', 'https://antropoloji.hacettepe.edu.tr'),
        BaseDepartment('hu-gsf', 'https://gsf.hacettepe.edu.tr'),
        BaseDepartment('hu-grafik', 'https://grafik.hacettepe.edu.tr'),
        BaseDepartment('hu-heykel', 'https://heykel.hacettepe.edu.tr'),
        BaseDepartment('hu-resim', 'https://resim.hacettepe.edu.tr'),
        BaseDepartment('hu-seramikvecam', 'https://seramikvecam.hacettepe.edu.tr'),
        BaseDepartment('hu-snf', 'https://snf.hacettepe.edu.tr'),
        BaseDepartment('hu-egitimbilimlerienstitusu', 'https://egitimbilimlerienstitusu.hacettepe.edu.tr'),
        BaseDepartment('hu-okuloncesi', 'https://okuloncesi.hacettepe.edu.tr'),
        BaseDepartment('hu-elt', 'https://elt.hacettepe.edu.tr'),
    ]


def decode(text_id: str, language: str) -> str:
    translation = TRANSLATION_UNIT.get(language).get(text_id)

    if not translation:
        translation = TRANSLATION_UNIT.get(DEFAULT_LANGUAGE).get(text_id)

    return translation


def get_possible_deps(_list) -> list[str]:
    return [dep.id for dep in AVAILABLE_DEPARTMENTS if dep.id not in _list]
