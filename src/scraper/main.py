import src.scraper.math as math
import src.scraper.sksdb as sksdb
import src.scraper.chemie as chemie
import src.scraper.cs as cs
import src.scraper.ie as ie
import src.scraper.tomer as tomer
import src.scraper.medicine as medicine
import src.scraper.stat as stat
import src.scraper.cheng as cheng
import src.scraper.bilisim as bilisim
import src.scraper.muhfac as muhfac
import src.scraper.me as me



math_website = math.Math()
sksdb_website = sksdb.Sksdb()
chemie_website = chemie.Chemie()
cs_website = cs.ComputerScience()
ie_website = ie.IndustrialEngineering()
tomer_website = tomer.Tomer()
medicine_website = medicine.Medicine()
stat_website = stat.Stat()
cheng_website = cheng.ChEng()
bilisim_website = bilisim.Bilisim
muhfac_website = muhfac.MuhFac()
me_website = me.ME()

departments = {
    'CS': cs_website,
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Chemie': chemie_website,
    'IE': ie_website,
    'TOMER': tomer_website,
    'Medicine': medicine_website,
    'Stat': stat_website,
    "ChEng": cheng_website,
    "Bilisim": bilisim_website,
    "MuhFac": muhfac_website,
    "ME": me_website
}
