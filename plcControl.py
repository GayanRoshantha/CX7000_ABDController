# Working Code 
#Last edit 2026-02-24 4.57 PM

import sys
import pyads
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QTimer


class Ui_Form(object):

    flags = {
        "ABD_AVAILABLE": False,
        "ABD_FAULT": False,
        "ABD_ACTIVE": False,
        "INTRUSION": False,
        "WIN_REQUEST": False,
        "AIRLINE_ID": False,
        "ABD_AUTO": False
    }

    inputStatus = {
        "lcFrontLower": False,
        "lcFrontUpper": False,
        "lcRear": False,
        "peInsRev": False,
        "peInsC": False,
        "peParkRev": False,
        "peParkC": False,
        "peMidRev": False,
        "peMidC": False,
        "peShtrOpen": False,
        "peShtrClose": False,
        "safetyRelay": False
    }

    # --- Setup 100 ms polling timer ---
    poll_timer = QtCore.QTimer()
    poll_timer.start(20)  

    def on_input_changed(self, name, value):
        print(f"{name} changed to {value}")
        self.inputStatus[name] = value
        # TODO: update table row color here
    
    def toggle_pc_heartbeat(self):
        try:
            # Toggle boolean
            self.pcHeartbeat = not self.pcHeartbeat
            
            # Write to PLC global variable
            self.plc1.write_by_name(
                "GVL.pcHeartbeat",  
                self.pcHeartbeat,
                pyads.PLCTYPE_BOOL
            )
        except Exception as e:
            print("Heartbeat write failed:", e)

    def setupUi(self, Form):
        print(pyads.__version__)

        Form.setObjectName("Form")
        Form.resize(1300, 700)
        Form.setWindowTitle("ELENIUM AUTOMATION - ABD Control Panel")
        
        # PLC setup
        self.ams_net_id = "5.166.193.9.1.1"
        self.ads_port = pyads.PORT_TC3PLC1  # 851

        self.plc1 = pyads.Connection(self.ams_net_id, self.ads_port)
        try:
            self.plc1.open()
            print(f"Connected?: {self.plc1.is_open}")
            print(f"Local Address: {self.plc1.get_local_address()}")

            #Shutter bypass
            self.plc1.write_by_name("GVL.bypassShutter", True, pyads.PLCTYPE_BOOL) 
            self.plc1.write_by_name('GVL.bagDropSide', 'R', pyads.PLCTYPE_STRING);   

        except Exception as e:
            print("PLC connection failed:", e)
     #   self.plc = pyads.Connection('5.166.193.9.1.1', 27905)
     #   self.plc1 = pyads.Connection('5.166.193.9.1.1', 851)
     #   self.plc = pyads.Connection('5.166.193.9.1.1', pyads.PORT_TC3PLC1)
      #  self.plc.open()
     #   self.plc1.open()
 
    #    print(f"Connected?: {self.plc1.is_open}")
    #    print(f"Local Address: {self.plc1.get_local_address()}")

        #_translate = QtCore.QCoreApplication.translate


        # -------------------------
        # PC Heartbeat Setup
        # -------------------------
        self.pcHeartbeat = False

        self.heartbeatTimer = QtCore.QTimer(Form)
        self.heartbeatTimer.setInterval(500)  # 500 ms
        self.heartbeatTimer.timeout.connect(self.toggle_pc_heartbeat)
        self.heartbeatTimer.start()


        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setText("ABD Control Panel")
        self.label.setGeometry(QtCore.QRect(500, 5, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label1 = QtWidgets.QLabel(parent=Form)
        self.label1.setText("INPUT STATUS")
        self.label1.setGeometry(QtCore.QRect(5, 50, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label1.setFont(font)
        self.label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label2 = QtWidgets.QLabel(parent=Form)
        self.label2.setText("BHS INPUTS")
        self.label2.setGeometry(QtCore.QRect(260, 50, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label2.setFont(font)
        self.label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        #Signal Inputs Table
        self.tableInputs = QtWidgets.QTableWidget(parent=Form)
        self.tableInputs.setGeometry(QtCore.QRect(20, 80, 205, 500))
        # Set table font size
        table_font = QtGui.QFont()
        table_font.setKerning(False)
        table_font.setPointSize(12)
        self.tableInputs.setFont(table_font)
        self.tableInputs.setColumnCount(1)
        self.tableInputs.setRowCount(12)
        self.tableInputs.setColumnWidth(0, 200)
        self.tableInputs.horizontalHeader().setVisible(False)
        self.tableInputs.verticalHeader().setVisible(False)
        # Set default row height
        self.tableInputs.verticalHeader().setDefaultSectionSize(40)
        self.tableInputs.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 5px; }")

        data = [
            "LC-FRONT-LOWER", "LC-FRONT-UPPER", "LC-REAR", "INSPEREV", "INSPEC",
            "PARKPEREV", "PARKPEC", "MIDPEREV", "MIDPEC", "SHUTTER-PE-OPEN",
            "SHUTTER-PE-CLOSE", "SAFETY RELAY"
        ]

        for i in range(12):
            item = QtWidgets.QTableWidgetItem(data[i])
            # Center align horizontally and vertically
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.tableInputs.setItem(i, 0, item)

        #BHS Inputs Table
        self.tableIPBHS = QtWidgets.QTableWidget(parent=Form)
        self.tableIPBHS.setGeometry(QtCore.QRect(270, 80, 225, 135))
        # Set table font size
        table_font = QtGui.QFont()
        table_font.setKerning(False)
        table_font.setPointSize(12)
        self.tableIPBHS.setFont(table_font)
        self.tableIPBHS.setColumnCount(1)
        self.tableIPBHS.setRowCount(3)
        self.tableIPBHS.setColumnWidth(0, 225)
        self.tableIPBHS.horizontalHeader().setVisible(False)
        self.tableIPBHS.verticalHeader().setVisible(False)
        # Set default row height
        self.tableIPBHS.verticalHeader().setDefaultSectionSize(40)
        self.tableIPBHS.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 5px; }")

        data1 = [
            "WIN AVAIL", "BHS AVAIL", "BHS E-STOP OK"
        ]

        for i in range(3):
            item = QtWidgets.QTableWidgetItem(data1[i])
            # Center align horizontally and vertically
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.tableIPBHS.setItem(i, 0, item)
     
        # Common button font style
        button_font = QtGui.QFont()
        button_font.setKerning(False)
        button_font.setPointSize(12)

        self.default_button_style = "background-color: #535754; color: white; border-radius: 5px;"
        self.default_button_pressed_style = "background-color: #28a745; color: white; border-radius: 5px; font-weight: bold;"

        self.label4 = QtWidgets.QLabel(parent=Form)
        self.label4.setText("PARK CONV")
        self.label4.setGeometry(QtCore.QRect(800, 50, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label4.setFont(font)
        self.label4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #PARK Conv Table
        self.tableParkConv = QtWidgets.QTableWidget(parent=Form)
        self.tableParkConv.setGeometry(QtCore.QRect(810, 80, 225, 185))
        self.tableParkConv.setColumnCount(1)
        self.tableParkConv.setRowCount(4)
        self.tableParkConv.setColumnWidth(0, 200)
        self.tableParkConv.horizontalHeader().setVisible(False)
        self.tableParkConv.verticalHeader().setVisible(False)
        self.tableParkConv.verticalHeader().setDefaultSectionSize(40)  
        self.tableParkConv.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 10px; }")

        # --- Add buttons to each row ---
        dataParkConv = [
            "PARK STOP", "PARK RAMP", "PARK FWD", "PARK REV"
        ]

        for i in range(4):
            btn = QtWidgets.QPushButton(dataParkConv[i])
            btn.setStyleSheet(self.default_button_style)
            btn.setFont(button_font)
            btn.clicked.connect(lambda _, r=i, b=btn, n=dataParkConv[i]: self.on_button_clicked(r, b, n))
            self.tableParkConv.setCellWidget(i, 0, btn)

        self.label5 = QtWidgets.QLabel(parent=Form)
        self.label5.setText("INS CONV")
        self.label5.setGeometry(QtCore.QRect(800, 280, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label5.setFont(font)
        self.label5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        
        #INS Conv Table
        self.tableInsConv = QtWidgets.QTableWidget(parent=Form)
        self.tableInsConv.setGeometry(QtCore.QRect(810, 310, 225, 150))
        self.tableInsConv.setColumnCount(1)
        self.tableInsConv.setRowCount(3)
        self.tableInsConv.setColumnWidth(0, 200)
        self.tableInsConv.horizontalHeader().setVisible(False)
        self.tableInsConv.verticalHeader().setVisible(False)
        self.tableInsConv.verticalHeader().setDefaultSectionSize(40)  
        self.tableInsConv.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 10px; }")

        # --- Add buttons to each row ---
        dataInsConv = [
            "INS STOP", "INS FWD", "INS REV"
        ]

        for i in range(3):
            btn = QtWidgets.QPushButton(dataInsConv[i])
            btn.setStyleSheet(self.default_button_style)
            btn.setFont(button_font)
            btn.clicked.connect(lambda _, r=i, b=btn, n=dataInsConv[i]: self.on_button_clicked(r, b, n))
            self.tableInsConv.setCellWidget(i, 0, btn)

        self.label6 = QtWidgets.QLabel(parent=Form)
        self.label6.setText("MID CONV")
        self.label6.setGeometry(QtCore.QRect(525, 280, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label6.setFont(font)
        self.label6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #MID Conv Table
        self.tableMidConv = QtWidgets.QTableWidget(parent=Form)
        self.tableMidConv.setGeometry(QtCore.QRect(540, 310, 225, 150))
        self.tableMidConv.setColumnCount(1)
        self.tableMidConv.setRowCount(3)
        self.tableMidConv.setColumnWidth(0, 200)
        self.tableMidConv.horizontalHeader().setVisible(False)
        self.tableMidConv.verticalHeader().setVisible(False)
        self.tableMidConv.verticalHeader().setDefaultSectionSize(40)  
        self.tableMidConv.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 10px; }")

        # --- Add buttons to each row ---
        dataMidConv = [
            "MID STOP", "MID FWD", "MID REV"
        ]
        
        for i in range(3):
            btn = QtWidgets.QPushButton(dataMidConv[i])
            btn.setStyleSheet(self.default_button_style)
            btn.setFont(button_font)
            btn.clicked.connect(lambda _, r=i, b=btn, n=dataMidConv[i]: self.on_button_clicked(r, b, n))
            self.tableMidConv.setCellWidget(i, 0, btn)

        #Shutter Table
        self.label7 = QtWidgets.QLabel(parent=Form)
        self.label7.setText("SHUTTER CONTROL")
        self.label7.setGeometry(QtCore.QRect(530, 50, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label7.setFont(font)
        self.label7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.tableShutter = QtWidgets.QTableWidget(parent=Form)
        self.tableShutter.setGeometry(QtCore.QRect(540, 80, 225, 150))
        self.tableShutter.setColumnCount(1)
        self.tableShutter.setRowCount(3)
        self.tableShutter.setColumnWidth(0, 200)
        self.tableShutter.horizontalHeader().setVisible(False)
        self.tableShutter.verticalHeader().setVisible(False)
        self.tableShutter.verticalHeader().setDefaultSectionSize(40)  
        self.tableShutter.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 10px; }")

        # --- Add buttons to each row ---
        dataShtr = [
            "SHUTTER STOP", "SHUTTER OPEN", "SHUTTER CLOSE"
        ]

        for i in range(3):
            btn = QtWidgets.QPushButton(dataShtr[i])
            btn.setStyleSheet(self.default_button_style)
            btn.setFont(button_font)
            btn.clicked.connect(lambda _, r=i, b=btn, n=dataShtr[i]: self.on_button_clicked(r, b, n))
            self.tableShutter.setCellWidget(i, 0, btn)

        self.label3 = QtWidgets.QLabel(parent=Form)
        self.label3.setText("BHS OUTPUTS")
        self.label3.setGeometry(QtCore.QRect(260, 220, 240, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label3.setFont(font)
        self.label3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.tableBHSOutputs = QtWidgets.QTableWidget(parent=Form)
        self.tableBHSOutputs.setGeometry(QtCore.QRect(270, 250, 225, 310))
        self.tableBHSOutputs.setColumnCount(1)
        self.tableBHSOutputs.setRowCount(7)
        self.tableBHSOutputs.setColumnWidth(0, 200)
        self.tableBHSOutputs.horizontalHeader().setVisible(False)
        self.tableBHSOutputs.verticalHeader().setVisible(False)
        self.tableBHSOutputs.verticalHeader().setDefaultSectionSize(40)  
        self.tableBHSOutputs.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 10px; }")

        # --- Add buttons to each row ---
        dataBHSout = [
            "ABD AVAILABLE", "ABD FAULT", "ABD ACTIVE", "INTRUSION", "WIN REQUEST", "AIRLINE ID", "ABD AUTO"
        ]

        for i in range(7):
            btn = QtWidgets.QPushButton(dataBHSout[i])
            btn.setStyleSheet(self.default_button_style)
            btn.setFont(button_font)
            btn.clicked.connect(lambda _, r=i, b=btn, n=dataBHSout[i]: self.bhsButtonClicked(r, b, n))
            self.tableBHSOutputs.setCellWidget(i, 0, btn)

        self.label8 = QtWidgets.QLabel(parent=Form)
        self.label8.setText("OPERATOR PANEL")
        self.label8.setGeometry(QtCore.QRect(1070, 50, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label8.setFont(font)
        self.label8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        #Signal Operator Panel Table
        self.tableOPInputs = QtWidgets.QTableWidget(parent=Form)
        self.tableOPInputs.setGeometry(QtCore.QRect(1080, 80, 205, 380))
        # Set table font size
        table_font = QtGui.QFont()
        table_font.setKerning(False)
        table_font.setPointSize(12)
        self.tableOPInputs.setFont(table_font)
        self.tableOPInputs.setColumnCount(1)
        self.tableOPInputs.setRowCount(8)
        self.tableOPInputs.setColumnWidth(0, 200)
        self.tableOPInputs.horizontalHeader().setVisible(False)
        self.tableOPInputs.verticalHeader().setVisible(False)
        # Set default row height
        self.tableOPInputs.verticalHeader().setDefaultSectionSize(40)
        self.tableOPInputs.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 5px; }")

        dataOP = [
            "AUTO", "MANUAL", "REVERSE", "FAULT RESET", "LOAD",
            "RUN", "RELEASE"
        ]

        for i in range(7):
            item = QtWidgets.QTableWidgetItem(dataOP[i])
            # Center align horizontally and vertically
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.tableOPInputs.setItem(i, 0, item)

        self.label9 = QtWidgets.QLabel(parent=Form)
        self.label9.setText("STATUS SIGNALS")
        self.label9.setGeometry(QtCore.QRect(1070, 470, 230, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label9.setFont(font)
        self.label9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        #Signal Operator Panel Table
        self.tableStatusInputs = QtWidgets.QTableWidget(parent=Form)
        self.tableStatusInputs.setGeometry(QtCore.QRect(1080, 510, 205, 180))
        # Set table font size
        table_font = QtGui.QFont()
        table_font.setKerning(False)
        table_font.setPointSize(12)
        self.tableStatusInputs.setFont(table_font)
        self.tableStatusInputs.setColumnCount(1)
        self.tableStatusInputs.setRowCount(4)
        self.tableStatusInputs.setColumnWidth(0, 200)
        self.tableStatusInputs.horizontalHeader().setVisible(False)
        self.tableStatusInputs.verticalHeader().setVisible(False)
        # Set default row height
        self.tableStatusInputs.verticalHeader().setDefaultSectionSize(40)
        self.tableStatusInputs.setStyleSheet("QTableWidget { border: 2px solid #444444; padding: 5px; }")

        dataStatus = [
            "PLC RUN", "PLC STOP", "PLC ERROR", "HEARTBEAT"
        ]

        for i in range(4):
            item = QtWidgets.QTableWidgetItem(dataStatus[i])
            # Center align horizontally and vertically
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.tableStatusInputs.setItem(i, 0, item)

        # Map each PLC variable → row index
        self.watch_vars = {
            "GVL.lcFrontLower": 0,
            "GVL.lcFrontUpper": 1,
            "GVL.lcRear": 2,
            "GVL.peInsRev": 3,
            "GVL.peInsC": 4,
            "GVL.peParkRev": 5,
            "GVL.peParkC":  6,
            "GVL.peMidRev": 7,
            "GVL.peMidC": 8,
            "GVL.peShtrOpen": 9,            
            "GVL.peShtrClose": 10,
            "GVL.safetyRelay": 11, 
            "GVL.swAuto": 12,
            "GVL.swManual": 13,
            "GVL.pbReverse": 14,
            "GVL.pbFaultReset": 15,
            "GVL.pbLoad": 16,
            "GVL.pbRun":  17,
            "GVL.pbRelease": 18,
            "GVL.winAvail": 19,
            "GVL.bhsAvail": 20,
            "GVL.bhsEstopOk": 21,
            "GVL.plcRun": 22,
            "GVL.plcStop": 23,
            "GVL.plcError": 24,
            "GVL.plcHeartbeat": 25,
        }


        # Keep handles so you can remove notifications if needed
        self.notification_handles = {}

        # Register notifications
        self.register_notifications()
     

    def register_notifications(self):
        attr = pyads.NotificationAttrib(1)   # BOOL = 1 byte

        for var_name, row in self.watch_vars.items():
            # Bind var_name and row into a lambda using default args
            handle = self.plc1.add_device_notification(
                var_name,
                attr,
                lambda n, d, vn=var_name, r=row: self._callback(n, d, vn, r)
            )

            self.notification_handles[var_name] = handle
            #print(f"Notification added: {var_name}")

    def _callback(self, notification, data, var_name, row):
        # Decode BOOL value
        handle, timestamp, value = self.plc1.parse_notification(
            notification,
            pyads.PLCTYPE_BOOL
        )
        # GUI update
        if value:
            self.highlight_row(row, "#00FF00")   # green
        else:
            self.highlight_row(row, "#FFFFFF")   # white


    def bhsButtonClicked(self, row, button, btnName):
        #button.setStyleSheet(self.default_button_pressed_style)
        #QtCore.QTimer.singleShot(100, lambda: self.reset_button_style(button))
        match btnName:
            case "ABD AVAILABLE":
                print("ABD AVAILABLE")
                self.flags["ABD_AVAILABLE"] = not self.flags["ABD_AVAILABLE"]
                if self.flags["ABD_AVAILABLE"]:
                    self.plc1.write_by_name("GVL.abdAvail", True, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_pressed_style)     
                else:
                    self.plc1.write_by_name("GVL.abdAvail", False, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_style)
            case "ABD FAULT":
                print("ABD FAULT")
                self.flags["ABD_FAULT"] = not self.flags["ABD_FAULT"]
                if self.flags["ABD_FAULT"]:
                    self.plc1.write_by_name("GVL.abdFault", True, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_pressed_style)     
                else:
                    self.plc1.write_by_name("GVL.abdFault", False, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_style)
            case "ABD ACTIVE":
                print("ABD ACTIVE")
                self.flags["ABD_ACTIVE"] = not self.flags["ABD_ACTIVE"]
                if self.flags["ABD_ACTIVE"]:
                    self.plc1.write_by_name("GVL.abdActive", True, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_pressed_style)     
                else:
                    self.plc1.write_by_name("GVL.abdActive", False, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_style)
            case "INTRUSION":
                print("ABD INTRUSION")
                self.flags["INTRUSION"] = not self.flags["INTRUSION"]
                if self.flags["INTRUSION"]:
                    self.plc1.write_by_name("GVL.Intrusion", True, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_pressed_style)     
                else:
                    self.plc1.write_by_name("GVL.Intrusion", False, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_style)
            case "WIN REQUEST":
                print("WIN REQUEST")
                self.flags["WIN_REQUEST"] = not self.flags["WIN_REQUEST"]
                if self.flags["WIN_REQUEST"]:
                    self.plc1.write_by_name("GVL.WinReq", True, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_pressed_style)     
                else:
                    self.plc1.write_by_name("GVL.WinReq", False, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_style)
            case "AIRLINE ID":
                print("AIRLINE ID")
            case "ABD AUTO":
                print("ABD AUTO")
                self.flags["ABD_AUTO"] = not self.flags["ABD_AUTO"]
                if self.flags["ABD_AUTO"]:
                    self.plc1.write_by_name("GVL.abdAuto", True, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_pressed_style)     
                else:
                    self.plc1.write_by_name("GVL.abdAuto", False, pyads.PLCTYPE_BOOL)  
                    button.setStyleSheet(self.default_button_style)
            case _:
                print("Unknown button clicked")


    def on_button_clicked(self, row, button, btnName):
        button.setStyleSheet(self.default_button_pressed_style)
        QtCore.QTimer.singleShot(1000, lambda: self.reset_button_style(button))
        match btnName:
            case "INS STOP":
                print("Stopping INS conveyor...")
                self.plc1.write_by_name("GVL.insFwd", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.insRvs", False, pyads.PLCTYPE_BOOL)
                #self.update_input_status()
            # add your logic here
            case "INS FWD":
                print("INS conveyor forward...")
                self.plc1.write_by_name("GVL.insRvs", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.insFwd", True, pyads.PLCTYPE_BOOL)
                #self.update_input_status()
            case "INS REV":
                print("Reversing INS conveyor...")
                self.plc1.write_by_name("GVL.insRvs", True, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.insFwd", False, pyads.PLCTYPE_BOOL)
                #self.update_input_status()
            case "MID STOP":
                print("Stopping middle conveyor...")
                self.plc1.write_by_name("GVL.midFwd", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.midRvs", False, pyads.PLCTYPE_BOOL)
               # self.update_input_status()
            case "MID FWD":
                print("middle conveyor forward...")
                self.plc1.write_by_name("GVL.midRvs", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.midFwd", True, pyads.PLCTYPE_BOOL)
                #self.update_input_status()
            case "MID REV":
                print("Reversing middle conveyor...")
                self.plc1.write_by_name("GVL.midRvs", True, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.midFwd", False, pyads.PLCTYPE_BOOL)
            case "PARK STOP":
                print("Stopping Park conveyor...")
                self.plc1.write_by_name("GVL.parkFwd", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkRvs", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkRamp", False, pyads.PLCTYPE_BOOL)
            case "PARK FWD":
                print("Park conveyor forward...")
                self.plc1.write_by_name("GVL.parkRvs", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkRamp", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkFwd", True, pyads.PLCTYPE_BOOL)
            case "PARK REV":
                print("Reversing Park conveyor...")
                self.plc1.write_by_name("GVL.parkFwd", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkRamp", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkRvs", True, pyads.PLCTYPE_BOOL)
            case "PARK RAMP":
                print("Ramping Park conveyor...")
                self.plc1.write_by_name("GVL.parkRvs", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkFwd", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.parkRamp", True, pyads.PLCTYPE_BOOL)
            case "SHUTTER STOP":
                print("Shutter Stoping...")
                self.plc1.write_by_name("GVL.shtrOpen", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.shtrClose", False, pyads.PLCTYPE_BOOL)
            case "SHUTTER OPEN":
                print("Shutter Opening...")
                self.plc1.write_by_name("GVL.shtrClose", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.shtrOpen", True, pyads.PLCTYPE_BOOL)
            case "SHUTTER CLOSE":
                print("Shutter Closing...")
                self.plc1.write_by_name("GVL.shtrOpen", False, pyads.PLCTYPE_BOOL)
                self.plc1.write_by_name("GVL.shtrClose", True, pyads.PLCTYPE_BOOL)
            case _:
                print("Unknown button clicked")

    def highlight_row(self, row_index, color="#00FF00"):
        if row_index < 12:
            column_count = self.tableInputs.columnCount()
            for col in range(column_count):
                item = self.tableInputs.item(row_index, col)
                if item:
                    item.setBackground(QtGui.QColor(color))   
        elif 12 <= row_index <= 18:
            adjusted_index = row_index - 12
            column_count = self.tableOPInputs.columnCount()
            for col in range(column_count):
                item = self.tableOPInputs.item(adjusted_index, col)
                if item:
                    item.setBackground(QtGui.QColor(color))
        elif 19 <= row_index <= 21:
            adjusted_index1 = row_index - 19
            column_count = self.tableIPBHS.columnCount()
            for col in range(column_count):
                item = self.tableIPBHS.item(adjusted_index1, col)
                if item:
                    item.setBackground(QtGui.QColor(color))
        elif 22 <= row_index <= 25:
            adjusted_index1 = row_index - 22
            column_count = self.tableStatusInputs.columnCount()
            for col in range(column_count):
                item = self.tableStatusInputs.item(adjusted_index1, col)
                if item:
                    item.setBackground(QtGui.QColor(color))
          
        
    def reset_button_style(self, btn):
        btn.setStyleSheet(self.default_button_style)
        #QtCore.QMetaObject.connectSlotsByName(Form)

    """
    def update_input_status(self):
        
        self.inputStatus["lcFrontLower"] = self.plc1.read_by_name("GVL.lcFrontLower", pyads.PLCTYPE_BOOL)
        if self.inputStatus["lcFrontLower"]:
            self.highlight_row(0, "#00FF00")
        else:
            self.highlight_row(0, "#FFFFFF")
        
        self.inputStatus["lcFrontUpper"] = self.plc1.read_by_name("GVL.lcFrontUpper", pyads.PLCTYPE_BOOL)
        if self.inputStatus["lcFrontUpper"]:
            self.highlight_row(1, "#00FF00")
        else:
            self.highlight_row(1, "#FFFFFF")

        self.inputStatus["lcRear"] = self.plc1.read_by_name("GVL.lcRear", pyads.PLCTYPE_BOOL)
        if self.inputStatus["lcRear"]:
            self.highlight_row(2, "#00FF00")
        else:
            self.highlight_row(2, "#FFFFFF")
      

        self.inputStatus["peInsRev"] = self.plc1.read_by_name("GVL.peInsRev", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peInsRev"]:
            self.highlight_row(3, "#00FF00")
        else:
            self.highlight_row(3, "#FFFFFF")

        self.inputStatus["peInsC"] = self.plc1.read_by_name("GVL.peInsC", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peInsC"]:
            self.highlight_row(4, "#00FF00")
        else:
            self.highlight_row(4, "#FFFFFF")

        self.inputStatus["peParkRev"] = self.plc1.read_by_name("GVL.peParkRev", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peParkRev"]:
            self.highlight_row(5, "#00FF00")
        else:
            self.highlight_row(5, "#FFFFFF")

        self.inputStatus["peParkC"] = self.plc1.read_by_name("GVL.peParkC", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peParkC"]:
            self.highlight_row(6, "#00FF00")
        else:
            self.highlight_row(6, "#FFFFFF")

        self.inputStatus["peMidRev"] = self.plc1.read_by_name("GVL.peMidRev", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peMidRev"]:
            self.highlight_row(7, "#00FF00")
        else:
            self.highlight_row(7, "#FFFFFF")
        
        self.inputStatus["peMidC"] = self.plc1.read_by_name("GVL.peMidC", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peMidC"]:
            self.highlight_row(8, "#00FF00")
        else:
            self.highlight_row(8, "#FFFFFF")

        self.inputStatus["peShtrOpen"] = self.plc1.read_by_name("GVL.peShtrOpen", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peShtrOpen"]:
            self.highlight_row(9, "#00FF00")
        else:
            self.highlight_row(9, "#FFFFFF")

        self.inputStatus["peShtrClose"] = self.plc1.read_by_name("GVL.peShtrClose", pyads.PLCTYPE_BOOL)
        if self.inputStatus["peShtrClose"]:
            self.highlight_row(10, "#00FF00")
        else:
            self.highlight_row(10, "#FFFFFF")

        self.inputStatus["safetyRelay"] = self.plc1.read_by_name("GVL.safetyRelay", pyads.PLCTYPE_BOOL)
        if self.inputStatus["safetyRelay"]:
            self.highlight_row(11, "#00FF00")
        else:
            self.highlight_row(11, "#FFFFFF")
        """

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    screens = app.screens()  # list of QScreen objects
    print("Detected screens:", len(screens))
    # Choose monitor index (1 = second monitor). Use 0-based indices.
    target_index = 1
    showScreen = 0 # make 0 if only 1 screen

    if len(screens) > target_index:
        screen = screens[showScreen]
        geom = screen.availableGeometry()  # use availableGeometry to avoid taskbar
        # Ensure the Form has the desired size (setupUi already called Form.resize(...))
        w = Form.width() or 1300
        h = Form.height() or 700

        # Center the window on the target screen:
        x = geom.x() + (geom.width() - w) // 2
        y = geom.y() + (geom.height() - h) // 2
        Form.setGeometry(x, y, w, h)

        # Optional: print debug info
        print("Launching on screen:", target_index, "screen name:", screen.name(), "geometry:", geom.getRect())
    else:
        print("Only one screen detected, using primary screen") # Fallback: only one display found - show on primary

    Form.show()
    #Form.showMaximized()
    Form.show()
    sys.exit(app.exec())
