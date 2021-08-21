from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton

def init_ui(self):
    '''
    This function create the layout for the analisis window
    '''
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    self.statusBar().showMessage('Ready')

    widget = QWidget(self)
    self.setCentralWidget(widget)
    vlay = QVBoxLayout(widget)
    hlay_first = QHBoxLayout()
    hlay_second = QHBoxLayout()

    # First curve realated layout
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

    # Lower max value related
    # ++++++++++++++++++++++++++
    # Items
    self.label_first_text1 = QLabel('Valor minimo de los maximos:', self)
    self.lower_max_input1 = QLineEdit(self)
    self.label_actual_lower_max1 = QLabel(str(self.integ.lower_max_edi), self)

    #Placement in layout
    hlay_first.addWidget(self.label_first_text1)
    hlay_first.addWidget(self.lower_max_input1)
    hlay_first.addWidget(self.label_actual_lower_max1)
    hlay_first.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

    vlay.addLayout(hlay_first)

    # Higer max related
    # ++++++++++++++++++++++++++

    self.label_first_text2 = QLabel('Valor maximo de los minimos:', self)
    self.higher_min_input1 = QLineEdit(self)
    self.label_actual_higer_min1 = QLabel(str(-self.integ.higer_min_edi), self)

    #Placement in layout
    hlay_first2 = QHBoxLayout()
    hlay_first2.addWidget(self.label_first_text2)
    hlay_first2.addWidget(self.higher_min_input1)
    hlay_first2.addWidget(self.label_actual_higer_min1)
    hlay_first2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

    # Button corresponding to first graph
    pybutton_1 = QPushButton('Calcular', self)
    aux_layer = QHBoxLayout()
    aux_layer.addWidget(pybutton_1)
    aux_layer.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
    first_super_vlay2 = QVBoxLayout()

    first_super_vlay2.addLayout(hlay_first2)
    first_super_vlay2.addLayout(aux_layer)
    vlay.addLayout(first_super_vlay2)

    # Add plot 1 to layout
    vlay.addWidget(self.plot_edi)

    # Second curve realated layouts
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------

    # Lower max value related
    # ++++++++++++++++++++++++++

    # Items
    self.label_second_text1 = QLabel('Valor minimo de los maximos:', self)
    self.lower_max_input2 = QLineEdit(self)
    self.label_actual_lower_max2 = QLabel(str(self.integ.lower_max_pes), self)

    #Placement in layout
    hlay_second.addWidget(self.label_second_text1)
    hlay_second.addWidget(self.lower_max_input2)
    hlay_second.addWidget(self.label_actual_lower_max2)
    hlay_second.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

    vlay.addLayout(hlay_second)

    # Higer max related
    # ++++++++++++++++++++++++++
    self.label_second_text2 = QLabel('Valor maximo de los minimos:', self)
    self.higher_min_input2 = QLineEdit(self)
    self.label_actual_higher_min2 = QLabel(str(-self.integ.higer_min_pes), self)

    #Placement in layout
    hlay_second2 = QHBoxLayout()
    hlay_second2.addWidget(self.label_second_text2)
    hlay_second2.addWidget(self.higher_min_input2)
    hlay_second2.addWidget(self.label_actual_higher_min2)
    hlay_second2.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

    # Button corresponding to second graph
    pybutton_2 = QPushButton('Calcular', self)
    aux_layer = QHBoxLayout()
    aux_layer.addWidget(pybutton_2)
    aux_layer.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))
    second_super_vlay2 = QVBoxLayout()

    second_super_vlay2.addLayout(hlay_second2)
    second_super_vlay2.addLayout(aux_layer)
    vlay.addLayout(second_super_vlay2)

    # Add plot 2 to layout
    vlay.addWidget(self.plot_pes)

    export_button = QPushButton('Exportar datos', self)
    aux_layer = QHBoxLayout()
    aux_layer.addWidget(export_button)
    aux_layer.addItem(QSpacerItem(1000, 10, QSizePolicy.Expanding))

    vlay.addLayout(aux_layer)

    

    # Buttons conections
    pybutton_1.clicked.connect(self.edi_button_clicked)
    pybutton_2.clicked.connect(self.pes_button_clicked)
    export_button.clicked.connect(self.export_data)