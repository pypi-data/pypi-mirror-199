"""
Author : wanqiang.liu
Email: 919740574@qq.com
Date: 2022/10/17
Desc: Parser .dbc get all signal of id,name,dlc,Transmitter , when you get a log from customer
            you can input id, get the id form which channel.
"""

import codecs
import os
import re
import time
import pandas as pd
import xml.dom.minidom as minidom
# Typer
import typer
from rich import print
from rich.progress import track, Progress, SpinnerColumn, TextColumn

# 编译正则表达式模式，返回一个对象，可以吧常用的正则表达式编译成正则表达式对象，方便后续调用及提高效率
# re.compile(pattern,flags=0)
# pattern 指定编译时表达式字符串
# flags 编译标志位，用来修改正则表达式的匹配方式，支持re.L | re.M 同时匹配
# re.L (re.Local) 做本地化识别匹配
# re.M (re.Multiline) 多行匹配，影响^ , $
__regex_pattern__ = re.compile(
    r""" SG_ (?P<name>.*) : (?P<start_bit>[0-9]{1,3})\|(?P<length>[0-9]{1,3})@(?P<format>[0-1])(?P<type>[+-]) \((?P<factor>.*),(?P<offset>.*)\) \[(?P<min>.*)\|(?P<max>.*)\] "(?P<unit>.*)"(\s{1,2})(?P<rx_nodes>.*)""")


class CANDatabase:
    """
    Object to hold all CAN messages in a network as defined by the DBC file.
    """

    # Private Properties
    _name = ""
    _dbcPath = ""
    _comment = ""
    _messages = list()
    _txNodes = list()
    _extended = False
    _attributes = list()
    _iter_index = 0
    _version = ""

    def __init__(self, dbc_path):
        """
        Constructor for the CAN Database.

        Arguments:
         - dbcPath: The file path to .dbc file.
        """
        self._dbcPath = dbc_path

    def __iter__(self):
        """
        Defined to make the object iterable.
        """
        return self

    def __next__(self):
        """
        Get the next iterable in the CANMessage list.
        """
        if self._iter_index == len(self._messages):
            self._iter_index = 0
            raise StopIteration
        self._iter_index += 1
        return self._messages[self._iter_index - 1]

    def Load(self):
        """
        Opens the DBC file and parses its contents.
        """
        try:
            # <wanqiang.liu> add 'r', encoding='UTF-8' , solve UnicodeDecodeError: 'gbk' codec can't decode byte 0x89 in position 4168: illegal multibyte sequence
            file = open(self._dbcPath, 'r', encoding='UTF-8')
        except OSError:
            print("Invalid file path specified.")
            print(self._dbcPath)
            return

        building_message = False
        can_msg = None

        line_number = 0
        for line in file:
            line = line.rstrip('\n')
            line_number += 1  # keep track of the line number for error reporting
            # BU_: 网络节点类型对象
            if line.startswith("BU_ :"):
                self._parseTransmittingNodes(line)
            # VERSION
            # # <wanqiang.liu>  bug has been fixed. 2022/10/19
            elif line.startswith("VERSION"):
                self._parseVersions(line)
            # BO_ 消息类型的对象 | 代表一条消息的起始标识
            # <wanqiang.liu>  bug has been fixed. 2022/10/19
            elif line.startswith("BO_"):
                can_msg = self._parseMessageHeader(line.replace(':', '').replace('  ', ' '))
                building_message = True
            # SG_ 信号类型的对象 | 比较核心的是正则表达式去匹配规则
            # <wanqiang.liu>  bug has been fixed. 2022/10/19
            elif line.startswith(" SG_") and building_message:
                can_msg.AddSignal(self._parseSignalEntry(line))
            # EV_ 环境变量类型的对象
            elif line == "EV_":
                pass
            # 空,预示一个BO_结束,循环下一个BO_
            elif line == "":
                if building_message:
                    building_message = False
                    self._messages += [can_msg]
                    can_msg.UpdateSubscribers()
                    can_msg = None
            # VAL_ 值描述
            # <wanqiang.liu>  bug has been fixed. 2022/10/19
            elif line.startswith("VAL_"):
                # print(line)
                val_components = valueLineSplit(line)
                new_value_name = val_components[2]
                new_value_canID = int(val_components[1])  # class int(x,base=10) 如果设置16,那就把x按照16进制的数转换成10进制！！
                # Tuple: (Name, CAN ID, Item Pairs)
                new_value = (new_value_name, new_value_canID, list())
                # Get： KeyValuePairs
                pairs = val_components[3:]
                for i in range(0, len(pairs), 2):
                    try:
                        # add item value/name pairs to list in new_value tuple
                        item_value = int(pairs[i])
                        item_name = pairs[i + 1]
                        new_value[2].append((item_value, item_name))
                    except IndexError:
                        print("Invalid value: " + new_value_name +
                              ". Found on line " + str(line_number) + '.')
                        return None
                # print(new_value)
                for message in self._messages:
                    if message.CANID() == new_value[1]:
                        message.AddValue(new_value)
                        break
            # BA_DEF_ BO_ parse attributes  属性定义
            # <wanqiang.liu>  bug has been fixed. 2022/10/19
            elif line.startswith("BA_DEF_ BO_"):
                components = line.split(' ')
                # warning: indices are one higher than they appear to be because of double space in line
                attr_name = components[2].strip('"')
                attr_type = components[3]
                attr_min = components[4]
                # 可能会遇到Enum类型，长度不止5
                attr_max = components[len(components) - 1].rstrip(';')
                new_attr = (attr_name, attr_type, attr_min, attr_max)
                self._attributes.append(new_attr)
            # BA_DEF_DEF_ 属性默认值
            # BA_ 属性值,信号发送周期 | 信号默认值，起始值
            # <wanqiang.liu>  bug has been fixed. 2022/10/19
            elif line.startswith("BA_ "):
                components = line.split(' ')
                if len(components) < 4:
                    pass
                elif components[2] == "SG_":
                    attr_name = components[1].strip('"')
                    attr_msgID = int(components[3])
                    attr_sigName = components[4]
                    attr_val = components[5].rstrip(';')
                    new_attr = (attr_sigName, attr_name, attr_val)

                    for message in self._messages:
                        if message.CANID() == attr_msgID:
                            message.AddAttribute(new_attr)
                            break

                elif components[2] == "BO_":
                    if components[1].strip('"') == 'GenMsgCycleTime' or components[1].strip('"') == 'GenMsgDelayTime':
                        attr_name = components[1].strip('"')
                        attr_msgID = int(components[3])
                        attr_msgCycleTime = components[4].rstrip(';')
                        for message in self._messages:
                            if message.CANID() == attr_msgID:
                                message.AddMsgCycleTime(attr_msgCycleTime)
                                break

            # CM_ 注释
            # <wanqiang.liu>  bug has been fixed. 2022/10/19
            # 避免BUG类似以下情况,可根据实际情况继续添加条件
            # Node Comments
            # CM_ BU_ ETC "External Tester Connector";
            elif line.startswith("CM_") and not line.startswith("CM_ BU_"):
                # print("NO. ----------------------------------------------")
                # print("0. " + line)
                # print("NO. ----------------------------------------------")
                components = line.split(' ')
                if len(components) <= 2:
                    break
                # 遍历messages
                for message in self._messages:
                    # 获取ID,判断ID在不在库中
                    # print("1. " + str(message.CANID()) + "  " + str(int(components[2])))
                    if message.CANID() == int(components[2]):
                        # 遍历message中的Signal
                        for signal in message:
                            # 获取信号名,判断是否相等
                            # print("2. " + signal.Name() + "     " + components[3])
                            if signal.Name() == components[3]:
                                comment_str = ''
                                # 记录信号的Comment
                                for each in components[4:]:
                                    # 拆解的时候去掉了空格,那么备注还是需要加上空格
                                    comment_str += each + ' '
                                # print("3. " + comment_str)
                                signal.AddComment(comment_str)
                                break
                        break
        self._iter_index = 0
        return self

    def Name(self):
        """
        Gets the CAN Database's name.
        """
        return self._name

    def Messages(self):
        """
        Gets the list of CANMessage objects.
        """
        return self._messages

    def Attribute(self):
        """
        Gets the list of Attribute.
        """
        return self._attributes

    def _parseTransmittingNodes(self, line):
        """
        Takes a string and parses the name of transmitting nodes in the CAN bus
        from it.
        """
        items = line.split(' ')
        for item in items:
            if item == "BU_:":
                pass
            else:
                self._txNodes += [item]
        return

    # wanqiang.liu
    def _parseVersions(self, line):
        """
        Takes a string and parses the name of version
        """
        items = line.split(' ')
        for item in items:
            if item == "VERSION":
                pass
            else:
                self._version = item
        return

    def _parseMessageHeader(self, line):
        """
        Creates a signal-less CANMessage object from the header line.
        """
        items = line.split(' ')
        msg_id = int(items[1])
        msg_name = items[2]
        msg_dlc = int(items[3])
        msg_tx = items[4].rstrip('\n')

        return CANMessage(msg_id, msg_name, msg_dlc, msg_tx)

    def _parseSignalEntry(self, line):
        """
        Creates a CANSignal object from DBC file information.

        The Regex used is compiled once in order to save time for the numerous
        signals being parsed.
        """
        result = __regex_pattern__.match(line)

        name = result.group('name')
        start_bit = int(result.group('start_bit'))
        length = int(result.group('length'))
        sig_format = int(result.group('format'))
        sig_type = result.group('type')
        # int()不能将带有小数点的字符串转化为整数类型 int(float("0.0"))
        factor = float(result.group('factor'))  # int() 可能会导致出错
        offset = int(float(result.group('offset')))
        minimum = float(result.group('min'))  # int() 可能会导致出错
        maximum = float(result.group('max'))  # int() 可能会导致出错
        unit = result.group('unit')
        rx_nodes = result.group('rx_nodes').split(',')

        return CANSignal(name, sig_type, sig_format, start_bit, length, offset,
                         factor, minimum, maximum, unit, rx_nodes)


