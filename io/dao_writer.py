# -*- coding: utf-8 -*-

from db.db_support import DbSupport
from utils.string_utils import StringUtils


def convert_from_sqlite_to_c(sqlite_type):
    if sqlite_type == "INTEGER":
        ret = "int"
    elif sqlite_type == "TEXT" or sqlite_type.find("VARCHAR") > -1:
        ret = "string"
    elif sqlite_type == "BOOLEAN":
        ret = "bool"

    return ret


def get_field_type(sqlite_type):
    if sqlite_type == "INTEGER":
        ret = "GetIntValue"
    elif sqlite_type == "TEXT" or sqlite_type.find("VARCHAR") > -1:
        ret = "GetStringValue"
    elif sqlite_type == "BOOLEAN":
        ret = "GetBoolValue"

    return ret


def create_sentence(fout, column_info):
    column_type = convert_from_sqlite_to_c(column_info[1])
    if column_type == "int":
        write_with_line(fout, "".join(["            .Append(entity.", StringUtils.to_camel(column_info[0]), ")"]))
    elif column_type == "string":
        write_with_line(fout, "            .Append(\"'\")")
        write_with_line(fout, "".join(["            .Append(entity.", StringUtils.to_camel(column_info[0]), ")"]))
        write_with_line(fout, "            .Append(\"'\")")
    else:
        write_with_line(fout,
                        "".join(["            .Append(entity.", StringUtils.to_camel(column_info[0]), " ? 1 : 0)"]))


def create_select_all_sentence(fout, table_name, entity_cls_name):
    write_with_line(fout, "".join(["    public static List<", entity_cls_name, "> SelectAll()"]))
    write_with_line(fout, "    {")
    write_with_line(fout, "".join(
        ["        List<", entity_cls_name, "> entityList = new List<", entity_cls_name, ">();"]))
    write_with_line(fout, "        StringBuilder sb = new StringBuilder();")
    write_with_line(fout, "".join(["        sb.Append(\"SELECT * FROM ", table_name, ";\");"]))
    write_with_line(fout, "        DataTable dataTable = DbManager.ExecuteQuery(sb.ToString());")
    write_with_line(fout, "        dataTable.Rows.ForEach(r => entityList.Add(CreateEntity(r)));")
    write_with_line(fout, "        return entityList;")
    write_with_line(fout, "    }")
    write_with_line(fout, "")


def create_select_pk_sentence(fout, table_name, column_info_list, entity_cls_name):
    write_with_line(fout, "".join(["    public static ", entity_cls_name, " SelectByPrimaryKey(int id)"]))
    write_with_line(fout, "    {")
    write_with_line(fout, "        StringBuilder sb = new StringBuilder();")
    write_with_line(fout, "".join(
        ["        sb.Append(\"SELECT * FROM ", table_name, " WHERE ", column_info_list[0][0], " = \")"]))
    write_with_line(fout, "            .Append(id)")
    write_with_line(fout, "            .Append(\";\");")
    write_with_line(fout, "        DataTable dataTable = DbManager.ExecuteQuery(sb.ToString());")
    write_with_line(fout, "        return dataTable.Rows.Count == 0 ? null : CreateEntity(dataTable[0]);")
    write_with_line(fout, "    }")
    write_with_line(fout, "")


def create_insert_sentence(fout, table_name, column_info_list, entity_cls_name):
    write_with_line(fout, "".join(["    public static void Insert(", entity_cls_name, " entity)"]))
    write_with_line(fout, "    {")
    write_with_line(fout, "        StringBuilder sb = new StringBuilder();")
    write_with_line(fout, "".join(["        sb.Append(\"INSERT INTO ", table_name, " VALUES (\")"]))
    count = len(column_info_list)
    index = 0;
    for column_info in column_info_list:
        index += 1
        create_sentence(fout, column_info)
        if index == count:
            write_with_line(fout, "            .Append(\");\");")
        else:
            write_with_line(fout, "            .Append(\",\")")
    write_with_line(fout, "        DbManager.ExecuteNonQuery(sb.ToString());")
    write_with_line(fout, "    }")
    write_with_line(fout, "")


