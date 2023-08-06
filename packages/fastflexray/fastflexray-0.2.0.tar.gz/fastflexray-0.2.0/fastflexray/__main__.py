"""
Author : wanqiang.liu
Email: 919740574@qq.com
Date: 2023/01/30 - 2023/02/01
Desc: FIBEX3.1.0 XML FLEXRAY PARSER

Poetry UserManual
-----------------
poetry show -h >> Shows information about packages.
poetry install >> install pyproject.toml file all dependence
poetry show >> view project installed dependence
poetry show -t >> view project installed dependence as tree
poetry update >> update all lock version of dependence
poetry update typer >> update special package dependence
poetry remove typer >> uninstall special package
poetry env list >> list current project venv, --full-path can show abs path

config
>> windows %APPDATA%/pypoetry/config.toml
>> macos /Users/xxx/Library/Application Support/pypoetry

current support param:
poetry config <key> <value> --list --local --unset
----------------------
item                  description
----------------------------------------------------------------------------------
cache-dir             default value:
                                macox   ~/Library/Caches/pypoetry
                                windwos %APPDATA%/Local/pypoetry/Cache
                                Unix    ~/.cache/pypoetry
virtualenvs.create     default value: true
                       如果执行poetry install/poetry add时没有虚拟环境，就自动创建一个虚拟环境
                       设置为false的话，当虚拟环境不存在时，会将包安装到系统环境
virtualenvs.in-project default value: false， 设置为true的话，会在当前项目目录下创建虚拟环境
virtualenvs.path       虚拟环境的路径，默认路径{cache-dir}\virtualenvs
repositories.<name>    设置新的备用存储库，具体的参数待确定

poetry config certificates.PyPI.cert false
"""
import xml
from xml.dom import minidom
import time
import codecs

import typer
import os
from rich import print
from rich.progress import track, Progress, SpinnerColumn, TextColumn


