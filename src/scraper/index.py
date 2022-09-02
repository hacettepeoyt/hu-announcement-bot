'''
        index module simply creates the objects and store them in a dictionary.
        That's what it does only.

        If you are a contributor, don't forget to read scraper/README.md
'''



from .math import Math
from .sksdb import Sksdb
from .cs import ComputerScience
from .standart import StandartDepartment
from .ie import IndustrialEngineering
from .literature import Literature
from .bby import InformationManagement


cs_website = ComputerScience('hu-1', 'http://www.cs.hacettepe.edu.tr/')
math_website = Math('hu-2', 'http://www.mat.hacettepe.edu.tr/')
sksdb_website = Sksdb('hu-3', 'http://www.sksdb.hacettepe.edu.tr/bidbnew/index.php')
me_website = StandartDepartment('hu-4', 'http://www.me.hacettepe.edu.tr/')
cheng_website = StandartDepartment('hu-5', 'http://www.cheng.hacettepe.edu.tr/')
bilisim_website = StandartDepartment('hu-6', 'http://www.bilisim.hacettepe.edu.tr/')
engineering_website = StandartDepartment('hu-7', 'http://www.muhfak.hacettepe.edu.tr/')
chemie_website = StandartDepartment('hu-8', 'http://www.chem.hacettepe.edu.tr/')
tomer_website = StandartDepartment('hu-9', 'http://www.tomer.hacettepe.edu.tr/')
medicine_website = StandartDepartment('hu-10', 'http://www.tip.hacettepe.edu.tr/')
stat_website = StandartDepartment('hu-11', 'http://www.stat.hacettepe.edu.tr/tr/')
ydyo_website = StandartDepartment('hu-12', 'http://www.ydyo.hacettepe.edu.tr/')
oidb_website = StandartDepartment('hu-13', 'http://www.oidb.hacettepe.edu.tr/')
law_website = StandartDepartment('hu-14', 'http://www.hukukfakultesi.hacettepe.edu.tr/')
dentistry_website = StandartDepartment('hu-15', 'http://www.dis.hacettepe.edu.tr/')
konservatuvar_website = StandartDepartment('hu-16', 'http://adk.hacettepe.edu.tr/')
iibf_website = StandartDepartment('hu-17', 'http://www.iibf.hacettepe.edu.tr/')
politics_website = StandartDepartment('hu-18', 'http://www.sbky.hacettepe.edu.tr/')
ie_website = IndustrialEngineering('hu-19', 'http://www.ie.hacettepe.edu.tr/')
pharmacy_website = StandartDepartment('hu-20', 'http://www.eczacilik.hacettepe.edu.tr/')
ce_website = StandartDepartment('hu-21', 'http://www.ce.hacettepe.edu.tr/')
cevre_website = StandartDepartment('hu-22', 'http://www.cevre.hacettepe.edu.tr/')
psychology_website = StandartDepartment('hu-23', 'http://www.psikoloji.hacettepe.edu.tr/')
edu_website = StandartDepartment('hu-24', 'http://www.egitim.hacettepe.edu.tr/')
literature_website = Literature('hu-25', 'http://www.edebiyat.hacettepe.edu.tr/')
bby_website = InformationManagement('hu-26', 'http://bby.hacettepe.edu.tr/')
ergo_website = StandartDepartment('hu-27', 'http://www.ergoterapi.hacettepe.edu.tr/')


availableDepartments = {
    cs_website.name: cs_website,
    math_website.name: math_website,
    sksdb_website.name: sksdb_website,
    oidb_website.name: oidb_website,
    konservatuvar_website.name: konservatuvar_website,
    chemie_website.name: chemie_website,
    tomer_website.name: tomer_website,
    medicine_website.name: medicine_website,
    dentistry_website.name: dentistry_website,
    stat_website.name: stat_website,
    cheng_website.name: cheng_website,
    bilisim_website.name: bilisim_website,
    engineering_website.name: engineering_website,
    me_website.name: me_website,
    law_website.name: law_website,
    ydyo_website.name: ydyo_website,
    iibf_website.name: iibf_website,
    politics_website.name: politics_website,
    ie_website.name: ie_website,
    pharmacy_website.name: pharmacy_website,
    ce_website.name: ce_website,
    cevre_website.name: cevre_website,
    psychology_website.name: psychology_website,
    edu_website.name: edu_website,
    literature_website.name: literature_website,
    bby_website.name: bby_website,
    ergo_website.name: ergo_website
}