class CANMessage:
    """
    Contains information on a message's ID, length in bytes, transmitting node,
    and the signals it contains.
    """

    def __init__(self, msg_id, msg_name, msg_dlc, msg_tx):
        """
        Constructor.
        """
        self._canID = msg_id
        self._name = msg_name
        self._dlc = msg_dlc
        self._txNode = msg_tx
        self._cycleTime = ""
        self._idType = None
        self._comment = ""
        self._signals = list()
        self._attributes = list()
        self._iter_index = 0
        self._subscribers = list()

    def __iter__(self):
        """
        Defined to make the object iterable.
        """
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Defines the next CANSignal object to be returned in an iteration.
        """
        if self._iter_index == len(self._signals):
            self._iter_index = 0
            raise StopIteration
        self._iter_index += 1
        return self._signals[self._iter_index - 1]

    def AddSignal(self, signal):
        """
        Takes a CANSignal object and adds it to the list of signals.
        """
        self._signals += [signal]
        return self

    def Signals(self):
        """
        Gets the signals in a CANMessage object.
        """
        return self._signals

    def SetComment(self, comment_str):
        """
        Sets the Comment property for the CANMessage.
        """
        self._comment = comment_str

        return self

    def CANID(self):
        """
        Gets the message's CAN ID.
        """
        # self._canID = str(hex(eval(str(self._canID)))).upper()
        return self._canID

    def MsgCycleTime(self):
        """
        Gets the message's CAN ID of Cycle Time
        :return:
        """
        # Example : 10.000 -> 10
        return self._cycleTime[:self._cycleTime.rfind('.')]

    def AddValue(self, value_tuple):
        """
        Adds a enumerated value mapping to the appropriate signal.
        """
        for signal in self._signals:
            if signal.Name() == value_tuple[0]:
                signal.SetValues(value_tuple[2])
                break
        return self

    def AddMsgCycleTime(self, msg_cycle_time):
        """
        Adds a CycleTime to the message.
        :return:
        """
        self._cycleTime = msg_cycle_time
        return self

    def AddAttribute(self, attr_tuple):
        """
        Adds an attribute to the message.
        """
        for signal in self._signals:
            if signal.Name() == attr_tuple[0]:
                signal.SetAttrs(attr_tuple[1:])
                # self._attributes.append(attr_tuple)
        return self

    def Attributes(self):
        return self._attributes

    def Name(self):
        return self._name

    def TransmittingNode(self):
        return self._txNode

    def DLC(self):
        return self._dlc

    def UpdateSubscribers(self):
        """
        Iterates through signals in the message to note all of the receiving
        nodes subscribed to the message.
        """
        for signal in self:
            nodes = signal.RxNodes()
            for each in nodes:
                if each not in self._subscribers:
                    self._subscribers += [each]
        return self


class CANSignal:
    """
    Contains information describing a signal in a CAN message.
    """

    def __init__(self, name, sigtype, sigformat, startbit, length, offset, factor,
                 minVal, maxVal, unit, rx_nodes):
        """
        Constructor.
        """
        self._name = name
        self._type = sigtype
        self._format = sigformat
        self._startbit = startbit
        self._length = length
        self._offset = offset
        self._factor = factor
        self._minVal = minVal
        self._maxVal = maxVal
        self._units = unit
        self._values = list()
        self._comment = ""
        self._rx_nodes = rx_nodes
        self._attr = list()

    def __lt__(self, other):
        return self._startbit < other._startbit

    def Name(self):
        """
        Gets the name of the CANSignal.
        """
        return self._name

    def Startbit(self):
        return self._startbit

    def Length(self):
        """
        Gets the length of the CANSignal.
        :return:
        """
        return self._length

    def GetSigFormat(self):
        """
        Gets the Format of the CANSignal. 0 Motorola 1 Intel
        :return:
        """
        return self._format

    def SignType(self):
        """
        Gets the var type of the CANSignal. + uint - int
        :return:
        """
        return self._type

    def GetMinVal(self):
        """
        Gets the min value of the CANSignal.
        :return:
        """
        return self._minVal

    def GetMaxVal(self):
        """
        Gets the max value of the CANSignal.
        :return:
        """
        return self._maxVal

    def SetValues(self, values_lst):
        """
        Sets the enumerated value map for the signal's data.
        """
        self._values = values_lst
        return self

    def GetValues(self):
        """
        Gets the message's Value Table.
        """
        return self._values

    def SetAttrs(self, attr_lst):
        """
        Sets the enumerated value map for the signal's data.
        """
        self._attr.append(attr_lst)
        return self

    def GetAttrs(self):
        """
        Gets the message's Value Table.
        """
        return self._attr

    def AddComment(self, cm_str):
        self._comment = cm_str
        return self

    def ReadComment(self):
        return self._comment

    def GetFactor(self):
        return self._factor

    def GetOffset(self):
        return self._offset

    def GetUnit(self):
        return self._units

    def RxNodes(self):
        return self._rx_nodes


def valueLineSplit(line):
    """
    Custom split function for splitting up the components of a value line.

    Could not use normal String.split(' ') due to spaces in some of the value
    name strings.
    """
    components = list()
    part = ""
    in_quotes = False
    # to solve below bug
    # VAL_ 288 ADataRawSafeALat1Qf 0 "Qf1_DevOfDataUndefd" 1 "Qf1_DataTmpUndefdAndEvlnInProgs" 2 "Qf1_DevOfDataNotWithinRngAllwd" 3 "Qf1_DataCalcdWithDevDefd";
    # ['VAL_', '288', 'ADataRawSafeALat1Qf', '0', 'Qf1_DevOfDataUndefd', '1', 'Qf1_DataTmpUndefdAndEvlnInProgs', '2', 'Qf1_DevOfDataNotWithinRngAllwd', '3']
    # add:   or ch == ';'
    for ch in line:
        if (ch == ' ' or ch == ';') and not in_quotes:
            components.append(part)
            part = ""
        elif ch == '"' and not in_quotes:
            in_quotes = True
        elif ch == '"' and in_quotes:
            in_quotes = False
        else:
            part += ch
    return components


class CreateDBOfDBC:
    import sqlite3

    def __init__(self):
        self.__pd_setting__()

    @staticmethod
    def __pd_setting__(full_display: bool = True):
        if full_display:
            pd.set_option('display.width', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_colwidth', None)
            pd.set_option('display.max_info_rows', None)

    def create_db(self):
        # Sqlite
        # Connect db
        conn = self.sqlite3.connect('example/output/adc20_dbc.db')
        print('database open success!')
        # Create db
        c = conn.cursor()
        try:
            c.execute(
                '''CREATE TABLE ADC20_DBC(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        _canID INT NOT NULL,
                                        _canIDHex TEXT NOT NULL,
                                        _sigName TEXT NOT NULL,
                                        _dlc TEXT NOT NULL,
                                        _txNode TEXT(20),
                                        _msgCh TEXT);''')
            print('database table create success')
        except Exception as e:
            print(e)
        return conn

    def insert_db(self, conn, v_canID, v_canIDHex, v_sigName, v_dlc, v_txNode, v_msgCh):
        c = conn.cursor()
        # Insert db
        c.execute("INSERT INTO ADC20_DBC (_canID,_canIDHex,_sigName,_dlc,_txNode,_msgCh) \
                      VALUES(?,?,?,?,?,?)", (v_canID, v_canIDHex, v_sigName, v_dlc, v_txNode, v_msgCh))

    def select_db(self, conn):
        c = conn.cursor()
        cursor = c.execute("SELECT _canID,_canIDHex,_sigName,_dlc,_txNode,_msgCh from ADC20_DBC")
        for row in cursor:
            print(" _canID= ", row[0])
            print(" _canIDHex= ", row[1])
            print(" _sigName= ", row[2])
            print(" _txNode= ", row[3])
            print(" _txNode= ", row[4])
            print(" _msgCh= ", row[5], "\n")

    @staticmethod
    def update_db(conn):
        c = conn.cursor()
        c.execute("UPDATE ADC20_DBC set _canID=9999 where _canID=147")
        conn.commit()
        print("Total number of rows updated : ", conn.total_changes)

        cursor = conn.execute("SELECT _canID,_canIDHex,_sigName,_dlc,_txNode,_msgCh from ADC20_DBC")
        for row in cursor:
            print(" _canID= ", row[0])
            print(" _canIDHex= ", row[1])
            print(" _sigName= ", row[2])
            print(" _txNode= ", row[3])
            print(" _txNode= ", row[4])
            print(" _msgCh= ", row[5], "\n")

    @staticmethod
    def delete_db(conn):
        c = conn.cursor()
        c.execute("DELETE from ADC20_DBC where _msgCh='ChassisCAN1';")
        conn.commit()
        print("Total number of rows deleted : ", conn.total_changes)

        cursor = conn.execute("SELECT _canID,_canIDHex,_sigName,_dlc,_txNode,_msgCh from ADC20_DBC")
        for row in cursor:
            print(" _canID= ", row[0])
            print(" _canIDHex= ", row[1])
            print(" _sigName= ", row[2])
            print(" _txNode= ", row[3])
            print(" _txNode= ", row[4])
            print(" _msgCh= ", row[5], "\n")

    def delete_db_all(self):
        try:
            conn = self.sqlite3.connect('example/output/adc20_dbc.db')
            c = conn.cursor()
            try:
                c.execute("DROP table ADC20_DBC;")
                conn.commit()
                print("Total number of rows deleted : ", conn.total_changes)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    @staticmethod
    def close_db(conn):
        conn.commit()
        conn.close()

    def loading(self):
        # wanqiang.liu modified
        _can_msg_id = []
        _can_msg_name = []
        _can_msg_dlc = []
        _can_msg_tx_node = []
        _can_msg_channel = []
        fil_or_fld = 1
        if fil_or_fld == 1:
            file_db = "example/input/SDB22100_FX11_High_ChassisCAN1_220314.dbc"
            file_db = "example/input/SDB22100_FX11_High_SafetyCANFD2_220314.dbc"
            file_db = "example/input/SDB22100_FX11_High_PassiveSafetyCAN_220314.dbc"
            file_db = "example/input/SDB2010707_EX11_A2_PassiveSafetyCAN_220714.dbc"
            can_db = CANDatabase(file_db).Load()
            for message in can_db.Messages():
                # 将信息加入列表中 <wanqiang.liu>
                _can_msg_id.append(message.CANID())
                _can_msg_name.append(message.Name())
                _can_msg_dlc.append(message.DLC())
                _can_msg_tx_node.append(message.TransmittingNode())
                _can_msg_channel.append(can_db._version.strip('"'))
        else:
            self.delete_db_all()
            conn = self.create_db()
            folder = "./example/input/"
            for root, dirs, files in os.walk(folder):
                # root 表示当前正在访问的文件夹路径
                # dirs 表示该文件夹下的子路径名list
                # files 表示该文件夹下的文件list
                for file in files:
                    if file.endswith('.dbc'):
                        tmp_file = os.path.join(root, file)
                        can_db = CANDatabase(tmp_file).Load()
                    else:
                        continue
                    for message in can_db.Messages():
                        # 将信息加入列表中 <wanqiang.liu>
                        # _can_msg_id.append(message.CANID())
                        # _can_msg_name.append(message.Name())
                        # _can_msg_dlc.append(message.DLC())
                        # _can_msg_tx_node.append(message.TransmittingNode())
                        # _can_msg_channel.append(can_db._version.strip('"'))
                        self.insert_db(conn=conn,
                                       v_canID=message.CANID(),
                                       v_canIDHex=str(hex(message.CANID())).upper()[2:],
                                       v_sigName=message.Name(),
                                       v_dlc=message.DLC(),
                                       v_txNode=message.TransmittingNode(),
                                       v_msgCh=can_db._version.strip('"'))
                self.close_db(conn=conn)
                for dir in dirs:
                    tmp_folder = os.path.join(root, dir)
        # 打印PD  <wanqiang.liu>
        message_pd = pd.DataFrame({'_canId': _can_msg_id,
                                   '_sigName': _can_msg_name,
                                   '_dlc': _can_msg_dlc,
                                   '_txNode': _can_msg_tx_node,
                                   '_msgCh': _can_msg_channel
                                   })
        # print(message_pd.sort_index(ascending=False))  # 降序排序
        # print(message_pd.sort_index(axis=1))  # 按索引和按列名排序
        print(message_pd.sort_values(by='_canId'))  # 按_canId列排序
        # print(message_pd.sort_values(by=['_canId', '_sigName']))  # 按_canId列排序,如果有相同的再按照_sigName列排序


class ReEditXvpVar:
    import xml
    from xml.dom import minidom
    import codecs

    def __init__(self, xvp_path, sysvar_namespace):
        self._xvp_path = xvp_path
        self._sysvar_namespace = sysvar_namespace
        self.reedit_signal2variable()

    @staticmethod
    def fixed_writexml(self, writer, indent="", add_indent="", new_line=""):
        writer.write(indent + "<" + self.tagName)
        attrs = self._get_attributes()
        a_names = attrs.keys()
        # a_names.sort()
        for a_name in a_names:
            writer.write(" %s=\"" % a_name)
            minidom._write_data(writer, attrs[a_name].value)
            writer.write("\"")
        if self.childNodes:
            if len(self.childNodes) == 1 \
                    and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
                writer.write(">")
                self.childNodes[0].writexml(writer, "", "", "")
                writer.write("</%s>%s" % (self.tagName, new_line))
                return
            writer.write(">%s" % new_line)
            for node in self.childNodes:
                if node.nodeType is not minidom.Node.TEXT_NODE:
                    node.writexml(writer, indent + add_indent, add_indent, new_line)
            writer.write("%s</%s>%s" % (indent, self.tagName, new_line))
        else:
            writer.write("/>%s" % new_line)

    def reedit_signal2variable(self):
        minidom.Element.writexml = self.fixed_writexml
        XVP_XML_ENTITY = self.xml.dom.minidom.parse(self._xvp_path)
        root = XVP_XML_ENTITY.documentElement
        # 获取从根节点数列表第3个Object，该值需要变更
        SymbolConfiguration = XVP_XML_ENTITY.getElementsByTagName("Object")[1]
        for item in SymbolConfiguration.getElementsByTagName("Object"):
            for element in item.getElementsByTagName("Property"):
                # 对展示的信号名SignalName更改，当前未更改
                if element.getAttribute("Name") == 'Text' or element.getAttribute("Name") == 'DescriptionText':
                    element.lastChild.data = str(element.lastChild.data)
                # 对Combo类控件添加节点<Property Name="UsedValueTable">PhysicalValue</Property>
                if element.getAttribute("Name") == 'Name':
                    if str(element.lastChild.data).find('ComboBoxControl') != -1:
                        valuetab_node = XVP_XML_ENTITY.createElement('Property')
                        text_node = XVP_XML_ENTITY.createTextNode('PhysicalValue')
                        valuetab_node.setAttribute('Name', "UsedValueTable")
                        valuetab_node.appendChild(text_node)
                        item.appendChild(valuetab_node)
                # 将Signal替换为系统变量
                if element.getAttribute("Name") == 'SymbolConfiguration':
                    # 判断是否已变更,2表示关联的是dbc信号，16表示系统变量
                    if str(element.lastChild.data).split(';')[1] == '2':
                        toSplitTemp = str(element.lastChild.data)
                        toSplitTemp = toSplitTemp.split(';')
                        toCombineTemp = toSplitTemp[0]
                        toCombineTemp += ';' + '16'
                        toCombineTemp += ';' + f'{self._sysvar_namespace}'
                        toCombineTemp += ';'
                        toCombineTemp += ';'
                        toCombineTemp += ';' + toSplitTemp[4] + '_' + toSplitTemp[5]
                        toCombineTemp += ';' + toSplitTemp[6]
                        toCombineTemp += ';'
                        toCombineTemp += ';'
                        toCombineTemp += ';' + toSplitTemp[9]
                        toCombineTemp += ';'
                        toCombineTemp += ';'
                        toCombineTemp += ';'
                        toCombineTemp += ';'
                        element.lastChild.data = toCombineTemp
        # 输出文件
        fh = codecs.open(self._xvp_path, 'w', 'UTF-8')
        XVP_XML_ENTITY.writexml(fh, addindent='  ', newl='\n', encoding='UTF-8')
        fh.close()

        print('---------------------------------------------------------------')
        print('Done! : File Output' + self._xvp_path)
        print('---------------------------------------------------------------')


def developmentDbc2Capl(dbc_path: str = r"example/input/SDB2010707_EX11_A2_PassiveSafetyCAN_220714.dbc"):
    """
    Opens a DBC file and parses it into a CANDatabase object and uses the
    information to generate a C header file for the Network Manager
    application.
    从DBC创建CAPL及SYSVAR
    """
    candb = CANDatabase(dbc_path)
    messages = candb.Load()
    # 打印属性
    attributes = messages.Attribute()
    for each in attributes:
        pass
    # 生成capl .can文件
    with open(f'{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}.can', 'w') as f:
        # 表头
        f.writelines('/*------------------------------------------------------------\n')
        f.writelines(f' * Author: wanqiang.liu \n')
        f.writelines(' * Description: This dbc_path mainly for Com send msg\n')
        f.writelines(' * Support: Email wanqiang.liu@freetech.com\n')
        f.writelines(f' * Source: {dbc_path}\n')
        f.writelines(f' * Date: {time.ctime()}\n')
        f.writelines('------------------------------------------------------------*/\n')
        f.writelines('/*@!Encoding:936*/\n')
        f.writelines('includes\n')
        f.writelines('{\n\n')
        f.writelines('}\n\n')
        # variables区域
        f.writelines('/*------------------------------------------------------------\n')
        f.writelines('Intro: define global variables, struct and etc. \n')
        f.writelines('@Param:   message         define message object\n')
        f.writelines('@Param:   msTimer         define message timer\n')
        f.writelines('@Param:   int cycleTime_  define message cycle time\n')
        f.writelines('@Param:   int txEnable_   define message tx or not\n')
        f.writelines('------------------------------------------------------------*/\n')
        f.writelines('variables\n')
        f.writelines('{\n')
        f.writelines(f'  /* Control whole messages Tx */\n')
        f.writelines(f'  int _TxEnable_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")} = 0; \n\n\n')
        f.writelines(f'  /* #define NUM */\n')
        f.writelines(f'  const int NUM_TxInit = 1;\n')
        f.writelines(f'  const int NUM_CntInit = 0;\n')
        f.writelines(f'  const int NUM_STEP1 = 500;\n')
        f.writelines(f'  const int NUM_STEP2 = 1000;\n')
        f.writelines(f'  const int NUM_ON = 1;\n')
        f.writelines(f'  const int NUM_OFF = 0;\n')
        f.writelines(f'  const int NUM_CntrLimit = 1;\n')
        f.writelines(f'  \n\n')
        for message in messages.Messages():
            f.writelines('  /* MsgID: 0x{:03X}'.format(message.CANID()) + f'  {message.Name()} */\n')
            f.writelines(f'  message {message.Name()} MSG_{message.Name()};\n')
            f.writelines(f'  msTimer msT_{message.Name()};\n')
            f.writelines(f'  int cycleTime_{message.Name()} = {message.MsgCycleTime()};\n')
            f.writelines(f'  int txEnable_{message.Name()}  = NUM_TxInit;   //0:TxStop, 1:Tx @sysvar, 2:Tx CycleChange, 3:Tx Cycle\n')
            f.writelines(f'  int cntCycle_{message.Name()}  = NUM_CntInit;  //use for cycle change message values\n')
            f.writelines(f'  int cntStep1_{message.Name()}  = NUM_STEP1;    //cntCycle_ <= Step1 send [value1]\n')
            f.writelines(f'  int cntStep2_{message.Name()}  = NUM_STEP2;    //Step1 < cntCycle_ <= Step2 send [value2]\n')
            f.writelines(f'  /*------ComGwUb or Monitor Signal-----------*/\n')
            f.writelines(f'  int BgnMonitorThisMsg_{message.Name()} = NUM_OFF;  /*control monitor msg on/off, default:off */\n')
            f.writelines(f'  int cntrLimit_{message.Name()} = NUM_CntrLimit;    /*control monitor of cntr to set sysvar to 1 */\n')
            for signal in message.Signals():
                f.writelines(f'  int cntr_{message.Name()}_{signal.Name()} = 0;\n')
            f.writelines('\n')
        f.writelines('}\n\n')
        # on start区域
        f.writelines('on start\n')
        f.writelines('{\n')
        f.writelines('  setEnableTx();\n')
        f.writelines('  initialize();\n')
        f.writelines('}\n\n')
        # Initialize区域
        f.writelines('Initialize()\n')
        f.writelines('{ \n')
        f.writelines('  /* SetTimer for all messages, you can use canceltimer(msT_xxx) */\n')
        for message in messages.Messages():
            f.writelines(f'  setTimer(msT_{message.Name()}, cycleTime_{message.Name()});\n')
        f.writelines('}\n\n')
        # setEnableTx区域
        f.writelines('setEnableTx()\n')
        f.writelines('{ \n')
        num_index = 0
        for message in messages.Messages():
            signals = message.Signals()
            sigRxNode = ''
            for signal in signals:
                sigRxNode = signal.RxNodes()[0]
            if sigRxNode != 'ASDM':
                f.writelines(f'  @DBCTx_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}::_Enable_01[{num_index}] = 0;/*{message.Name()}    TxNode:{message.TransmittingNode()}   RxNode:{sigRxNode}*/\n')
            else:
                f.writelines(f'  @DBCTx_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}::_Enable_01[{num_index}] = 1;/*{message.Name()}    TxNode:{message.TransmittingNode()}   RxNode:{sigRxNode}*/\n')
            num_index = num_index + 1
        f.writelines('}\n\n')
        # 逻辑主体区域
        num_index = 0
        for message in messages.Messages():
            f.writelines('/*-------------------------------------------------------------------------------------------------\n')
            f.writelines(f' * on timer {message.Name()}\n')
            signals = message.Signals()
            sigRxNode = ''
            for signal in signals:
                sigRxNode = signal.RxNodes()[0]
            f.writelines(f' * TxNode : {message.TransmittingNode()}     RxNode: {sigRxNode} \n')
            f.writelines(f' * Author : wanqiang.liu@freetech.com\n')
            f.writelines(f' * Date : {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}\n')
            f.writelines(f' * @Param: _TxEnable_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")} | control all messages tx or not\n')
            f.writelines(f' * @Param: @DBCTx::_Enable_01[{num_index}] | through sysvar control this messages tx or not\n')
            f.writelines(f' * @Param: txEnable_{message.Name()} | through global var control this messages tx or not\n')
            f.writelines(f' * @Param: cntCycle_{message.Name()} | control script values change cycle\n')
            f.writelines('-------------------------------------------------------------------------------------------------*/\n')
            f.writelines(f'on timer msT_{message.Name()}\n')
            f.writelines('{\n')
            f.writelines(f'  setTimer(msT_{message.Name()}, cycleTime_{message.Name()});\n')
            f.writelines(f'  if(_TxEnable_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")} || @DBCTx_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}::_Enable_01[{num_index}] == 1 )\n')
            num_index = num_index + 1
            f.writelines('  {\n')
            f.writelines('    /* (Panel) Through sysvar control message send */\n')
            # 逻辑主题系统变量控制区域1
            f.writelines(f'    if(txEnable_{message.Name()} == 1)\n')
            f.writelines('    {\n')
            signals = message.Signals()
            for signal in signals:
                tmp_startValue = 0
                for attr in signal.GetAttrs():
                    if attr[0] == 'GenSigStartValue':
                        tmp_startValue = attr[1]
                # signal.GetFactor()
                f.writelines(f'      /* StartBit: {signal.Startbit()}       Length: {signal.Length()}         Format: {signal.GetSigFormat()} (0 Motorola 1 Intel)   SignType: {signal.SignType()} (+ uint - int)\n')
                f.writelines(
                    f'       * Factor: {signal.GetFactor()}        Offset: {signal.GetOffset()}         PhysMinVal: {signal.GetMinVal()}      PhysMaxVal: {signal.GetMaxVal()}     (Can Bus Value)StartValue:{tmp_startValue}     Unit: {signal.GetUnit()}\n')
                f.writelines(f'       * ValuesTables: {signal.GetValues()}            \n')
                f.writelines(f'       * RxNode: {signal.RxNodes()}      Attr: {signal.GetAttrs()}           \n')
                f.writelines(f'       * Comment:    {signal.ReadComment()}   \n')
                f.writelines(f'       * Notes: (value * factor) + offset = phys_value           value = (phys_value - offset)/factor */   \n')
                f.writelines(f'      MSG_{message.Name()}.{signal.Name()} = (@sysvar::DBCTx_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}::{message.Name()}_{signal.Name()} - ({signal.GetOffset()}))/{signal.GetFactor()};\n\n')
            f.writelines(f'      output(MSG_{message.Name()});\n')
            f.writelines('    }\n')
            f.writelines('    /* (Script) Cycle change message value send */\n')
            # 逻辑主题 循环发送（变更值）区域2
            f.writelines(f'    else if(txEnable_{message.Name()} == 2)\n')
            f.writelines('    {\n')
            f.writelines(f'      cntCycle_{message.Name()}++;\n')
            f.writelines(f'      if(cntCycle_{message.Name()} <= cntStep1_{message.Name()})\n')
            f.writelines('      {\n')
            for signal in signals:
                f.writelines(f'        MSG_{message.Name()}.{signal.Name()} = 0;\n')
            f.writelines('      }\n')
            f.writelines(f'      else if(cntCycle_{message.Name()} <= cntStep2_{message.Name()})\n')
            f.writelines('      {\n')
            for signal in signals:
                f.writelines(f'        MSG_{message.Name()}.{signal.Name()} = 1;\n')
            f.writelines('      }\n')
            f.writelines('      else\n')
            f.writelines('      {\n')
            f.writelines(f'        cntCycle_{message.Name()} = 0;\n')
            f.writelines('      }\n\n')
            f.writelines(f'      output(MSG_{message.Name()});\n')
            f.writelines('    }\n')
            f.writelines('    /* (Send Const Value) message send const value */\n')
            # 逻辑主题 固定值发送区域3
            f.writelines(f'    else if(txEnable_{message.Name()} == 3)\n')
            f.writelines('    {\n')
            for signal in signals: f.writelines(f'      MSG_{message.Name()}.{signal.Name()} = 0;\n')
            f.writelines(f'      output(MSG_{message.Name()});\n')
            f.writelines('    }\n')
            f.writelines('    else\n')
            f.writelines('    {\n\n')
            f.writelines('    }\n')
            f.writelines('  }\n')
            f.writelines('}\n\n')
        # on message区域
        for message in messages.Messages():
            f.writelines('/*-------------------------------------------------------------------------------------------------\n')
            f.writelines(f' * Function: on message {message.Name()}\n')
            f.writelines(f' * Support: wanqiang.liu@freetech.com\n')
            f.writelines(f' * Description: Monitor Signal When Value equal xx last for n frame(set by cntrLimit_{message.Name()})\n')
            f.writelines('-------------------------------------------------------------------------------------------------*/\n')
            f.writelines(f'on message {message.Name()}\n')
            f.writelines('{\n')
            f.writelines(f'  if(BgnMonitorThisMsg_{message.Name()} == 1)\n')
            f.writelines('  {\n')
            for signal in message.Signals():
                f.writelines(f'    /* MonitorSignal_{signal.Name()} */\n')
                f.writelines(f'    if(this.{signal.Name()} == 0)\n')
                f.writelines('    {\n')
                f.writelines(f'      cntr_{message.Name()}_{signal.Name()}++;\n')
                f.writelines('    }\n')
                f.writelines(f'    else\n')
                f.writelines('    {\n')
                f.writelines(f'      cntr_{message.Name()}_{signal.Name()} = 0;\n')
                f.writelines('    }\n')
                f.writelines(f'    if(cntr_{message.Name()}_{signal.Name()} >= cntrLimit_{message.Name()})\n')
                f.writelines('    {\n')
                f.writelines(f'      @DBCUb_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}::{message.Name()}_{signal.Name()} = 1;\n')
                f.writelines('    }\n')
                f.writelines('    else\n')
                f.writelines('    {\n')
                f.writelines(f'      @DBCUb_{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}::{message.Name()}_{signal.Name()} = 0;\n')
                f.writelines('    }\n')
            f.writelines('  }\n')
            f.writelines('}\n\n\n')
        f.close()
    # 写系统变量xml *.vsysvar
    # -------------------------------------------------------------------------------------------------------------------------------------
    dom = minidom.getDOMImplementation().createDocument(None, 'systemvariables', None)
    root = dom.documentElement
    root.setAttribute('version', "4")
    # node 1
    node_1 = dom.createElement('namespace')
    node_1.setAttribute('name', "")
    node_1.setAttribute('comment', "_author: wanqiang.liu@freetech.com")
    node_1.setAttribute('interface', "")
    # 写入DBCTx
    # -------------------------------------------------------------------------------------------------------------------------------------
    # node 2
    node_2 = dom.createElement('namespace')
    node_2.setAttribute('name', f"DBCTx_{dbc_path[dbc_path.rfind('/') + 1:].replace('.dbc', '')}")
    node_2.setAttribute('comment', f'Src: {dbc_path[dbc_path.rfind("/") + 1:]}    Date: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}')
    node_2.setAttribute('interface', "")
    # node 3
    node_3 = dom.createElement('variable')
    sysvar_attr_val = {
        "anlyzLocal": "2",
        "readOnly": "false",
        "valueSequence": "false",
        "unit": "",
        "name": "_Enable_01",
        "comment": "",
        "bitcount": "32",
        "isSigned": "true",
        "encoding": "65001",
        "type": "intarray",
        "arrayLength": f"{num_index}",
        "startValue": ('0;' * num_index).rstrip(';'),
        "minValue": "0",
        "minValuePhys": "0",
        "maxValue": "1",
        "maxValuePhys": "1"}
    for attr in sysvar_attr_val:
        node_3.setAttribute(attr, sysvar_attr_val[attr])
    node_2.appendChild(node_3)
    # node 3
    for message in messages.Messages():
        signals = message.Signals()
        for signal in signals:
            node_3 = dom.createElement('variable')
            tmp_startValue = 0
            for attr in signal.GetAttrs():
                if attr[0] == 'GenSigStartValue':
                    tmp_startValue = attr[1]
            tmp_isSigned = 'true'
            if signal.SignType() == '+':
                # 解决物理值不是signed类型导致minval无法设置负值
                if int(float(signal.GetMinVal())) < 0:
                    tmp_isSigned = 'true'
                else:
                    tmp_isSigned = 'false'
            sysvar_attr_val = {
                "anlyzLocal": "2",
                "readOnly": "false",
                "valueSequence": "false",
                "unit": f"{signal.GetUnit()}",
                "name": f"{message.Name()}_{signal.Name()}",
                "comment": f"{signal.ReadComment()}",
                "bitcount": "32",
                "isSigned": tmp_isSigned,
                "encoding": "65001",
                "type": "int",
                # 信号值
                # "startValue": str(int(float(tmp_startValue))),
                # "minValue": f"{str(int(float(((signal.GetMinVal() - signal.GetOffset()) / signal.GetFactor()))))}",
                # "minValuePhys": f"{str(int(float(((signal.GetMinVal() - signal.GetOffset()) / signal.GetFactor()))))}",
                # "maxValue": f"{str(int(float(((signal.GetMaxVal() - signal.GetOffset()) / signal.GetFactor()))))}",
                # "maxValuePhys": f"{str(int(float(((signal.GetMaxVal() - signal.GetOffset()) / signal.GetFactor()))))}"}
                # 物理值
                "startValue": str(int(float((int(float(tmp_startValue) * signal.GetFactor()) + signal.GetOffset())))),
                "minValue": f"{str(int(float(((signal.GetMinVal() - signal.GetOffset()) / signal.GetFactor()))))}",
                "minValuePhys": f"{str(int(float(signal.GetMinVal())))}",
                "maxValue": f"{str(int(float(((signal.GetMaxVal() - signal.GetOffset()) / signal.GetFactor()))))}",
                "maxValuePhys": f"{str(int(float(signal.GetMaxVal())))}"}
            """
            精度值与偏移量：
            信号值 = （物理值-偏移量）/精度值  Example: (16 - (-40))/1 = 56(dec) = 0x38
            ((signal.GetMinVal() - signal.GetOffset())/signal.GetFactor())
            """
            for attr in sysvar_attr_val:
                node_3.setAttribute(attr, sysvar_attr_val[attr])
            # 如果存在ValueTable
            if len(signal.GetValues()) != 0:
                node_4 = dom.createElement('valuetable')
                node_4.setAttribute('name', f"{signal.Name()}")
                node_4.setAttribute('definesMinMax', "true")
                for value_item in signal.GetValues():
                    node_5 = dom.createElement('valuetableentry')
                    node_5.setAttribute('value', f"{value_item[0]}")
                    node_5.setAttribute('lowerBound', f"{value_item[0]}")
                    node_5.setAttribute('upperBound', f"{value_item[0]}")
                    node_5.setAttribute('description', f"{value_item[1]}")
                    node_5.setAttribute('displayString', f"{value_item[1]}")
                    node_4.appendChild(node_5)
                node_3.appendChild(node_4)
            node_2.appendChild(node_3)
    # 写入DBCUb
    # -------------------------------------------------------------------------------------------------------------------------------------
    # node 2_1
    node_2_1 = dom.createElement('namespace')
    node_2_1.setAttribute('name', f"DBCUb_{dbc_path[dbc_path.rfind('/') + 1:].replace('.dbc', '')}")
    node_2_1.setAttribute('comment', f'Src: {dbc_path[dbc_path.rfind("/") + 1:]}    Date: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}')
    node_2_1.setAttribute('interface', "")
    # node 3_1
    for message in messages.Messages():
        signals = message.Signals()
        for signal in signals:
            node_3_1 = dom.createElement('variable')
            sysvar_attr_val = {
                "anlyzLocal": "2",
                "readOnly": "false",
                "valueSequence": "false",
                "unit": "",
                "name": f"{message.Name()}_{signal.Name()}",
                "comment": "",
                "bitcount": "32",
                "isSigned": "true",
                "encoding": "65001",
                "type": "int",
                "startValue": "0",
                "minValue": "0",
                "minValuePhys": "0",
                "maxValue": "1",
                "maxValuePhys": "1"}
            for attr in sysvar_attr_val:
                node_3_1.setAttribute(attr, sysvar_attr_val[attr])
            node_2_1.appendChild(node_3_1)

    tmp_node = [
        (node_2, [node_3]),
        (node_1, [node_2, node_2_1]),
        (root, [node_1]),
    ]
    for item in tmp_node:
        for each in item[1]:
            item[0].appendChild(each)
    # 写文件
    fh = codecs.open(f'{dbc_path[dbc_path.rfind("/") + 1:].replace(".dbc", "")}.vsysvar', 'w', encoding='utf-8')
    dom.writexml(fh, addindent='\t', newl='\n', encoding='utf-8')
    fh.close()


def createDbOfDbc():
    entity = CreateDBOfDBC()
    entity.loading()


app = typer.Typer()


@app.command()
def dbc2capl(dbc_path: str = typer.Argument(..., help="the path of can dbc file path , ext with .dbc")):
    """
    帮助用户将dbc文件快速转换为capl发送脚本。

    :param dbc_path: 车载行业dbc文件输入

    :return: None
    """
    if os.path.isfile(dbc_path):
        if os.path.splitext(dbc_path)[-1] == '.dbc':
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description="Processing...", total=None)
                progress.add_task(description="Preparing...", total=None)
                developmentDbc2Capl(dbc_path)
                print(f'Done Generator at: [green]{os.path.dirname(dbc_path)}[/green]')
        else:
            print('[red]file format not in support list[/red]')


@app.command()
def rp_xvp(xvp_path: str = typer.Argument(..., help="the path of can xvp file path , ext with .xvp"),
           sysvar_namespace: str = typer.Argument(..., help="canoe sysvar namespace,link with sysvar")):
    """
    帮助用户快速将排版好的panel界面替换为sysvar,将panel与capl关联

    :param xvp_path: canoe12sp4以上panel可以快速排列发送信号

    :param sysvar_namespace: 该命名取值来自本工具生成dbc时候的脚本名称

    :return: None
    """
    if os.path.isfile(xvp_path):
        if os.path.splitext(xvp_path)[-1] == '.xvp':
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description="Processing...", total=None)
                progress.add_task(description="Preparing...", total=None)
                entity = ReEditXvpVar(xvp_path, sysvar_namespace)
        else:
            print('[red]file format not in support list[/red]')


if __name__ == "__main__":
    # createDbOfDbc()
    app()
