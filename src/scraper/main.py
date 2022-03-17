import src.scraper.math as math
import src.scraper.sksdb as sksdb
import src.scraper.chemie as chemie
import src.scraper.cs as cs
import src.scraper.ie as ie
import src.scraper.tomer as tomer
import src.scraper.medicine as medicine
import src.scraper.stat as stat


math_website = math.Math()
sksdb_website = sksdb.Sksdb()
chemie_website = chemie.Chemie()
cs_website = cs.ComputerScience()
ie_website = ie.IndustrialEngineering()
tomer_website = tomer.Tomer()
medicine_website = medicine.Medicine()
stat_website = stat.Stat()

departments = {
    'CS': cs_website,
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Chemie': chemie_website,
    'IE': ie_website,
    'TOMER': tomer_website,
    'Medicine': medicine_website,
    'Stat': stat_website
}