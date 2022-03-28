import src.scraper.math as math
import src.scraper.sksdb as sksdb
import src.scraper.cs as cs
import src.scraper.ie as ie
import src.scraper.cheng as cheng
import src.scraper.bilisim as bilisim
import src.scraper.muhfac as muhfac
import src.scraper.me as me
import src.scraper.Standart as Standart


math_website = math.Math()
sksdb_website = sksdb.Sksdb()
me_website = me.MechanicalEngineering()
cs_website = cs.ComputerScience()
ie_website = ie.IndustrialEngineering()
cheng_website = cheng.ChemieEngineering()
bilisim_website = bilisim.Bilisim()
muhfac_website = muhfac.EngineeringFaculty()
chemie_website = Standart.StandartDepartment('Chemie', 'http://www.chem.hacettepe.edu.tr/')
tomer_website = Standart.StandartDepartment('TOMER', 'http://www.tomer.hacettepe.edu.tr/')
medicine_website = Standart.StandartDepartment('Medicine', 'http://www.tip.hacettepe.edu.tr/')
stat_website = Standart.StandartDepartment('Statistic', 'http://www.stat.hacettepe.edu.tr/tr')
ydyo_website = Standart.StandartDepartment('Foreign Languages School', 'http://www.ydyo.hacettepe.edu.tr/')
oidb_website = Standart.StandartDepartment('Student Affairs Office', 'http://www.oidb.hacettepe.edu.tr/')
law_website = Standart.StandartDepartment('Law', 'http://www.hukukfakultesi.hacettepe.edu.tr/')
dentistry_website = Standart.StandartDepartment('Dentistry', 'http://www.dis.hacettepe.edu.tr/')
konservatuvar_website = Standart.StandartDepartment('Ankara Devlet Konservatuvarı', 'http://adk.hacettepe.edu.tr/')

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
