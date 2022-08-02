import scraper.math as math
import scraper.sksdb as sksdb
import scraper.cs as cs
import scraper.standart as standart

cs_website = cs.ComputerScience('hu-1', 'http://www.cs.hacettepe.edu.tr/')
math_website = math.Math('hu-2', 'http://www.mat.hacettepe.edu.tr/')
sksdb_website = sksdb.Sksdb('hu-3', 'http://www.sksdb.hacettepe.edu.tr/bidbnew/index.php')
me_website = standart.StandartDepartment('hu-4', 'http://www.me.hacettepe.edu.tr/')
cheng_website = standart.StandartDepartment('hu-5', 'http://www.cheng.hacettepe.edu.tr/')
bilisim_website = standart.StandartDepartment('hu-6', 'http://www.bilisim.hacettepe.edu.tr/')
engineering_website = standart.StandartDepartment('hu-7', 'http://www.muhfak.hacettepe.edu.tr/')
chemie_website = standart.StandartDepartment('hu-8', 'http://www.chem.hacettepe.edu.tr/')
tomer_website = standart.StandartDepartment('hu-9', 'http://www.tomer.hacettepe.edu.tr/')
medicine_website = standart.StandartDepartment('hu-10', 'http://www.tip.hacettepe.edu.tr/')
stat_website = standart.StandartDepartment('hu-11', 'http://www.stat.hacettepe.edu.tr/tr/')
ydyo_website = standart.StandartDepartment('hu-12', 'http://www.ydyo.hacettepe.edu.tr/')
oidb_website = standart.StandartDepartment('hu-13', 'http://www.oidb.hacettepe.edu.tr/')
law_website = standart.StandartDepartment('hu-14', 'http://www.hukukfakultesi.hacettepe.edu.tr/')
dentistry_website = standart.StandartDepartment('hu-15', 'http://www.dis.hacettepe.edu.tr/')
konservatuvar_website = standart.StandartDepartment('hu-16', 'http://adk.hacettepe.edu.tr/')
iibf_website = standart.StandartDepartment('hu-17', 'http://www.iibf.hacettepe.edu.tr/')
politics_website = standart.StandartDepartment('hu-18', 'http://www.sbky.hacettepe.edu.tr/')

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
    politics_website.name: politics_website
}

"""
for website in availableDepartments.values():
    print(f"Current website: {website.name}")
    news = website.get_announcements()

    document = {
        'department': website.name,
        'announcements': news
    }

    AnnouncementDatabase.insert_documents([document])
"""

"""
news = sksdb_website.get_announcements()
olds = AnnouncementDatabase.find_announcement('SKSDB')

document = {
    'department': sksdb_website.name,
    'announcements': news
}

AnnouncementDatabase.insert_documents([document])


def check_diff(olds, news):
    count = 0
    flag = False

    for new in news:
        if new not in olds:
            print("Here")
            flag = True
            print(f"#{count}New one:", new)

        count += 1

    if flag:
        print("Database updated!")
        AnnouncementDatabase.update_announcements('SKSDB', news)


check_diff(olds, news)
"""

"""
new_announcements = cs_website.get_announcements()
#new_announcements[0]['title'] = 'WOWOWOWOW'
document = {
    'department': cs_website.name,
    'announcements': new_announcements
}

old_announcements = AnnouncementDatabase.find_announcement('Computer Science')


def check_diff(olds, news):
    count = 0
    flag = False

    for new in news:
        if new not in olds:
            print("Here")
            flag = True
            print(f"#{count}New one:", new)

        count += 1

    if flag:
        print("Database updated!")
        AnnouncementDatabase.update_announcements('Computer Science', news)


check_diff(old_announcements, new_announcements)
"""