class FRDatabase:
    """
    Object to hold all FIBEX 3.1.0 in a network as defined by the xml file.
    """
    # Private Properties
    _name = ""
    _xmlPath = ""
    _comment = ""
    _frame = list()
    _frameTriggerings = list()
    _pduSignals = list()
    _pdus = list()
    _signalsName = list()
    _ecuList = list()
    _ecuRxList = list()
    _ecuTxList = list()
    # FrCoding
    _regulation = list()
    _valueTable = list()
    _frCoding = list()

    _txNodes = list()
    _extended = False
    _attributes = list()
    _iter_index = 0
    _version = ""

    def __init__(self, xml_path):
        """
        Constructor for the CAN Database.
        Arguments:
         - xml_path: The file path to .xml file.
        """
        self._xmlPath = xml_path

    def __iter__(self):
        """
        Defined to make the object iterable.
        """
        return self

    def __next__(self):
        """
        Get the next iterable in the CANMessage list.
        """
        if self._iter_index == len(self._frame):
            self._iter_index = 0
            raise StopIteration
        self._iter_index += 1
        return self._frame[self._iter_index - 1]

    def frames(self):
        """
        Gets the list of CANMessage objects.
        """
        return self._frame

    def parser_processing_coding(self, node):
        processing_info = node.getElementsByTagName("fx:PROCESSING-INFORMATION")[0]
        unit_spic = processing_info.getElementsByTagName("ho:UNIT-SPEC")[0]
        codings = processing_info.getElementsByTagName("fx:CODINGS")[0]
        coding = codings.getElementsByTagName("fx:CODING")
        for item in coding:
            self._regulation = []
            self._valueTable = []
            coding_id = item.getAttribute('ID')
            coding_name = item.getElementsByTagName("ho:SHORT-NAME")[0].lastChild.data
            # <ho:CODED-TYPE>
            coded_type = item.getElementsByTagName("ho:CODED-TYPE")[0]
            # >> A_UINT8 A_INT16
            base_data_type = coded_type.getAttribute("ho:BASE-DATA-TYPE")
            # >> STANDARD-LENGTH-TYPE
            category = coded_type.getAttribute("CATEGORY")
            # >> UNSIGNED SIGNED
            encoding = coded_type.getAttribute("ENCODING")
            # >> 8 10 ...
            bit_length = coded_type.getElementsByTagName("ho:BIT-LENGTH")[0].lastChild.data
            # <ho:COMPU-METHODS>
            if len(item.getElementsByTagName("ho:COMPU-METHODS")) != 0:
                compu_methods = item.getElementsByTagName("ho:COMPU-METHODS")[0]
                compu_method = compu_methods.getElementsByTagName("ho:COMPU-METHOD")[0]
                # >> A31_1 A33_1
                compu_method_shortname = compu_method.getElementsByTagName("ho:SHORT-NAME")[0].lastChild.data
                # >> LINEAR TEXTTABLE IDENTICAL
                compu_method_category = compu_method.getElementsByTagName("ho:CATEGORY")[0].lastChild.data

                # >> Unit ID REF
                if len(compu_method.getElementsByTagName("ho:UNIT-REF")) != 0:
                    compu_method_unit_ref = compu_method.getElementsByTagName("ho:UNIT-REF")[0]
                    unit_ref_id = compu_method_unit_ref.getAttribute("ID-REF")
                else:
                    unit_ref_id = 'None'
                # 最小值|最大值
                if len(compu_method.getElementsByTagName("ho:PHYS-CONSTRS")) != 0:
                    compu_method_phy_constrs = compu_method.getElementsByTagName("ho:PHYS-CONSTRS")[0]
                    lower_limit = compu_method_phy_constrs.getElementsByTagName("ho:LOWER-LIMIT")[0].lastChild.data
                    upper_limit = compu_method_phy_constrs.getElementsByTagName("ho:UPPER-LIMIT")[0].lastChild.data
                else:
                    lower_limit = '0'
                    upper_limit = '1'
                # Regulation | ValueTable
                if len(compu_method.getElementsByTagName("ho:COMPU-INTERNAL-TO-PHYS")) != 0:
                    compu_method_compu_internal_to_phys = compu_method.getElementsByTagName("ho:COMPU-INTERNAL-TO-PHYS")[0]
                    compu_method_compu_scale = compu_method_compu_internal_to_phys.getElementsByTagName("ho:COMPU-SCALE")
                    tmp_min = list()
                    tmp_max = list()
                    for each in compu_method_compu_scale:
                        if compu_method_category == 'LINEAR' or compu_method_category == 'IDENTICAL':
                            compu_rational_coeffs = each.getElementsByTagName("ho:COMPU-RATIONAL-COEFFS")[0]
                            compu_numberator = compu_rational_coeffs.getElementsByTagName("ho:COMPU-NUMERATOR")[0]  # numerator分子
                            compu_numberator_1 = compu_numberator.getElementsByTagName("ho:V")[0].lastChild.data
                            compu_numberator_2 = compu_numberator.getElementsByTagName("ho:V")[1].lastChild.data
                            compu_denominator = compu_rational_coeffs.getElementsByTagName("ho:COMPU-DENOMINATOR")[0]  # denominator分母
                            compu_denominator_1 = compu_denominator.getElementsByTagName("ho:V")[0].lastChild.data
                            # 输出
                            self._regulation.append((compu_numberator_1, compu_numberator_2, compu_denominator_1))
                        elif compu_method_category == 'TEXTTABLE':
                            vt_lower_limit = each.getElementsByTagName("ho:LOWER-LIMIT")[0].lastChild.data
                            vt_upper_limit = each.getElementsByTagName("ho:UPPER-LIMIT")[0].lastChild.data
                            compu_const = each.getElementsByTagName("ho:COMPU-CONST")[0]
                            vt = compu_const.getElementsByTagName("ho:VT")[0].lastChild.data
                            # 输出
                            self._regulation = [('0.0', '1.0', '1.0')]  # 增加容错性所加,value table无需考虑
                            self._valueTable.append((vt, vt_lower_limit, vt_upper_limit))
                            tmp_min.append(float(vt_lower_limit))
                            tmp_max.append(float(vt_upper_limit))
                            lower_limit = min(tmp_min)
                            upper_limit = max(tmp_max)
            else:
                compu_method_shortname = 'None'
                compu_method_category = 'None'
                unit_ref_id = 'None'
                lower_limit = '0'
                upper_limit = '1'
                self._regulation = [('0.0', '1.0', '1.0')]
                self._valueTable = []
            fr_coding = FrCoding(coding_id, encoding, bit_length, compu_method_category, unit_ref_id, lower_limit, upper_limit, self._regulation, self._valueTable)
            self._frCoding += [fr_coding]
        return self._frCoding

    def parser_ecus(self, node):
        fx_elements = node.getElementsByTagName("fx:ELEMENTS")[0]
        fx_ecus = fx_elements.getElementsByTagName("fx:ECUS")[0]
        fx_ecu = fx_elements.getElementsByTagName("fx:ECU")
        for ecu in fx_ecu:
            ecu_id = ecu.getAttribute("ID")
            short_name = ecu.getElementsByTagName("ho:SHORT-NAME")[0].lastChild.data
            connectors = ecu.getElementsByTagName("fx:CONNECTORS")[0]
            connector = connectors.getElementsByTagName("fx:CONNECTOR")[0]
            channel_ref = connector.getElementsByTagName("fx:CHANNEL-REF")[0]
            channel_ref_id = channel_ref.getAttribute("ID-REF")
            try:
                inputs = connector.getElementsByTagName("fx:INPUTS")[0]
                input_port = inputs.getElementsByTagName("fx:INPUT-PORT")
                self._ecuRxList = []
                for port in input_port:
                    frame_triggering_ref = port.getElementsByTagName("fx:FRAME-TRIGGERING-REF")[0]
                    frame_triggering_ref_id = frame_triggering_ref.getAttribute("ID-REF")
                    self._ecuRxList += [frame_triggering_ref_id]
            except Exception as e:
                self._ecuRxList = []
            try:
                outputs = connector.getElementsByTagName("fx:OUTPUTS")[0]
                output_port = outputs.getElementsByTagName("fx:OUTPUT-PORT")
                self._ecuTxList = []
                for port in output_port:
                    frame_triggering_ref = port.getElementsByTagName("fx:FRAME-TRIGGERING-REF")[0]
                    frame_triggering_ref_id = frame_triggering_ref.getAttribute("ID-REF")
                    self._ecuTxList += [frame_triggering_ref_id]
            except Exception as e:
                self._ecuTxList = []

            ecu_nodes = FrEcuNodes(short_name, channel_ref_id, self._ecuRxList, self._ecuTxList)
            self._ecuList += [ecu_nodes]
        return self._ecuList

    def parser_signals(self, node):
        fx_elements = node.getElementsByTagName("fx:ELEMENTS")[0]
        fx_signals = fx_elements.getElementsByTagName("fx:SIGNALS")[0]
        fx_signal = fx_signals.getElementsByTagName("fx:SIGNAL")
        for signal in fx_signal:
            signal_id = signal.getAttribute("ID")
            short_name = signal.getElementsByTagName("ho:SHORT-NAME")[0].lastChild.data
            coding_ref = signal.getElementsByTagName("fx:CODING-REF")[0]
            coding_ref_id_ref = coding_ref.getAttribute("ID-REF")
            try:
                default_value = signal.getElementsByTagName("fx:DEFAULT-VALUE")[0].lastChild.data
            except Exception as e:
                default_value = '0.0'
            try:
                # TODO:由于一些原因,下述的节点并不是必然存在的,因此如果需要解析,需要增加更多解析策略,暂定
                description = signal.getElementsByTagName("ho:DESC")[0].lastChild.data
                # default_value = signal.getElementsByTagName("fx:DEFAULT-VALUE")[0].lastChild.data
                # coding_ref = signal.getElementsByTagName("fx:CODING-REF")[0]
                # coding_ref_id_ref = coding_ref.getAttribute("ID-REF")
                signal_type = signal.getElementsByTagName("fx:SIGNAL-TYPE")[0]
                fx_type = signal_type.getElementsByTagName("fx:TYPE")[0].lastChild.data
                fx_method = signal_type.getElementsByTagName("fx:METHOD")[0].lastChild.data
                fx_attributes = signal_type.getElementsByTagName("fx:ATTRIBUTES")[0]
                fx_attribute = fx_attributes.getElementsByTagName("fx:ATTRIBUTE")[0].lastChild.data
            except Exception as e:
                pass
            signals = FrSignals(signal_id, short_name, default_value, coding_ref_id_ref)
            self._signalsName += [signals]
        return self._signalsName

    def parser_pdus(self, node):
        fx_elements = node.getElementsByTagName("fx:ELEMENTS")[0]
        fx_pdus = fx_elements.getElementsByTagName("fx:PDUS")[0]
        fx_pdu = fx_pdus.getElementsByTagName("fx:PDU")
        for pdu in fx_pdu:
            pdu_id = pdu.getAttribute("ID")
            short_name = pdu.getElementsByTagName("ho:SHORT-NAME")[0].lastChild.data
            byte_length = pdu.getElementsByTagName("fx:BYTE-LENGTH")[0].lastChild.data
            pdu_type = pdu.getElementsByTagName("fx:PDU-TYPE")[0].lastChild.data
            signal_instance = pdu.getElementsByTagName("fx:SIGNAL-INSTANCE")
            self._pduSignals = []
            for instance in signal_instance:
                sig_instance_id = instance.getAttribute('ID')
                sig_instance_bit_position = instance.getElementsByTagName('fx:BIT-POSITION')[0].lastChild.data
                sig_instance_is_high_low_byte_order = instance.getElementsByTagName('fx:IS-HIGH-LOW-BYTE-ORDER')[0].lastChild.data
                sig_instance_signal_ref = instance.getElementsByTagName('fx:SIGNAL-REF')[0]
                sig_instance_signal_ref_id_ref = sig_instance_signal_ref.getAttribute('ID-REF')
                if len(instance.getElementsByTagName('fx:SIGNAL-UPDATE-BIT-POSITION')) != 0:
                    sig_instance_signal_ub_bit_position = instance.getElementsByTagName('fx:SIGNAL-UPDATE-BIT-POSITION')[0].lastChild.data
                else:
                    sig_instance_signal_ub_bit_position = 'None'
                # 输出
                fr_pdu_signals = FrPduSignalInfo(sig_instance_id, sig_instance_bit_position, sig_instance_is_high_low_byte_order, sig_instance_signal_ref_id_ref, sig_instance_signal_ub_bit_position)
                self._pduSignals += [fr_pdu_signals]
            # 输出
            pdus = FrPdus(pdu_id, short_name, byte_length, pdu_type, self._pduSignals)
            self._pdus += [pdus]

        return self._pdus

    def parser_frame_triggerings(self, node):
        fx_elements = node.getElementsByTagName("fx:ELEMENTS")[0]
        fx_channels = fx_elements.getElementsByTagName("fx:CHANNELS")[0]
        fx_channel = fx_channels.getElementsByTagName("fx:CHANNEL")[0]
        fx_frame_triggerings = fx_channel.getElementsByTagName("fx:FRAME-TRIGGERINGS")[0]
        fx_frame_triggering = fx_frame_triggerings.getElementsByTagName("fx:FRAME-TRIGGERING")
        for trigger in fx_frame_triggering:
            # ID
            frame_triggering_id = trigger.getAttribute("ID")

            # fx:TIMINGS/fx:ABSOLUTELY-SCHEDULED-TIMING/
            timings = trigger.getElementsByTagName("fx:TIMINGS")[0]
            absolutely_scheduled_timing = timings.getElementsByTagName("fx:ABSOLUTELY-SCHEDULED-TIMING")[0]
            # fx:SLOT-ID | fx:BASE-CYCLE | fx:CYCLE-REPETITION
            slot_id = absolutely_scheduled_timing.getElementsByTagName("fx:SLOT-ID")[0].lastChild.data
            base_cycle = absolutely_scheduled_timing.getElementsByTagName("fx:BASE-CYCLE")[0].lastChild.data
            cycle_repetition = absolutely_scheduled_timing.getElementsByTagName("fx:CYCLE-REPETITION")[0].lastChild.data

            # fx:FRAME-REF/ID-REF
            frame_ref = trigger.getElementsByTagName('fx:FRAME-REF')[0].getAttribute("ID-REF")

            # 输出
            fr_frame_triggerings = FrFrameTriggerings(frame_triggering_id, slot_id, base_cycle, cycle_repetition,
                                                      frame_ref)
            self._frameTriggerings += [fr_frame_triggerings]
        return self._frameTriggerings

    def parser_frame(self, node):
        fx_elements = node.getElementsByTagName("fx:ELEMENTS")[0]
        fx_frames = fx_elements.getElementsByTagName("fx:FRAMES")[0]
        fx_frame = fx_frames.getElementsByTagName("fx:FRAME")
        for frame in fx_frame:
            # ID
            frame_id = frame.getAttribute("ID")

            # ho:SHORT-NAME
            short_name = frame.getElementsByTagName("ho:SHORT-NAME")[0].lastChild.data

            # fx:BYTE-LENGTH
            byte_length = frame.getElementsByTagName("fx:BYTE-LENGTH")[0].lastChild.data

            # fx:FRAME-TYPE
            frame_type = frame.getElementsByTagName("fx:FRAME-TYPE")[0].lastChild.data

            # fx:PDU-INSTANCES/fx:PDU-INSTANCE/ID
            pdu_instances = frame.getElementsByTagName("fx:PDU-INSTANCES")[0]
            pdu_instance = pdu_instances.getElementsByTagName("fx:PDU-INSTANCE")[0]
            pdu_instance_id = pdu_instance.getAttribute("ID")

            # fx:PDU-INSTANCES/fx:PDU-INSTANCE/fx:PDU-REF/ID-REF
            pdu_ref = pdu_instance.getElementsByTagName("fx:PDU-REF")[0]
            id_ref = pdu_ref.getAttribute("ID-REF")

            # fx:PDU-INSTANCES/fx:PDU-INSTANCE/fx:BIT_POSITION
            bit_position = pdu_instance.getElementsByTagName("fx:BIT-POSITION")[0].lastChild.data

            # fx:PDU-INSTANCES/fx:PDU-INSTANCE/fx:IS-HIGH-LOW-BYTE-ORDER
            is_high_low_byte_order = pdu_instance.getElementsByTagName("fx:IS-HIGH-LOW-BYTE-ORDER")[0].lastChild.data

            # 输出
            fr_frame = FrFRAME(frame_id, short_name, byte_length, frame_type, pdu_instance_id, id_ref, bit_position,
                               is_high_low_byte_order)
            self._frame += [fr_frame]
        return self._frame

    def load(self):
        """
        Opens the xml file and parses its contents.
        """
        try:
            # <wanqiang.liu> add 'r', encoding='UTF-8' , solve UnicodeDecodeError: 'gbk' codec can't decode byte 0x89 in position 4168: illegal multibyte sequence
            dom = xml.dom.minidom.parse(self._xmlPath)
        except OSError:
            print("Invalid file path specified.")
            print(self._xmlPath)
            return
        root = dom.documentElement
        # fx:FRAME
        frames = self.parser_frame(root)
        frames_triggerings = self.parser_frame_triggerings(root)
        pdus = self.parser_pdus(root)
        signals = self.parser_signals(root)
        ecus = self.parser_ecus(root)
        codings = self.parser_processing_coding(root)
        for coding in codings:
            # signal关联coding
            for signal in signals:
                if coding.get_coding_id() == signal.get_coding_ref_id():
                    signal.set_coding(coding)
        for pdu in pdus:
            # pdu关联signals
            for pdu_signal_info in pdu.get_pdu_signals_info():
                for signal in signals:
                    if pdu_signal_info.get_signal_ref_id() == signal.get_signal_id():
                        signal.set_sig_bit_position(pdu_signal_info.get_signals_bit_position())
                        signal.set_sig_ub_position(pdu_signal_info.get_signals_ub_position())
                        pdu.set_signals(signal)
                        # pdu.set_signals_names(sig_signal.get_signal_name())
        for frame in frames:
            # 关联triggerings | 获取slot id, offset , repetition
            for triggering in frames_triggerings:
                if frame.get_id() == triggering.get_frame_ref():
                    frame.set_frame_triggerings(triggering)
            # 关联pdus | 获取signals list and name
            for pdu in pdus:
                # frame关联pdu
                if frame.get_pdu_id_ref() == pdu.get_pdu_id():
                    frame.set_frame_pdus(pdu)
        for frame in frames:
            trigger = frame.get_frame_triggerings()[0]
            for ecu in ecus:
                # 关联RxNodes
                for ref in ecu.get_rx_list():
                    if ref == trigger.get_frame_triggering_id():
                        trigger.set_frame_rx_nodes(ecu.get_name())
                # 关联TxNodes
                for ref in ecu.get_tx_list():
                    if ref == trigger.get_frame_triggering_id():
                        trigger.set_frame_tx_nodes(ecu.get_name())
        # 测试区域
        # for frame in frames:
        #     trigger = frame.get_frame_triggerings()[0]
        #     pdu = frame.get_frame_pdus()[0]
        #     signals = pdu.get_signals()
        #     # signals_name = pdu.get_signals_names()
        #     print(frame.get_name())
        #     print('ByteLen: ' + frame.get_length())
        #     print('SlotID: ' + trigger.get_slot_id())
        #     print('BaseCycle: ' + trigger.get_base_cycle())
        #     print('Repetition: ' + trigger.get_cycle_repetition())
        #     print(trigger.get_frame_tx_nodes())
        #     print(trigger.get_frame_rx_nodes())
        #     print(pdu.get_short_name())
        #     # print(signals_name)
        #     for signal in signals:
        #         coding = signal.get_coding()[0]
        #         print(signal.get_signal_name())
        #         print(coding.get_method_category())
        #         print(coding.get_lower_limit())
        #         print(coding.get_upper_limit())
        #         print(coding.get_regulation())
        #         print(coding.get_value_table())
        #     print('\n\n\n')
        # END
        self._iter_index = 0
        return self


