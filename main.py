# from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from ui import Ui_MainWindow
import MySQLdb as Mdb
from string import digits


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super(Program, self).__init__()
        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        headers = {
            "Сотрудники": ["Код сотруддника", "Имя", "Фамилия", "Отчество", "Опыт работы", "Должность", "Отдел"],
            "Должности": ["Название долнжости", "Описание", "Требуемый опыт"],
            "Отделы": ["Номер отдела", "Название отдела"],
            "Имущество": ["Код предмета", "Поставщик", "Ответственной лицо", "Расположение", "Тип", "Состояние",
                          "Стоимость"],
            "Поставщики": ["Наименование организации", "Телефон"],
            "Расположения": ["Корпус", "Этаж", "Кабинет"],
            "Типы имущества": ["Тип", "Описание"],
        }
        self.table = Table(self.window, headers)

        self.form_initialization()

    def form_initialization(self):
        tabs = ["Сотрудники", "Должности", "Отделы", "Имущество", "Поставщики", "Расположения", "Типы имущества"]
        for tab in tabs:
            temp = QtWidgets.QWidget()
            temp.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.window.tablesTabs.addTab(temp, tab)

        self.table.display_table("Сотрудники")

        # self.table.table.horizontalHeader().setDefaultSectionSize(200)
        self.table.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.window.filterTabs.currentChanged.connect(self.filter_tabs_changed)
        self.window.filterTabs.setCurrentIndex(0)
        self.window.filterCombobox.currentIndexChanged.connect(self.filter_combobox_changed)
        self.input_tabs_enable_tab(0)
        #
        self.window.additionCombobox.currentIndexChanged.connect(self.addition_combobox_changed)
        self.window.additionAddButton.clicked.connect(self.addition_add_button_click)

        self.window.tablesTabs.currentChanged.connect(self.table_tabs_changed)

        table = self.table.get_table("Сотрудники")
        maximum = max([record[4] for record in table])
        self.window.filterStaffExpToSpinB.setValue(maximum)

        table = self.table.get_table("Имущество")
        maximum = max([record[6] for record in table])
        self.window.filterPropToSpinBox.setValue(maximum)

        self.configure_combo_boxes()

        self.window.filterStaffDecRadioB_2.setChecked(True)
        self.window.filterPropDecRadioB_2.setChecked(True)
        #
        self.window.filterStaffDecRadioB_2.toggled.connect(self.filter_staff)
        self.window.filterStaffIncRadioB.toggled.connect(self.filter_staff)
        self.window.filterStaffDecRadioB.toggled.connect(self.filter_staff)
        self.window.filterStaffPostsCB.currentIndexChanged.connect(self.filter_staff)
        self.window.filterStaffDepartCB.currentIndexChanged.connect(self.filter_staff)
        self.window.filterStaffExpFromSpinB.valueChanged.connect(self.filter_staff)
        self.window.filterStaffExpToSpinB.valueChanged.connect(self.filter_staff)
        self.window.filterStaffSortNSearchCB.currentIndexChanged.connect(self.filter_staff)
        self.window.filterStaffSeachEdit.textChanged.connect(self.filter_staff)
        #
        self.window.filterPropDecRadioB.toggled.connect(self.filter_property)
        self.window.filterPropFromSpinBox.textChanged.connect(self.filter_property)
        self.window.filterPropToSpinBox.textChanged.connect(self.filter_property)
        self.window.filterPropIncRadioB.toggled.connect(self.filter_property)
        self.window.filterPropDecRadioB_2.toggled.connect(self.filter_property)
        self.window.filterPropTypeCB.currentIndexChanged.connect(self.filter_property)
        self.window.filterPropStateCB.currentIndexChanged.connect(self.filter_property)
        self.window.filterPropProvidersCB.currentIndexChanged.connect(self.filter_property)
        self.window.filterPropLocationCB.currentIndexChanged.connect(self.filter_property)
        self.window.filterPropSearchEdit.textChanged.connect(self.filter_property)
        self.window.filterPropSearchCB.currentIndexChanged.connect(self.filter_property)

        self.window.filterProvidersSearchEdit.textChanged.connect(self.filter_providers)
        self.window.filterProvidersSortCB.currentIndexChanged.connect(self.filter_providers)

        self.window.filterDeleteButton.clicked.connect(self.filter_delete_button_clicked)

        self.window.removalDeleteButton.clicked.connect(self.removal_delete_button_clicked)

    def removal_delete_button_clicked(self):
        index = self.window.tablesTabs.currentIndex()
        table_name = self.table.get_table_name(index)
        table = self.table.get_table(table_name, with_id=True)
        for item in self.window.tableWidget.selectedItems():
            for i, record in enumerate(table):
                if i == item.row():
                    self.table.delete_record_from_table(record[0], table_name)
        self.table.display_table(table_name)

    def filter_delete_button_clicked(self):
        if self.window.filterTabs.currentIndex() == 2:
            table = self.filter_providers()
            for record in table:
                self.table.delete_record_from_table(record[0], "Поставщики")
            self.table.display_table("Поставщики")

        if self.window.filterTabs.currentIndex() == 1:
            table = self.filter_property()
            for record in table:
                self.table.delete_record_from_table(record[0], "Имущество")
            self.table.display_table("Имущество")

        if self.window.filterTabs.currentIndex() == 0:
            table = self.filter_staff()
            for record in table:
                self.table.delete_record_from_table(record[0], "Сотрудники")
            self.table.display_table("Сотрудники")

    def filter_tabs_changed(self):
        self.window.filterCombobox.setCurrentIndex(self.window.filterTabs.currentIndex())
        self.table.display_table(self.window.filterCombobox.currentText())
        if self.window.filterTabs.currentIndex() == 0:
            self.window.tablesTabs.setCurrentIndex(0)
        if self.window.filterTabs.currentIndex() == 1:
            self.window.tablesTabs.setCurrentIndex(3)
        if self.window.filterTabs.currentIndex() == 2:
            self.window.tablesTabs.setCurrentIndex(4)

    def filter_providers(self):
        table = self.table.get_table("Поставщики")
        table_with_ids = self.table.get_table("Поставщики", with_id=True)

        self.table.display_table("Поставщики", table)
        #
        if len(self.window.filterProvidersSearchEdit.text()) != 0:
            table = self.table.left_found_records(table, self.window.filterProvidersSearchEdit.text(),
                                                  self.window.filterProvidersSortCB.currentIndex() + 1)
            table_with_ids = self.table.left_found_records(table_with_ids, self.window.filterProvidersSearchEdit.text(),
                                                           self.window.filterProvidersSortCB.currentIndex() + 2)
            self.table.color_by_matching_with_another_table(table, (90, 200, 90))

        return table_with_ids

    def filter_property(self):
        table = self.table.get_table("Имущество")

        t = self.window.filterPropTypeCB.currentText()
        location = self.window.filterPropLocationCB.currentText()
        state = self.window.filterPropStateCB.currentText()
        provider = self.window.filterPropProvidersCB.currentText()

        if t != "Все":
            table = self.table.left_only_one_value(table, t, 5)

        if location != "Все":
            table = self.table.left_only_one_value(table, location, 4)

        if state != "Все":
            table = self.table.left_only_one_value(table, state, 6)

        if provider != "Все":
            table = self.table.left_only_one_value(table, provider, 2)

        bottom_value = self.window.filterPropFromSpinBox.value()
        top_value = self.window.filterPropToSpinBox.value()

        table = self.table.left_only_from_to_records(bottom_value, top_value, table, 7)

        if self.window.filterPropDecRadioB.isChecked():
            table = self.table.descending_sort(table, 7)
        if self.window.filterPropIncRadioB.isChecked():
            table = self.table.ascending_sort(table, 7)

        self.table.display_table("Имущество", table)

        if len(self.window.filterPropSearchEdit.text()) != 0:
            table = self.convert_table_to_string(table)
            table = self.table.left_found_records(table, self.window.filterPropSearchEdit.text(),
                                                  self.window.filterPropSearchCB.currentIndex() + 2)
            self.table.color_by_matching_with_another_table(table, (90, 200, 90))
            pass

        return table

    def filter_staff(self):
        table = self.table.get_table("Сотрудники")

        post = self.window.filterStaffPostsCB.currentText()
        department = self.window.filterStaffDepartCB.currentText()

        if post != "Все":
            table = self.table.left_only_one_value(table, post, 6)

        if department != "Все":
            table = self.table.left_only_one_value(table, department, 7)

        bottom_value = self.window.filterStaffExpFromSpinB.value()
        top_value = self.window.filterStaffExpToSpinB.value()

        table = self.table.left_only_from_to_records(bottom_value, top_value, table, 5)

        if self.window.filterStaffDecRadioB.isChecked():
            table = self.table.descending_sort(table, self.window.filterStaffSortNSearchCB.currentIndex() + 2)
        if self.window.filterStaffIncRadioB.isChecked():
            table = self.table.ascending_sort(table, self.window.filterStaffSortNSearchCB.currentIndex() + 2)

        self.table.display_table("Сотрудники", table)

        if len(self.window.filterStaffSeachEdit.text()) != 0:
            table = self.convert_table_to_string(table)
            table = self.table.left_found_records(table, self.window.filterStaffSeachEdit.text(),
                                                  self.window.filterStaffSortNSearchCB.currentIndex() + 2)
            self.table.color_by_matching_with_another_table(table, (90, 200, 90))

        return table

    @staticmethod
    def convert_table_to_string(table):
        new_table = []
        for record in table:
            new_record = []
            for value in record:
                new_record.append(str(value))
            new_table.append(new_record)

        return new_table

    def filter_combobox_changed(self):
        self.window.filterTabs.setCurrentIndex(self.window.filterCombobox.currentIndex())
        self.table.display_table(self.window.filterCombobox.currentText())
        if self.window.filterTabs.currentIndex() == 0:
            self.window.tablesTabs.setCurrentIndex(0)
        if self.window.filterTabs.currentIndex() == 1:
            self.window.tablesTabs.setCurrentIndex(3)
        if self.window.filterTabs.currentIndex() == 2:
            self.window.tablesTabs.setCurrentIndex(4)

    def configure_combo_boxes(self):
        def staff_configure():
            staff = self.table.get_table("Сотрудники")
            posts = set()
            departments = set()
            for record in staff:
                post = record[5]
                depart = record[6]
                posts.add(post)
                departments.add(depart)

            self.window.filterStaffDepartCB.addItem("Все")
            for depart in departments:
                self.window.staffDepartmentCB.addItem(depart)
                self.window.filterStaffDepartCB.addItem(depart)

            self.window.filterStaffPostsCB.addItem("Все")
            for post in posts:
                self.window.staffPostCB.addItem(post)
                self.window.filterStaffPostsCB.addItem(post)

        def property_configure():
            types = set()
            providers = set()
            locations = set()
            states = ["Исправен", "Требуется починка", "Утерян"]
            types_table = self.table.get_table("Типы имущества")
            providers_table = self.table.get_table("Поставщики")
            locations_table = self.table.get_table("Расположения")

            for record in types_table:
                t = record[0]
                types.add(t)
            self.window.filterPropTypeCB.addItem("Все")
            for t in types:
                self.window.propertyTypeCB.addItem(t)
                self.window.filterPropTypeCB.addItem(t)

            for record in providers_table:
                provider = record[0]
                providers.add(provider)
            self.window.filterPropProvidersCB.addItem("Все")
            for provider in providers:
                self.window.propertyProviderCB.addItem(provider)
                self.window.filterPropProvidersCB.addItem(provider)

            self.window.filterPropStateCB.addItem("Все")
            for state in states:
                self.window.propertyStateCB.addItem(state)
                self.window.filterPropStateCB.addItem(state)

            for record in locations_table:
                location = str(record[0]) + str(record[1]) + str(record[2])
                locations.add(location)
            locations = list(locations)
            locations.sort()
            self.window.filterPropLocationCB.addItem("Все")
            for location in locations:
                self.window.propertyLocationCB.addItem(location)
                self.window.filterPropLocationCB.addItem(location)

        def filter_staff_configure():
            fields = ["Имя", "Фамилия", "Отчество", "Опыт работы"]
            for field in fields:
                self.window.filterStaffSortNSearchCB.addItem(field)

        def filter_property_configure():
            fields = ["Поставщики", "Ответственные лица", "Расположения", "Типы"]
            for field in fields:
                self.window.filterPropSearchCB.addItem(field)

        def filter_providers_configure():
            fields = ["Название", "Телефон"]
            for field in fields:
                self.window.filterProvidersSortCB.addItem(field)

        filter_providers_configure()
        filter_property_configure()
        filter_staff_configure()

        staff_configure()

        property_configure()

    def input_tabs_enable_tab(self, tabindex):
        for index in range(0, self.window.additioninputTabs.count()):
            self.window.additioninputTabs.setTabEnabled(index, False)

        self.window.additioninputTabs.setTabEnabled(tabindex, True)
        self.window.additioninputTabs.setCurrentIndex(tabindex)

    def addition_add_button_click(self):
        if self.window.additionCombobox.currentIndex() == 0:
            self.add_record_to_staff()
        elif self.window.additionCombobox.currentIndex() == 1:
            self.add_record_to_posts()
        elif self.window.additionCombobox.currentIndex() == 2:
            self.add_record_to_departments()
        elif self.window.additionCombobox.currentIndex() == 3:
            self.add_record_to_property()
        elif self.window.additionCombobox.currentIndex() == 4:
            self.add_record_to_providers()
        elif self.window.additionCombobox.currentIndex() == 5:
            self.add_record_to_types()
        self.table.update_table(self.window.additionCombobox.currentText())
        self.table.display_table(self.window.additionCombobox.currentText())

    def addition_combobox_changed(self):
        index = self.window.additionCombobox.currentIndex()
        self.input_tabs_enable_tab(index)
        self.window.tablesTabs.setCurrentIndex(index)
        if index == 5:
            self.table.display_table("Типы имущества")
            self.window.tablesTabs.setCurrentIndex(6)
        else:
            self.table.display_table(self.window.additionCombobox.currentText())
            self.window.tablesTabs.setCurrentIndex(index)

    def table_tabs_changed(self):
        index = self.window.tablesTabs.currentIndex()
        self.table.display_table(self.table.get_table_name(index))

    @staticmethod
    def string_validate(string, field):
        if len(string) == 0:
            return f"Поле \"{field}\" должно состоять как минимум из 1-го символа"
        elif True in [letter in digits for letter in string]:
            return f"В поле \"{field}\" не может быть чисел"
        elif len(string) > 45:
            return f"Поле \"{field}\" должно быть короче 45-ти символов"
        else:
            return None

    @staticmethod
    def int_validate(string, field):
        try:
            int(string)
            return None
        except ValueError:
            return f"Поле \"{field}\" должно быть целочисленным"

    def add_record_to_property(self):
        self.window.message.setText("")

        idd = 0
        provider = 0
        responsible_person = 0
        location = 0
        t = 0
        cost = 0

        error = self.int_validate(self.window.propertyIdEdit.text(), "Код предмета")
        if error is not None:
            self.window.message.setText(error)
        else:
            data = self.table.get_table("Имущество")
            existing_ids = [record[0] for record in data]
            if int(self.window.propertyIdEdit.text()) in existing_ids:
                self.window.message.setText("Такой код предмета уже существует")
            else:
                idd = int(self.window.propertyIdEdit.text())

        error = self.int_validate(self.window.propertyCostEdit.text(), "Стоимость")
        if error is not None:
            self.window.message.setText(error)
        else:
            cost = int(self.window.propertyCostEdit.text())

        state = self.window.propertyStateCB.currentText()

        types_table = self.table.get_table("Типы имущества")
        for i, record in enumerate(types_table):
            if record[0] == self.window.propertyTypeCB.currentText():
                t = i + 1

        providers_table = self.table.get_table("Поставщики")
        for i, record in enumerate(providers_table):
            if record[0] == self.window.propertyProviderCB.currentText():
                provider = i + 1

        locations_table = self.table.get_table("Расположения")
        for i, record in enumerate(locations_table):
            if str(record[0]) + str(record[1]) + str(record[2]) == self.window.propertyLocationCB.currentText():
                location = i + 1

        error = self.int_validate(self.window.propertyEmplIdEdit.text(), "Ответственное лицо")
        if error is not None:
            self.window.message.setText(error)
        else:
            data = self.table.get_table("Сотрудники")
            existing_ids = [record[0] for record in data]
            if int(self.window.propertyEmplIdEdit.text()) in existing_ids:
                responsible_person = int(self.window.propertyEmplIdEdit.text())
            else:
                self.window.message.setText("Такой код сотрудника не существует")

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        self.table.insert_into_table("Имущество", idd, provider, responsible_person, location, t, state, cost)

    def add_record_to_providers(self):
        self.window.message.setText("")

        org_name = ""
        phone = ""

        error = self.string_validate(self.window.providersTitleEdit.text(), "Наименование организации")
        if error is not None:
            self.window.message.setText(error)
        else:
            org_name = self.window.providersTitleEdit.text()

        error = self.int_validate(self.window.providersPhoneEdit.text(), "Номер телефона")
        if error is not None:
            self.window.message.setText(error)
        else:
            phone = self.window.providersPhoneEdit.text()
            if len(phone) != 12:
                self.window.message.setText("Не верный формат номера")

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        self.table.insert_into_table("Поставщики", org_name, phone)

    def add_record_to_types(self):
        self.window.message.setText("")

        property_type = ""

        error = self.string_validate(self.window.typesTypeEdit.text(), "Тип")
        if error is not None:
            self.window.message.setText(error)
        else:
            property_type = self.window.typesTypeEdit.text()

        disc = self.window.typesDiscEdit.toPlainText()

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        self.table.insert_into_table("Типы", property_type, disc)

    def add_record_to_staff(self):
        self.window.message.setText("")

        name = ""
        surname = ""
        patronymic = ""
        experience = 0
        post = 0
        department = 0

        error = self.string_validate(self.window.staffFNameEdit.text(), "Имя")
        if error is not None:
            self.window.message.setText(error)
        else:
            name = self.window.staffFNameEdit.text()

        error = self.string_validate(self.window.staffSNameEdit.text(), "Фамилия")
        if error is not None:
            self.window.message.setText(error)
        else:
            surname = self.window.staffSNameEdit.text()

        error = self.string_validate(self.window.staffPatEdit.text(), "Отчество")
        if error is not None:
            self.window.message.setText(error)
        else:
            patronymic = self.window.staffPatEdit.text()

        error = self.int_validate(self.window.staffExpEdit.text(), "Опыт работы")
        if error is not None:
            self.window.message.setText(error)
        else:
            experience = self.window.staffExpEdit.text()

        posts_table = self.table.get_table("Должности")
        for i, record in enumerate(posts_table):
            if record[0] == self.window.staffPostCB.currentText():
                post = i + 1

        depart_table = self.table.get_table("Отделы")
        for record in depart_table:
            if record[1] == self.window.staffDepartmentCB.currentText():
                department = record[0]

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        self.table.insert_into_table("Сотрудники", name, surname, patronymic, experience, post, department)

    def add_record_to_posts(self):
        self.window.message.setText("")

        title = ""
        experience = 0

        error = self.string_validate(self.window.postsTitleEdit.text(), "Название")
        if error is not None:
            self.window.message.setText(error)
        else:
            title = self.window.postsTitleEdit.text()

        error = self.int_validate(self.window.postsExpEdit.text(), "Требуемый опыт")
        if error is not None:
            self.window.message.setText(error)
        else:
            experience = int(self.window.postsExpEdit.text())

        disc = self.window.postsDicsEdit.toPlainText()

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        self.table.insert_into_table("Должности", title, disc, experience)

    def add_record_to_departments(self):
        self.window.message.setText("")

        title = ""
        i = 0

        error = self.string_validate(self.window.departmentsTitleEdit.text(), "Название отдела")
        if error is not None:
            self.window.message.setText(error)
        else:
            title = self.window.departmentsTitleEdit.text()

        error = self.int_validate(self.window.departmentsIdEdit.text(), "Номер отдела")
        if error is not None:
            self.window.message.setText(error)
        else:
            data = self.table.get_table("Отделы")
            existing_ids = [record[0] for record in data]
            if int(self.window.departmentsIdEdit.text()) in existing_ids:
                self.window.message.setText("Такой номер отдела уже существует")
            else:
                i = int(self.window.departmentsIdEdit.text())

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        self.table.insert_into_table("Отделы", i, title)


