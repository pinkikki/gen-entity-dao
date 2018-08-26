# -*- coding: utf-8 -*-

from db.db_support import DbSupport
from utils.string_utils import StringUtils
from jinja2 import Environment, FileSystemLoader


def convert_from_sqlite_to_c(sqlite_type):
    if sqlite_type == "integer":
        ret = "int"
    elif sqlite_type == "text" or sqlite_type.find("varchar") > -1:
        ret = "string"
    elif sqlite_type == "boolean":
        ret = "bool"

    return ret


def create_entity(table_name, column_info_list):
    cls_name = StringUtils.to_camel(table_name) + "Entity"
    env = Environment(loader=FileSystemLoader('./template/', encoding='utf8'))
    tpl = env.get_template('entity.template')
    with open("./output/" + cls_name + '.cs', 'wt', encoding='utf-8') as fout:
        columns = []
        for column_info in column_info_list:
            columns.append(
                {'field': StringUtils.to_camel(column_info[0]), 'type': convert_from_sqlite_to_c(column_info[1])})
        out_text = tpl.render({'entity_cls': cls_name, 'columns': columns})
        fout.write(out_text)


def create_dao(table_name, column_info_list):
    dao_cls_name = StringUtils.to_camel(table_name) + "Dao"
    entity_cls_name = StringUtils.to_camel(table_name) + "Entity"
    env = Environment(loader=FileSystemLoader('./template/', encoding='utf8'))
    tpl = env.get_template('dao.template')
    with open("./output/" + dao_cls_name + '.cs', 'wt', encoding='utf-8') as fout:
        columns = []
        count = len(column_info_list)
        index = 0;
        for column_info in column_info_list:
            index += 1
            columns.append(
                {'name': column_info[0], 'field': StringUtils.to_camel(column_info[0]),
                 'type': convert_from_sqlite_to_c(column_info[1]), 'last_flg': index == count})

        out_text = tpl.render(
            {'entity_cls': entity_cls_name, 'dao_cls': dao_cls_name, 'table_name': table_name, 'columns': columns,
             'pk_name': column_info_list[0][0], 'pk_field': StringUtils.to_camel(columns[0]['name'], lower_flg=True)})
        fout.write(out_text)


def main():
    table_list = DbSupport.create_entity_list('../input/master.db')

    for table in table_list:
        if table[0] == "sqlite_sequence":
            continue
        column_info_list = list(table[1])
        create_entity(table[0], column_info_list)
        create_dao(table[0], column_info_list)


if __name__ == '__main__':
    main()