class FrCoding:
    def __init__(self, coding_id, encoding, bit_length, compu_method_category, unit_ref_id, lower_limit, upper_limit,
                 regulation: list, value_table: list):
        """
        Constructor.
        """
        self._codingID = coding_id
        self._encoding = encoding
        self._bitLength = bit_length
        self._methodCategory = compu_method_category
        self._unitRefID = unit_ref_id
        self._lowerLimit = lower_limit
        self._upperLimit = upper_limit
        self._regulation = regulation
        self._valueTable = value_table

    def get_coding_id(self):
        """
        Link FrSignal
        :return:
        """
        return self._codingID

    def get_encoding(self):
        return self._encoding

    def get_bit_length(self):
        return self._bitLength

    def get_method_category(self):
        return self._methodCategory

    def get_unit_ref_id(self):
        return self._unitRefID

    def get_lower_limit(self):
        return self._lowerLimit

    def get_upper_limit(self):
        return self._upperLimit

    def get_regulation(self):
        return self._regulation

    def get_value_table(self):
        return self._valueTable


class FrEcuNodes:
    def __init__(self, short_name, channel_ref_id, ecu_rx_list, ecu_tx_list):
        """
        Constructor.
        """
        self._ecuName = short_name
        self._channelRefID = channel_ref_id
        self._rxList = ecu_rx_list
        self._txList = ecu_tx_list

    def get_name(self):
        return self._ecuName

    def get_rx_list(self):
        return set(self._rxList)

    def get_tx_list(self):
        return set(self._txList)


