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
import src.scraper.ydyo as ydyo



math_website = math.Math()
sksdb_website = sksdb.Sksdb()
chemie_website = chemie.Chemie()
cs_website = cs.ComputerScience()
ie_website = ie.IndustrialEngineering()
tomer_website = tomer.Tomer()
medicine_website = medicine.Medicine()
stat_website = stat.Stat()
cheng_website = cheng.ChemieEngineering()
bilisim_website = bilisim.Bilisim()
muhfac_website = muhfac.EngineeringFaculty()
me_website = me.MechanicalEngineering()
ydyo_website = ydyo.ForeignLanguages()

availableDepartments = {
    'Computer Science': cs_website,
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Chemie': chemie_website,
    'Industrial Engineering': ie_website,
    'TOMER': tomer_website,
    'Medicine': medicine_website,
    'Statistic': stat_website,
    "Chemie Engineering": cheng_website,
    "Bilişim Enstitüsü": bilisim_website,
    "Engineering Faculty": muhfac_website,
    "Mechanical Engineering": me_website,
    "Foreign Languages School": ydyo_website
}