class Table:
    def __init__(self, window, headers):
        self.table = window.tableWidget
        self.db = None
        self.tables = {}
        self.tables_with_id = {}
        self.headers = headers
        self.connect_base()

    def connect_base(self):
        self.db = Mdb.connect('localhost', 'root', '321Ilyxazc', 'trpo_db')
        self.db.set_character_set("utf8")
        self.select_tables()

    def select_tables(self):
        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.Название, отделы.Название
                                            FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                            сотрудники.idДолжности = должности.idДолжности) ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT Наименование, Описание FROM типы'''
        location_sql = '''SELECT Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, поставщики.НаименованиеОрганизации,
                 concat(сотрудники.Фамилия,' ', сотрудники.Имя,' ', сотрудники.Отчество),
                             concat(расположения.Корпус, расположения.Этаж, расположения.Кабинет) AS Расположение, типы.Наименование,
                              имущество.Состояние, имущество.Стоимость 
                             FROM сотрудники INNER JOIN (типы INNER JOIN (расположения INNER JOIN 
                            (имущество INNER JOIN поставщики on имущество.idПоставщики = поставщики.idПоставщики)
                             ON расположения.idРасположения = имущество.idРасположения) ON типы.idТипы = имущество.idТипы)
                              ON сотрудники.idСотрудники = имущество.idОтветственноеЛицо ORDER BY имущество.idИмущество'''
        queries = {
            "Сотрудники": staff_sql,
            "Отделы": departments_sql,
            "Должности": posts_sql,
            "Имущество": property_sql,
            "Поставщики": providers_sql,
            "Расположения": location_sql,
            "Типы имущества": types_sql,
        }
        cursor = self.db.cursor()

        for key in queries.keys():
            cursor.execute(queries[key])
            self.tables[key] = cursor.fetchall()

        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.Название, отделы.Название
                                                    FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                                    сотрудники.idДолжности = должности.idДолжности) ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT idДолжности, Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT idПоставщики, НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT idТипы, Наименование, Описание FROM типы'''
        location_sql = '''SELECT idРасположения, Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, поставщики.НаименованиеОрганизации,
                         concat(сотрудники.Фамилия,' ', сотрудники.Имя,' ', сотрудники.Отчество),
                                     concat(расположения.Корпус, расположения.Этаж, расположения.Кабинет) AS Расположение, типы.Наименование,
                                      имущество.Состояние, имущество.Стоимость 
                                     FROM сотрудники INNER JOIN (типы INNER JOIN (расположения INNER JOIN 
                                    (имущество INNER JOIN поставщики on имущество.idПоставщики = поставщики.idПоставщики)
                                     ON расположения.idРасположения = имущество.idРасположения) ON типы.idТипы = имущество.idТипы)
                                      ON сотрудники.idСотрудники = имущество.idОтветственноеЛицо ORDER BY имущество.idИмущество'''
        queries = {
            "Сотрудники": staff_sql,
            "Отделы": departments_sql,
            "Должности": posts_sql,
            "Имущество": property_sql,
            "Поставщики": providers_sql,
            "Расположения": location_sql,
            "Типы имущества": types_sql,
        }
        cursor = self.db.cursor()

        for key in queries.keys():
            cursor.execute(queries[key])
            self.tables_with_id[key] = cursor.fetchall()

    def update_table(self, table_name):
        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.Название, отделы.Название
                                                    FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                                    сотрудники.idДолжности = должности.idДолжности) ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT Наименование, Описание FROM типы'''
        location_sql = '''SELECT Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, поставщики.НаименованиеОрганизации,
                         concat(сотрудники.Фамилия,' ', сотрудники.Имя,' ', сотрудники.Отчество),
                                     concat(расположения.Корпус, расположения.Этаж, расположения.Кабинет) AS Расположение, типы.Наименование,
                                      имущество.Состояние, имущество.Стоимость 
                                     FROM сотрудники INNER JOIN (типы INNER JOIN (расположения INNER JOIN 
                                    (имущество INNER JOIN поставщики on имущество.idПоставщики = поставщики.idПоставщики)
                                     ON расположения.idРасположения = имущество.idРасположения) ON типы.idТипы = имущество.idТипы)
                                      ON сотрудники.idСотрудники = имущество.idОтветственноеЛицо ORDER BY имущество.idИмущество'''
        queries = {
            "Сотрудники": staff_sql,
            "Отделы": departments_sql,
            "Должности": posts_sql,
            "Имущество": property_sql,
            "Поставщики": providers_sql,
            "Расположения": location_sql,
            "Типы имущества": types_sql,
        }
        cursor = self.db.cursor()
        cursor.execute(queries[table_name])
        self.tables[table_name] = cursor.fetchall()

        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.Название, отделы.Название
                                                            FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                                            сотрудники.idДолжности = должности.idДолжности) ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT idДолжности, Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT idПоставщики, НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT idТипы, Наименование, Описание FROM типы'''
        location_sql = '''SELECT idРасположения, Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, поставщики.НаименованиеОрганизации,
                                 concat(сотрудники.Фамилия,' ', сотрудники.Имя,' ', сотрудники.Отчество),
                                             concat(расположения.Корпус, расположения.Этаж, расположения.Кабинет) AS Расположение, типы.Наименование,
                                              имущество.Состояние, имущество.Стоимость 
                                             FROM сотрудники INNER JOIN (типы INNER JOIN (расположения INNER JOIN 
                                            (имущество INNER JOIN поставщики on имущество.idПоставщики = поставщики.idПоставщики)
                                             ON расположения.idРасположения = имущество.idРасположения) ON типы.idТипы = имущество.idТипы)
                                              ON сотрудники.idСотрудники = имущество.idОтветственноеЛицо ORDER BY имущество.idИмущество'''
        queries = {
            "Сотрудники": staff_sql,
            "Отделы": departments_sql,
            "Должности": posts_sql,
            "Имущество": property_sql,
            "Поставщики": providers_sql,
            "Расположения": location_sql,
            "Типы имущества": types_sql,
        }

        cursor.execute(queries[table_name])
        self.tables_with_id[table_name] = cursor.fetchall()

    def get_table(self, table_name, with_id=False):
        if with_id:
            return self.tables_with_id[table_name]
        return self.tables[table_name]

    def get_table_name(self, index):
        names = list(self.headers.keys())
        return names[index]

    def insert_into_table(self, table_name, *values):
        cursor = self.db.cursor()

        if table_name == "Сотрудники":
            cursor.execute("INSERT INTO сотрудники (Имя, Фамилия, Отчество, ОпытРаботы, idДолжности, idОтделы) "
                           f"VALUES('{values[0]}', '{values[1]}', '{values[2]}',"
                           f" '{values[3]}', '{values[4]}', '{values[5]}')")

        elif table_name == "Должности":
            cursor.execute("INSERT INTO должности (Название, Описание, ТребуемыйОпыт) "
                           f"VALUES('{values[0]}', '{values[1]}', '{values[2]}')")

        elif table_name == "Отделы":
            cursor.execute(f"INSERT INTO отделы(idОтделы, Название) VALUES ('{values[0]}', '{values[1]}')")

        elif table_name == "Типы":
            cursor.execute("INSERT INTO типы (Наименование, Описание) "
                           f"VALUES('{values[0]}', '{values[1]}')")

        elif table_name == "Поставщики":
            cursor.execute("INSERT INTO поставщики (НаименованиеОрганизации, телефон) "
                           f"VALUES('{values[0]}', '{values[1]}')")

        elif table_name == "Имущество":
            cursor.execute("INSERT INTO имущество (idИмущество, idПоставщики, idОтветственноеЛицо,"
                           " idРасположения, idТипы, Состояние, Стоимость) "
                           f"VALUES('{values[0]}', '{values[1]}', '{values[2]}',"
                           f" '{values[3]}', '{values[4]}', '{values[5]}', '{values[6]}')")

        self.db.commit()

    def get_current_table(self):
        result_table = []
        for i in range(0, self.table.rowCount()):
            record = []
            for j in range(0, self.table.columnCount()):
                value = self.table.item(i, j).text()
                record.append(value)
            result_table.append(record)
        return result_table

    def delete_record_from_table(self, identifier, table_name):
        sql_query = f"DELETE FROM {table_name} WHERE (id{table_name} = {identifier});"
        cursor = self.db.cursor()
        cursor.execute(sql_query)
        self.db.commit()
        self.update_table(table_name)

    @staticmethod
    def left_found_records(table, searching_word, row_number):
        result_table = []
        for record in table:
            k = 0
            index = 0
            for letter in searching_word:
                for i in range(index, len(record[row_number - 1])):
                    if letter.lower() == record[row_number - 1][i].lower():
                        k += 1
                        index = i + 1
                        break
                    pass
            if k == len(searching_word):
                result_table.append(record)

        return result_table

    @staticmethod
    def descending_sort(table, row_number):
        for i in range(1, len(table)):
            f = 0
            for j in range(0, len(table) - i):
                if table[j][row_number - 1] < table[j + 1][row_number - 1]:
                    table[j], table[j + 1] = table[j + 1], table[j]
                    f = 1
            if f == 0:
                break

        return table

    @staticmethod
    def ascending_sort(table, row_number):
        for i in range(1, len(table)):
            f = 0
            for j in range(0, len(table) - i):
                if table[j][row_number - 1] > table[j + 1][row_number - 1]:
                    table[j], table[j + 1] = table[j + 1], table[j]
                    f = 1
            if f == 0:
                break

        return table

    @staticmethod
    def left_only_from_to_records(bottom_value, top_value, table, row_number):
        result_table = []
        for record in table:
            if bottom_value <= record[row_number - 1] <= top_value:
                result_table.append(record)

        return result_table

    @staticmethod
    def left_only_one_value(table, value, row_number):
        result_table = []
        for record in table:
            if record[row_number - 1] == value:
                result_table.append(record)

        return result_table

    def color_by_matching_with_another_table(self, table, color):
        r = color[0]
        g = color[1]
        b = color[2]
        current_table = self.get_current_table()
        for i, record in enumerate(current_table):
            for rec in table:
                k = 0
                for q in range(0, len(rec)):
                    if rec[q] == record[q]:
                        k += 1
                if k == len(rec):
                    for j in range(0, self.table.columnCount()):
                        self.table.item(i, j).setBackground(QtGui.QColor(r, g, b))

    def display_table(self, table_name, table=None):
        if table is None:
            table = self.get_table(table_name)
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        for row_number, row_data in enumerate(table):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if self.table.columnCount() <= column_number:
                    self.table.setColumnCount(self.table.columnCount() + 1)
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.table.setHorizontalHeaderLabels(self.headers[table_name])


# QTabBar::tab:selected  {
#     background-color:rgb(255, 255, 0);
# }


# qss = '''
# QTabBar::tab {
#     background-color:rgb(220, 220, 0);
# }
# '''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qss)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    application = Program()
    application.show()
    sys.exit(app.exec_())

# app = QtWidgets.QApplication([])

# sys.exit(app.exec())