class FrSignals:
    """
    Contains information on a FrFRAME's ID, length in bytes, transmitting node,
    and the signals it contains.
    """

    def __init__(self, signal_id, short_name, default_value, coding_ref_id_ref):
        """
        Constructor.
        """
        self._signalID = signal_id
        self._signalName = short_name
        self._defaultVal = default_value
        self._codingRefID = coding_ref_id_ref
        self._codingInstance = list()
        self._sigBitPosition = ''
        self._sigUbPosition = ''

    def get_signal_name(self):
        return self._signalName

    def get_signal_id(self):
        return self._signalID

    def get_default_val(self):
        return self._defaultVal

    def get_coding_ref_id(self):
        """
        link Coding
        :return:
        """
        return self._codingRefID

    def set_coding(self, coding):
        self._codingInstance += [coding]
        return self

    def get_coding(self):
        return self._codingInstance

    def set_sig_bit_position(self, bit_position):
        self._sigBitPosition = bit_position
        return self

    def get_sig_bit_position(self):
        return self._sigBitPosition

    def set_sig_ub_position(self, ub_position):
        self._sigUbPosition = ub_position
        return self

    def get_sig_ub_position(self):
        return self._sigUbPosition


class FrPduSignalInfo:
    """
    Contains information on a FrFRAME's ID, length in bytes, transmitting node,
    and the signals it contains.
    """

    def __init__(self, sig_instance_id, sig_instance_bit_position, sig_instance_is_high_low_byte_order, sig_instance_signal_ref_id_ref, sig_instance_signal_ub_bit_position):
        """
        Constructor.
        """
        self._signalID = sig_instance_id
        self._bitPosition = sig_instance_bit_position
        self._isHighLowOrder = sig_instance_is_high_low_byte_order
        self._signalRefID = sig_instance_signal_ref_id_ref
        self._signalUbPosition = sig_instance_signal_ub_bit_position

    def get_signal_ref_id(self):
        """
        link -> fx:SIGNALS
        :return:
        """
        return self._signalRefID

    def get_signals_bit_position(self):
        return self._bitPosition

    def get_signals_ub_position(self):
        return self._signalUbPosition


class FrPdus:
    """
    Contains information on a FrFRAME's ID, length in bytes, transmitting node,
    and the signals it contains.
    """

    def __init__(self, pdu_id, short_name, byte_length, pdu_type, pdu_signals):
        """
        Constructor.
        """
        self._pduID = pdu_id
        self._shortName = short_name
        self._byteLen = byte_length
        self._pduType = pdu_type
        self._pduSignalsInfo = pdu_signals
        self._signals = list()
        self._signalsNames = list()

    # 通过Triggers/_signalRefID 找到ID,关联到Class Signals,找到信号名
    # def set_signals_names(self, signals_name):
    #     self._signalsNames += [signals_name]
    #     return self
    #
    # def get_signals_names(self):
    #     return self._signalsNames

    def set_signals(self, signals):
        self._signals += [signals]
        return self

    def get_signals(self):
        return self._signals

    def get_pdu_signals_info(self):
        return self._pduSignalsInfo

    def get_pdu_id(self):
        return self._pduID

    def get_short_name(self):
        return self._shortName

    def get_byte_len(self):
        return self._byteLen

    def get_pdu_type(self):
        return self._pduType


