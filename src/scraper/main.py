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
import src.scraper.oidb as oidb
import src.scraper.law as law
import src.scraper.dentistry as dentistry
import src.scraper.konservatuvar as konservatuvar


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
oidb_website = oidb.StudentAffairsOffice()
law_website = law.Law()
dentistry_website = dentistry.Dentistry()
konservatuvar_website = konservatuvar.Konservatuvar()

availableDepartments = {
    'Computer Science': cs_website,
    'Math': math_website,
    'SKSDB': sksdb_website,
    'Student Affairs Office': oidb_website,
    'Ankara Devlet Konservatuvarı': konservatuvar_website,
    'Chemie': chemie_website,
    'Industrial Engineering': ie_website,
    'TOMER': tomer_website,
    'Medicine': medicine_website,
    'Dentistry': dentistry_website,
    'Statistic': stat_website,
    'Chemie Engineering': cheng_website,
    'Bilişim Enstitüsü': bilisim_website,
    'Engineering Faculty': muhfac_website,
    'Mechanical Engineering': me_website,
    'Law': law_website,
    'Foreign Languages School': ydyo_website
}