def create_entity_sentence(fout, column_info_list, entity_cls_name):
    write_with_line(fout, "    private static DummyEntity CreateEntity(DataRow row)")
    write_with_line(fout, "    {")
    write_with_line(fout, "".join(["        ", entity_cls_name, " entity = new ", entity_cls_name, "();"]))
    for column_info in column_info_list:
        write_with_line(fout, "".join(["        entity.", StringUtils.to_camel(column_info[0]), " = DaoSupport.",
                                       get_field_type(column_info[1]), "(row, \"", column_info[0], "\");"]))
    write_with_line(fout, "        return entity;")
    write_with_line(fout, "    }")


def create_update_sentence(fout, table_name, column_info_list, entity_cls_name):
    write_with_line(fout, "".join(["    public static void Update(", entity_cls_name, " entity)"]))
    write_with_line(fout, "    {")
    write_with_line(fout, "        StringBuilder sb = new StringBuilder();")
    write_with_line(fout, "".join(["        sb.Append(\"UPDATE ", table_name, " SET \""]))
    count = len(column_info_list)
    index = 0;
    for column_info in column_info_list:
        index += 1
        write_with_line(fout, "".join(["            .Append(\"", column_info[0], " = \")"]))
        create_sentence(fout, column_info)
        if index != count:
            write_with_line(fout, "            .Append(\",\")")
    write_with_line(fout, "            .Append(\" WHERE \")")
    write_with_line(fout, "".join(["            .Append(\"", column_info_list[0][0], "\")"]))
    write_with_line(fout, "            .Append(\"=\")")
    write_with_line(fout,
                    "".join(["            .Append(entity.", StringUtils.to_camel(column_info_list[0][0]), ")"]))
    write_with_line(fout, "            .Append(\";\");")
    write_with_line(fout, "        DbManager.ExecuteNonQuery(sb.ToString());")
    write_with_line(fout, "    }")
    write_with_line(fout, "")


def create_entity(table_name, column_info_list):
    cls_name = StringUtils.to_camel(table_name) + "Entity"
    with open("../output/" + cls_name + '.cs', 'wt') as fout:
        write_with_line(fout, "namespace script.common.entity")
        write_with_line(fout, "{")
        write_with_line(fout, "".join(["    public class ", cls_name, " {"]))
        for column_info in column_info_list:
            column_name = StringUtils.to_camel(column_info[0])
            type_name = convert_from_sqlite_to_c(column_info[1])
            write_with_line(fout, "".join(["        public ", type_name, " ", column_name, " { get; set; }"]))
        write_with_line(fout, "    }")
        write_with_line(fout, "}")


def create_dao(table_name, column_info_list):
    dao_cls_name = StringUtils.to_camel(table_name) + "Dao"
    entity_cls_name = StringUtils.to_camel(table_name) + "Entity"
    with open("../output/" + dao_cls_name + '.cs', 'wt') as fout:
        write_with_line(fout, "using System.Collections.Generic;")
        write_with_line(fout, "using System.Text;")
        write_with_line(fout, "using Plugins;")
        write_with_line(fout, "using script.common.entity;")
        write_with_line(fout, "using script.core.db;")
        write_with_line(fout, "")
        write_with_line(fout, "".join(["public static class ", dao_cls_name]))
        write_with_line(fout, "{")

        create_select_all_sentence(fout, table_name, entity_cls_name)
        create_select_pk_sentence(fout, table_name, column_info_list, entity_cls_name)
        create_insert_sentence(fout, table_name, column_info_list, entity_cls_name)
        create_update_sentence(fout, table_name, column_info_list, entity_cls_name)
        create_entity_sentence(fout, column_info_list, entity_cls_name)

        fout.write("}")


def write_with_line(fout, val):
    fout.write(val)
    fout.write("\n")


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