class FrFrameTriggerings:
    """
    Contains information on a FrFRAME's ID, length in bytes, transmitting node,
    and the signals it contains.
    """

    def __init__(self, frame_triggering_id, slot_id, base_cycle, cycle_repetition, frame_ref):
        """
        Constructor.
        """
        self._frame_triggering_id = frame_triggering_id
        self._slot_id = slot_id
        self._base_cycle = base_cycle
        self._cycle_repetition = cycle_repetition
        self._frame_ref = frame_ref
        self._rxNodes = list()
        self._txNodes = list()

    def set_frame_rx_nodes(self, nodes):
        """
        Takes a frame triggerings object and adds it to the list of frame.
        """
        self._rxNodes += [nodes]
        return self

    def get_frame_rx_nodes(self):
        """
        Gets the signals in a CANMessage object.
        """
        return self._rxNodes

    def set_frame_tx_nodes(self, nodes):
        """
        Takes a frame triggerings object and adds it to the list of frame.
        """
        self._txNodes += [nodes]
        return self

    def get_frame_tx_nodes(self):
        """
        Gets the signals in a CANMessage object.
        """
        return self._txNodes

    def get_frame_triggering_id(self):
        """
        link ECUS
        :return:
        """
        return self._frame_triggering_id

    def get_slot_id(self):
        return self._slot_id

    def get_base_cycle(self):
        return self._base_cycle

    def get_cycle_repetition(self):
        return self._cycle_repetition

    def get_frame_ref(self):
        """
        Link -> Frame ID
        :return:
        """
        return self._frame_ref


class FrFRAME:
    """
    Contains information on a FrFRAME's ID, length in bytes, transmitting node,
    and the signals it contains.
    """

    def __init__(self, frame_id, short_name, byte_length, frame_type, pdu_instance_id, id_ref, bit_position,
                 is_high_low_byte_order):
        """
        Constructor.
        """
        self._id = frame_id
        self._name = short_name
        self._dlc = byte_length
        self._type = frame_type
        self._pdu_instance_id = pdu_instance_id
        self._pdu_id_ref = id_ref
        self._bit_position = bit_position
        self._is_high_low_byte_order = is_high_low_byte_order
        self._iter_index = 0
        self._frame_triggerings = list()
        self._framePdus = list()

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
        if self._iter_index == len(self._frame_triggerings):
            self._iter_index = 0
            raise StopIteration
        self._iter_index += 1
        return self._frame_triggerings[self._iter_index - 1]

    def set_frame_triggerings(self, triggerings):
        """
        Takes a frame triggerings object and adds it to the list of frame.
        """
        self._frame_triggerings += [triggerings]
        return self

    def get_frame_triggerings(self):
        """
        Gets the signals in a CANMessage object.
        """
        return self._frame_triggerings

    def set_frame_pdus(self, pdus):
        """
        Takes a frame triggerings object and adds it to the list of frame.
        """
        self._framePdus += [pdus]
        return self

    def get_frame_pdus(self):
        """
        Gets the signals in a CANMessage object.
        """
        return self._framePdus

    def get_id(self):
        """
        frame_id 关联 Triggerings
        :return:
        """
        return self._id

    def get_pdu_id_ref(self):
        """
        关联pdu id
        :return:
        """
        return self._pdu_id_ref

    def get_name(self):
        return self._name

    def get_length(self):
        return self._dlc


def example_parser():
    dev = True
    fact = False
    run_method = dev
    ifile = 'SDB2010707_EX11_A2_BackboneFR_220714.xml'
    ofile = 'SDB2010707_EX11_A2_BackboneFR_220714.can'
    if run_method is True:
        workspace_i = f'./example/input/{ifile}'
        workspace_o = f'./example/output/{ofile}'
    else:
        tmp_date = '20221028'
        workspace_i = f'./workspace/{tmp_date}/input/{ifile}'
        workspace_o = f'./workspace/{tmp_date}/output/{ofile}'

    xml_db = FRDatabase(workspace_i)
    frame_obj = xml_db.load()


