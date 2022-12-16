import xml.etree.ElementTree as ET

import glob
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Entity
from sqlalchemy.dialects.postgresql import insert

engine = create_engine("postgresql://user:hackme@localhost")
Session = sessionmaker(bind=engine)

def GetEntitiesFromXml(xml_file_path):
    xml_file = ET.parse(xml_file_path)
    entities = []
    entities_dict = dict()

    for entity in xml_file.findall('СвЮЛ'):
        entityAttrib = entity.attrib
        address = entity.find('СвАдресЮЛ')

        #собираем адрес
        if address.find('АдресРФ'):
            addressInfo = address.find('АдресРФ')
        else:
            addressInfo = address.find('СвАдрЮЛФИАС')

        addressAttribs = []
        if 'Индекс' in addressInfo.attrib:
            addressAttribs.append(addressInfo.attrib['Индекс'])

        for attr in addressInfo.iter():
            attrString = ' '.join(attr.attrib.values())
            if attr.tag in ('НаимРегион', ):
                addressAttribs.append(attr.text)
            if attr.tag in ('МуниципРайон', ):
                addressAttribs.append(attr.attrib['Наим'])
            if attr.tag not in ('СвАдрЮЛФИАС', 'АдресРФ', 'ГРНДата', 'ГРНДатаИспр', 'НаимРегион', 'МуниципРайон'):
                if len(attrString) > 0: addressAttribs.append(attrString)

        for attrKey, attrValue in addressInfo.attrib.items():
            if attrKey not in ('КодАдрКладр', 'Индекс', 'КодРегион', 'ИдНом'):
                addressAttribs.append(attrValue)

        #собираем сведения о руководителе
        # chiefInfo = entity.find('СведДолжнФЛ')
        # if chiefInfo:
        #     chiefNameInfo = chiefInfo.find('СвФЛ').attrib
        #     secondname = '' if 'Фамилия' not in chiefNameInfo else chiefNameInfo['Фамилия'] 
        #     firstname = '' if 'Имя' not in chiefNameInfo else chiefNameInfo['Имя'] 
        #     patronymic = '' if 'Отчество' not in chiefNameInfo else chiefNameInfo['Отчество'] 
        #     chiefNameString = secondname + ' ' + firstname + ' ' + patronymic
            
        
        nameInfo = entity.find('СвНаимЮЛ')
        shortNameInfo = nameInfo.find('СвНаимЮЛСокр')

        #собираем все поля
        name = nameInfo.attrib['НаимЮЛПолн']
        short_name = '' if not shortNameInfo else shortNameInfo.attrib['НаимСокр']
        inn = '' if 'ИНН' not in entityAttrib else entityAttrib['ИНН']
        ogrn = '' if 'ОГРН' not in entityAttrib else entityAttrib['ОГРН']
        kpp = '' if 'КПП' not in entityAttrib else entityAttrib['КПП']
        addressString = ', '.join(addressAttribs)
        reg_date = '' if 'ОГРН' not in entityAttrib else entityAttrib['ДатаОГРН']

        entities_dict[inn] = {
                # 'inn': inn,
                'ogrn': ogrn,
                'kpp': kpp,
                'name': name,
                'short_name': short_name,
                'address': addressString,
                'reg_date': reg_date
            }

    for inn, entity in entities_dict.items():
        entity['inn'] = inn
        entities.append(entity)

    return entities

def uploadFromXml(folder):
    files = glob.glob(os.path.join(folder, "*"))
    for file in files:
        print(file)
        entities = GetEntitiesFromXml(file)

        with Session() as session:
            #upsert
            stmt = insert(Entity).values(entities)

            stmt = stmt.on_conflict_do_update(
                index_elements=[Entity.inn],
                set_={
                    Entity.ogrn: stmt.excluded.ogrn, 
                    Entity.kpp: stmt.excluded.kpp, 
                    Entity.name: stmt.excluded.name, 
                    Entity.address: stmt.excluded.address
                }
            )

            session.execute(stmt)
            session.commit()


uploadFromXml('EGRUL_FULL_2022-01-01_1')
uploadFromXml('EGRUL_2022-09-21_10')

# GetEntitiesFromXml('EGRUL_FULL_2022-01-01_1\EGRUL_FULL_2022-01-01_761688.XML')

# with Session() as session:
#     q = session.query(Entity).all()
#     print(q)
#     session.commit()