def developmentXml2Capl(flexray_xml_path: str = r"example/input/SDB2010707_EX11_A2_BackboneFR_220714.xml"):
    xml_db = FRDatabase(flexray_xml_path)
    frame_obj = xml_db.load()
    ifile = flexray_xml_path
    # 写数据
    with open(f'{flexray_xml_path[flexray_xml_path.rfind("/") + 1:].replace(".xml", "")}.can', 'w') as f:
        # 表头
        f.writelines('/*------------------------------------------------------------\n')
        f.writelines(f' * Author: wanqiang.liu \n')
        f.writelines(' * Description: This file mainly for flexray send msg\n')
        f.writelines(' * Support: Email wanqiang.liu@freetech.com\n')
        f.writelines(f' * Source: {flexray_xml_path}\n')
        f.writelines(f' * FIBEX 3.1.0\n')
        f.writelines(f' * Date: {time.ctime()}\n')
        f.writelines('------------------------------------------------------------*/\n')
        f.writelines('/*@!Encoding:936*/\n')
        f.writelines('includes\n')
        f.writelines('{\n\n')
        f.writelines('}\n\n')
        # variables区域
        f.writelines('/*------------------------------------------------------------\n')
        f.writelines('Intro: define global variables, struct and etc. \n')
        f.writelines(f'@Author: wanqiang.liu  Date: {time.ctime()}\n')
        f.writelines('@Param:   frames          define frames object\n')
        f.writelines('@Param:   puds            define puds object\n')
        f.writelines('@Param:   msTimer         define frames/pdus timer\n')
        f.writelines('@Param:   int cycleTime_  define frames/pdus cycle time\n')
        f.writelines('@Param:   int txEnable_   define frames/pdus tx or not\n')
        f.writelines('@Param:   int cntCycle_   define frames/pdus tx counter\n')
        f.writelines('@Param:   int cntStep1    define frames/pdus tx limit send value 1\n')
        f.writelines('@Param:   int cntStep2    define frames/pdus tx limit send value 2\n')
        f.writelines('------------------------------------------------------------*/\n')
        f.writelines('variables\n')
        f.writelines('{\n')
        f.writelines(f'  /* Control whole messages Tx */\n')
        f.writelines(f'  int _TxEnable_{ifile[ifile.rfind("/") + 1:].replace(".xml", "")} = 0; \n\n\n')
        f.writelines(f'  /* #define NUM */\n')
        f.writelines(f'  const int NUM_TxInit = 1;\n')
        f.writelines(f'  const int NUM_CntInit = 0;\n')
        f.writelines(f'  const int NUM_STEP1 = 500;\n')
        f.writelines(f'  const int NUM_STEP2 = 1000;\n')
        f.writelines(f'  const int NUM_ON = 1;\n')
        f.writelines(f'  const int NUM_OFF = 0;\n')
        f.writelines(f'  const int NUM_CntrLimit = 1;\n')
        f.writelines(f'  \n\n')
        for frame in frame_obj.frames():
            trigger = frame.get_frame_triggerings()[0]
            pdu = frame.get_frame_pdus()[0]
            frame_name = frame.get_name()
            pdu_name = pdu.get_short_name()
            signals = pdu.get_signals()

            f.writelines(f'  /* {frame_name}  ByteLen:{frame.get_length()} Slot:{trigger.get_slot_id()} Offset:{trigger.get_base_cycle()} Repetition:{trigger.get_cycle_repetition()}*/\n')
            f.writelines(f'  frFrame {frame_name} Frm_{frame_name};\n')
            f.writelines(f'  frPDU {pdu_name} Pdu_{pdu_name};\n')
            f.writelines(f'  msTimer msT_{frame_name};\n')
            f.writelines(f'  int cycleTime_{frame_name} = {int(trigger.get_cycle_repetition()) * 5};\n')
            f.writelines(f'  int txEnable_{frame_name} = NUM_TxInit;       //0:TxStop, 1:Tx @sysvar, 2:Tx CycleChange, 3:Tx Cycle\n')
            f.writelines(f'  int cntCycle_{frame_name} = NUM_CntInit;      //use for cycle change message values\n')
            f.writelines(f'  int cntStep1_{frame_name} = NUM_STEP1;        //cntCycle_ <= Step1 send [value1]\n')
            f.writelines(f'  int cntStep2_{frame_name} = NUM_STEP2;        //Step1 < cntCycle_ <= Step2 send [value2]\n')
            f.writelines(f'  /*------ComGwUb or Monitor Signal-----------*/\n')
            f.writelines(f'  int BgnMonitorThisMsg_{pdu_name} = NUM_OFF;  /*control monitor msg on/off, default:off */\n')
            f.writelines(f'  int cntrLimit_{pdu_name} = NUM_CntrLimit;    /*control monitor of cntr to set sysvar to 1 */\n')
            for signal in signals:
                signal_name = signal.get_signal_name()
                f.writelines(f'  int cntr_{pdu_name}_{signal_name} = 0;\n')
            f.writelines('\n')
        f.writelines('}\n\n')
        # on preStart区域
        f.writelines('/*------------------------------------------------------------\n')
        f.writelines(' * on preStart\n')
        f.writelines(f' * Author: wanqiang.liu  Date: {time.ctime()}\n')
        f.writelines(' * API USAGE :\n')
        f.writelines(
            ' * void frSetKeySlot (long channel, long channelMask, long keySlotIndex, long keySlotId, long keySlotUsage);\n')
        f.writelines(' *  - channel:      1 (Cluster 1)\n')
        f.writelines(' *  - channelMask:  1 (Channel A)\n')
        f.writelines(' *  - keySlotIndex: 1 (Key slot1)\n')
        f.writelines(' *  - keySlotId:    7 (Slot 7)\n')
        f.writelines(' *  - keySlotUsage: 1 (Startup/Sync (Allowing Leading Coldstart))\n')
        f.writelines(' * void frSetSendPDU( <PDU object> );\n')
        f.writelines('------------------------------------------------------------*/\n')
        f.writelines('on preStart\n')
        f.writelines('{\n')
        for frame in frame_obj.frames():
            trigger = frame.get_frame_triggerings()[0]
            pdu = frame.get_frame_pdus()[0]
            pdu_name = pdu.get_short_name()
            frame_name = frame.get_name()
            f.writelines(f'  /* {frame_name}   Slot:{trigger.get_slot_id()} */\n')
            f.writelines(f'  frSetKeySlot(1, 1, 1, {trigger.get_slot_id()}, 1);\n')
            f.writelines(f'  frSetSendPDU(Pdu_{pdu_name});\n')
            f.writelines(f'  //frSetSendFrame(Frm_{frame_name});\n')
            f.writelines(f'  //Frm_({frame_name}.fr_flags = 0x0);\n')
            f.writelines(f'  //frUpdateStatFrame(Frm_{pdu_name});\n')
            f.writelines(f'\n\n')
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
        f.writelines('  /* SetTimer for all frame, you can use canceltimer(msT_xxx) */\n')
        for frame in frame_obj.frames():
            frame_name = frame.get_name()
            f.writelines(f'  setTimer(msT_{frame_name}, cycleTime_{frame_name});\n')
        f.writelines('}\n\n')
        # setEnableTx区域
        f.writelines('setEnableTx()\n')
        f.writelines('{ \n')
        num_index = 0
        for frame in frame_obj.frames():
            xml_file_name = ifile[ifile.rfind("/") + 1:].replace(".xml", "")
            frame_name = frame.get_name()
            trigger = frame.get_frame_triggerings()[0]
            tx_nodes = trigger.get_frame_tx_nodes()
            rx_nodes = trigger.get_frame_rx_nodes()
            if 'ASDM' in trigger.get_frame_rx_nodes():
                f.writelines(f'  @FrTx_{xml_file_name}::_Enable_01[{num_index}] = 1;/*{frame_name} Tx:{tx_nodes} Rx:{rx_nodes}*/\n')
            else:
                f.writelines(f'  @FrTx_{xml_file_name}::_Enable_01[{num_index}] = 0;/*{frame_name} Tx:{tx_nodes} Rx:{rx_nodes}*/\n')
            num_index = num_index + 1
        f.writelines('}\n\n')
        # 逻辑主体区域
        num_index = 0
        for frame in frame_obj.frames():
            xml_file_name = ifile[ifile.rfind("/") + 1:].replace(".xml", "")
            trigger = frame.get_frame_triggerings()[0]
            tx_nodes = trigger.get_frame_tx_nodes()
            rx_nodes = trigger.get_frame_rx_nodes()
            pdu = frame.get_frame_pdus()[0]
            frame_name = frame.get_name()
            frame_byte_length = frame.get_length()
            pdu_name = pdu.get_short_name()
            signals = pdu.get_signals()

            f.writelines('/*-------------------------------------------------------------------------------------------------\n')
            f.writelines(f' * on timer {frame_name}\n')
            f.writelines(f' * frame byte length: {frame_byte_length}\n')
            f.writelines(f' * Author : wanqiang.liu@freetech.com\n')
            f.writelines(f' * Date : {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}\n')
            f.writelines(f' * @Param: _TxEnable_{xml_file_name} | control all messages tx or not\n')
            f.writelines(f' * @Param: @FrTx::_Enable_01[{num_index}] | through sysvar control this messages tx or not\n')
            f.writelines(f' * @Param: txEnable_{frame_name} | through global var control this messages tx or not\n')
            f.writelines(f' * @Param: cntCycle_{frame_name} | control script values change cycle\n')
            f.writelines('-------------------------------------------------------------------------------------------------*/\n')
            f.writelines(f'on timer msT_{frame_name}\n')
            f.writelines('{\n')
            f.writelines(f'  setTimer(msT_{frame_name}, cycleTime_{frame_name});\n')
            f.writelines(f'  if(_TxEnable_{xml_file_name} || @FrTx_{xml_file_name}::_Enable_01[{num_index}] == 1)\n')
            num_index = num_index + 1
            f.writelines('  {\n')
            f.writelines('    /* (Panel) Through sysvar control message send */\n')
            # 逻辑主题系统变量控制区域1
            f.writelines(f'    if(txEnable_{frame_name} == 1)\n')
            f.writelines('    {\n')
            for signal in signals:
                signal_name = signal.get_signal_name()
                signal_default_val = signal.get_default_val()
                signal_bit_position = signal.get_sig_bit_position()
                signal_ub_position = signal.get_sig_ub_position()
                coding = signal.get_coding()[0]
                coding_id = coding.get_coding_id()
                encoding = coding.get_encoding()
                bit_length = coding.get_bit_length()
                method_category = coding.get_method_category()
                min_value = coding.get_lower_limit()
                max_value = coding.get_upper_limit()
                regulation = coding.get_regulation()
                for reg in regulation:
                    regulation_offset = reg[0]
                    regulation_factor = reg[1]
                    regulation_denominator = reg[2]
                value_table = coding.get_value_table()
                bit_length_hex = '0x' + 'F' * int(bit_length)
                bit_length_hex_to_dec = str(int(bit_length_hex, 0))

                f.writelines(f'      /* DefaultValue:{signal_default_val}     Min: {min_value}    Max:{max_value}     Category:{method_category}   encoding:{encoding}    coding_id:{coding_id}\n')
                f.writelines(f'       * signal_bit_position:{signal_bit_position}     signal_ub_position:{signal_ub_position}  bit_length:{bit_length}     Hex: {bit_length_hex}    Dec: {bit_length_hex_to_dec}\n')
                f.writelines(f'       * Regulation(numberator1_offset, numberator2_factor, denominator1): {regulation} \n')
                f.writelines(f'       * flexray: (value * numberator2_factor) + numberator1_offset = phys_value  \n')
                f.writelines(f'       *           value = (phys_value - numberator1_offset)/numberator2_factor   \n')
                f.writelines(f'       * valueTable: {value_table} */ \n')
                f.writelines(f'      Pdu_{pdu_name}.{signal_name} = (@sysvar::FrTx_{xml_file_name}::{pdu_name}_{signal_name} - ({regulation_offset}))/{regulation_factor};\n\n')
            f.writelines(f'      frUpdatePDU(Pdu_{pdu_name},1,1);\n')
            f.writelines('    }\n')
            f.writelines('    /* (Script) Cycle change message value send */\n')
            # 逻辑主题 循环发送（变更值）区域2
            f.writelines(f'    else if(txEnable_{frame_name} == 2)\n')
            f.writelines('    {\n')
            f.writelines(f'      cntCycle_{frame_name}++;\n')
            f.writelines(f'      if(cntCycle_{frame_name} <= cntStep1_{frame_name})\n')
            f.writelines('      {\n')
            for signal in signals:
                signal_name = signal.get_signal_name()
                f.writelines(f'        Pdu_{pdu_name}.{signal_name} = 0;\n')
            f.writelines('      }\n')
            f.writelines(f'      else if(cntCycle_{frame_name} <= cntStep2_{frame_name})\n')
            f.writelines('      {\n')
            for signal in signals:
                signal_name = signal.get_signal_name()
                f.writelines(f'        Pdu_{pdu_name}.{signal_name} = 1;\n')
            f.writelines('      }\n')
            f.writelines('      else\n')
            f.writelines('      {\n')
            f.writelines(f'        cntCycle_{frame_name} = 0;\n')
            f.writelines('      }\n\n')
            f.writelines(f'      frUpdatePDU(Pdu_{pdu_name},1,1);\n')
            f.writelines('    }\n')
            f.writelines('    /* (Send Const Value) message send const value */\n')
            # 逻辑主题 固定值发送区域3
            f.writelines(f'    else if(txEnable_{frame_name} == 3)\n')
            f.writelines('    {\n')
            for signal in signals:
                signal_name = signal.get_signal_name()
                f.writelines(f'      Pdu_{pdu_name}.{signal_name} = 0;\n')
            f.writelines(f'      frUpdatePDU(Pdu_{pdu_name},1,1);\n')
            f.writelines('    }\n')
            f.writelines('    else\n')
            f.writelines('    {\n\n')
            f.writelines('    }\n')
            f.writelines('  }\n')
            f.writelines('}\n\n')
        # on FrPdu区域
        for frame in frame_obj.frames():
            xml_file_name = ifile[ifile.rfind("/") + 1:].replace(".xml", "")
            trigger = frame.get_frame_triggerings()[0]
            tx_nodes = trigger.get_frame_tx_nodes()
            rx_nodes = trigger.get_frame_rx_nodes()
            pdu = frame.get_frame_pdus()[0]
            frame_name = frame.get_name()
            frame_byte_length = frame.get_length()
            pdu_name = pdu.get_short_name()
            signals = pdu.get_signals()
            f.writelines('/*-------------------------------------------------------------------------------------------------\n')
            f.writelines(f' * Function: On frPDU  {pdu_name}\n')
            f.writelines(f' * Support: wanqiang.liu@freetech.com\n')
            f.writelines(f' * Description: Monitor Pdu When Value equal xx last for n frame(set by cntrLimit_{pdu_name})\n')
            f.writelines('-------------------------------------------------------------------------------------------------*/\n')
            f.writelines(f'On frPDU {pdu_name}\n')
            f.writelines('{\n')
            f.writelines(f'  if(BgnMonitorThisMsg_{pdu_name} == 1)\n')
            f.writelines('  {\n')
            for signal in signals:
                signal_name = signal.get_signal_name()
                f.writelines(f'    /* MonitorSignal_{signal_name} */\n')
                f.writelines(f'    if(this.{signal_name} == 0)\n')
                f.writelines('    {\n')
                f.writelines(f'      cntr_{pdu_name}_{signal_name}++;\n')
                f.writelines('    }\n')
                f.writelines(f'    else\n')
                f.writelines('    {\n')
                f.writelines(f'      cntr_{pdu_name}_{signal_name} = 0;\n')
                f.writelines('    }\n')
                f.writelines(f'    if(cntr_{pdu_name}_{signal_name} >= cntrLimit_{pdu_name})\n')
                f.writelines('    {\n')
                f.writelines(f'      @FrUb_{xml_file_name}::{pdu_name}_{signal_name} = 1;\n')
                f.writelines('    }\n')
                f.writelines('    else\n')
                f.writelines('    {\n')
                f.writelines(f'      @FrUb_{xml_file_name}::{pdu_name}_{signal_name} = 0;\n')
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
    # 写入FrTx
    # -------------------------------------------------------------------------------------------------------------------------------------
    # node 2
    node_2 = dom.createElement('namespace')
    node_2.setAttribute('name', f"FrTx_{ifile[ifile.rfind('/') + 1:].replace('.xml', '')}")
    node_2.setAttribute('comment', f'Src: {ifile[ifile.rfind("/") + 1:]}    Date: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}')
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
    for frame in frame_obj.frames():
        trigger = frame.get_frame_triggerings()[0]
        pdu = frame.get_frame_pdus()[0]
        xml_file_name = ifile[ifile.rfind("/") + 1:].replace(".xml", "")
        frame_name = frame.get_name()
        pdu_name = pdu.get_short_name()
        signals = pdu.get_signals()
        for signal in signals:
            signal_name = signal.get_signal_name()
            signal_default_val = float(signal.get_default_val())
            signal_bit_position = signal.get_sig_bit_position()
            signal_ub_position = signal.get_sig_ub_position()
            coding = signal.get_coding()[0]
            coding_id = coding.get_coding_id()
            encoding = coding.get_encoding()
            bit_length = coding.get_bit_length()
            method_category = coding.get_method_category()
            min_value = float(coding.get_lower_limit())
            max_value = float(coding.get_upper_limit())
            regulation = coding.get_regulation()
            for reg in regulation:
                regulation_offset = float(reg[0])
                regulation_factor = float(reg[1])
                regulation_denominator = float(reg[2])
            value_table = coding.get_value_table()
            bit_length_hex = '0x' + 'F' * int(bit_length)
            bit_length_hex_to_dec = str(int(bit_length_hex, 0))

            tmp_isSigned = 'false'
            if encoding == 'SIGNED' or min_value < 0:
                tmp_isSigned = 'true'

            node_3 = dom.createElement('variable')
            sysvar_attr_val = {
                "anlyzLocal": "2",
                "readOnly": "false",
                "valueSequence": "false",
                "unit": f"",
                "name": f"{pdu_name}_{signal_name}",
                "comment": f"codingID:{coding_id}   sigBitPos:{signal_bit_position}     sigUbPos:{signal_ub_position}",
                "bitcount": "32",
                "isSigned": f"{tmp_isSigned}",
                "encoding": "65001",
                "type": "int",
                # 信号值
                # "startValue": f"{signal_default_val}",
                # "minValue": f"{min_value}",
                # "minValuePhys": f"{min_value}",
                # "maxValue": f"{max_value}",
                # "maxValuePhys": f"{max_value}"}
                # 物理值
                "startValue": str(int(float(signal_default_val * regulation_factor + regulation_offset))),
                "minValue": f"{str(int(float(((min_value - regulation_offset) / regulation_factor))))}",
                "minValuePhys": f"{str(int(float(min_value)))}",
                "maxValue": f"{str(int(float(((max_value - regulation_offset) / regulation_factor))))}",
                "maxValuePhys": f"{str(int(float(max_value)))}"}
            for attr in sysvar_attr_val:
                node_3.setAttribute(attr, sysvar_attr_val[attr])
            # 如果存在ValueTable
            if len(value_table) != 0:
                node_4 = dom.createElement('valuetable')
                node_4.setAttribute('name', f"{signal_name}")
                node_4.setAttribute('definesMinMax', "true")
                for value_item in value_table:
                    node_5 = dom.createElement('valuetableentry')
                    node_5.setAttribute('value', f"{int(float(value_item[1]))}")
                    node_5.setAttribute('lowerBound', f"{int(float(value_item[1]))}")
                    node_5.setAttribute('upperBound', f"{int(float(value_item[2]))}")
                    node_5.setAttribute('description', f"{value_item[0]}")
                    node_5.setAttribute('displayString', f"{value_item[0]}")
                    node_4.appendChild(node_5)
                node_3.appendChild(node_4)
            node_2.appendChild(node_3)
    # 写入FrUb
    # -------------------------------------------------------------------------------------------------------------------------------------
    # node 2_1
    node_2_1 = dom.createElement('namespace')
    node_2_1.setAttribute('name', f"FrUb_{ifile[ifile.rfind('/') + 1:].replace('.xml', '')}")
    node_2_1.setAttribute('comment', f'Src: {ifile[ifile.rfind("/") + 1:]}    Date: {time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}')
    node_2_1.setAttribute('interface', "")
    # node 3_1
    for frame in frame_obj.frames():
        trigger = frame.get_frame_triggerings()[0]
        pdu = frame.get_frame_pdus()[0]
        xml_file_name = ifile[ifile.rfind("/") + 1:].replace(".xml", "")
        frame_name = frame.get_name()
        pdu_name = pdu.get_short_name()
        signals = pdu.get_signals()
        for signal in signals:
            signal_name = signal.get_signal_name()
            node_3_1 = dom.createElement('variable')
            sysvar_attr_val = {
                "anlyzLocal": "2",
                "readOnly": "false",
                "valueSequence": "false",
                "unit": "",
                "name": f"{pdu_name}_{signal_name}",
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
    fh = codecs.open(f'{flexray_xml_path[flexray_xml_path.rfind("/") + 1:].replace(".xml", "")}.vsysvar', 'w', encoding='utf-8')
    dom.writexml(fh, addindent='\t', newl='\n', encoding='utf-8')
    fh.close()


app = typer.Typer()


@app.command()
def xml2capl(xml_path: str = typer.Argument(..., help="the path of can flexray xml file path , ext with .xml")):
    """
    帮助用户将flexray xml文件快速转换为capl发送脚本。

    :param xml_path: 车载行业flexray xml文件输入

    :return: None
    """
    if os.path.isfile(xml_path):
        if os.path.splitext(xml_path)[-1] == '.xml':
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
                progress.add_task(description="Processing...", total=None)
                progress.add_task(description="Preparing...", total=None)
                developmentXml2Capl(xml_path)
                print(f'Done Generator at: [green]{os.path.dirname(xml_path)}[/green]')
        else:
            print('[red]file format not in support list[/red]')


if __name__ == "__main__":
    app()
    # main()
    # parser()
