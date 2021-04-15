from PyQt5 import QtGui
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from ui import Ui_MainWindow
from form2 import UiForm
import MySQLdb as Mdb
import inspect
from string import digits


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super(Program, self).__init__()
        self.window = Ui_MainWindow()
        self.window.setupUi(self)

        self.form_2 = UiForm()

        headers = {
            "Сотрудники": ["Код сотрудника", "Имя", "Фамилия", "Отчество", "Опыт работы", "Должность", "Отдел"],
            "Должности": ["Название долнжости", "Описание", "Требуемый опыт"],
            "Отделы": ["Номер отдела", "Название отдела"],
            "Имущество": ["Код предмета", "Поставщик", "Ответственной лицо", "Расположение", "Тип", "Состояние",
                          "Стоимость"],
            "Поставщики": ["Наименование организации", "Телефон"],
            "Расположения": ["Корпус", "Этаж", "Кабинет"],
            "Типы имущества": ["Тип", "Описание"],
        }
        self.table = Table(self.window, headers)

        self.__deleted_records = [[], ""]

        self.form_initialization()

    def form_initialization(self):
        tabs = ["Сотрудники", "Должности", "Отделы", "Имущество", "Поставщики", "Расположения", "Типы имущества"]
        for tab in tabs:
            temp = QtWidgets.QWidget()
            temp.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.window.tablesTabs.addTab(temp, tab)

        self.table.display_table("Сотрудники")
        self.input_tabs_enable_tab(0)
        self.filter_table_enable(0)

        self.window.tableWidget.resizeColumnsToContents()

        self.reset()
        #
        self.window.tableWidget.clicked.connect(self.save_cell)
        self.window.tableWidget.itemChanged.connect(self.update_table)
        #
        self.window.filterCombobox.currentIndexChanged.connect(self.filter_combobox_changed)
        #
        self.window.additionCombobox.currentIndexChanged.connect(self.addition_combobox_changed)
        self.window.additionAddButton.clicked.connect(self.addition_add_button_click)
        self.window.tablesTabs.currentChanged.connect(self.table_tabs_changed)
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

        self.window.removalReturnButton.clicked.connect(self.removal_return_button_clicked)

        self.form_2.pushButton.clicked(self.form_2.user_reply_entered)
        self.form_2.pushButton.setAutoDefault(True)
        self.form_2.user_reply.returnPressed.connect(self.form_2.pushButton.click)

    def save_cell(self):
        global previous_cell
        row = self.window.tableWidget.currentItem().row()
        column = self.window.tableWidget.currentItem().column()
        text = self.window.tableWidget.currentItem().text()
        previous_cell = (row, column, text)

    def update_table(self):
        global previous_cell
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = code_obj.co_name
        if code_obj_name != "<module>":
            return

        k = 0
        if self.window.tablesTabs.currentIndex() != 0 and \
                self.window.tablesTabs.currentIndex() != 3 and self.window.tablesTabs.currentIndex() != 2:
            k = 1
        table_name = self.table.get_table_name(self.window.tablesTabs.currentIndex())
        table = self.table.get_table(table_name, with_id=True)
        for i, record in enumerate(table):
            if i == previous_cell[0]:
                record = list(record)
                row_index = previous_cell[1] + k
                new_value = self.window.tableWidget.item(previous_cell[0], previous_cell[1]).text()
                record[row_index] = new_value
                identifier = record[0]

                for j, value in enumerate(record):
                    record[j] = str(value)

                if table_name == "Сотрудники":
                    result = self.validate_staff_addition(*record[1:], fk_is_not_number=True)
                    if result is not None:
                        record = result[0]
                        if row_index == 5:
                            self.window.tableWidget.item(previous_cell[0], previous_cell[1]).setText(result[1])
                        elif row_index == 6:
                            self.window.tableWidget.item(previous_cell[0], previous_cell[1]).setText(result[2])
                        new_value = record[row_index - 1]
                    else:
                        record = result
                elif table_name == "Должности":
                    record = self.validate_posts_addition(*record[1:])
                elif table_name == "Отделы":
                    record = self.validate_department_addition(*record)
                elif table_name == "Имущество":
                    errors = []
                    if row_index == 1:
                        try:
                            if not self.table.is_id_in_table("Поставщики", int(new_value)):
                                errors.append("Такой код сотрудника не существует")
                        except ValueError:
                            errors.append("В это поле вводится код поставщика")

                    elif row_index == 2:
                        try:
                            if not self.table.is_id_in_table("Сотрудники", int(new_value)):
                                errors.append("Такой код сотрудника не существует")
                        except ValueError:
                            errors.append("В это поле вводится код сотрудника")

                    elif row_index == 3:
                        locations_table = self.table.get_table("Расположения", with_id=True)
                        location = 0
                        for rec in locations_table:
                            loc = str(rec[1]) + str(rec[2]) + str(rec[3])
                            if new_value == loc:
                                location = rec[0]
                                new_value = rec[0]
                                break
                        if location == 0:
                            errors.append("Нет такого расположения")
                    elif row_index == 4:
                        types_table = self.table.get_table("Типы имущества", with_id=True)
                        new_value = "".join([letter.lower() for letter in new_value])
                        t = 0
                        for rec in types_table:
                            ty = "".join([letter.lower() for letter in rec[1]])
                            if new_value == ty:
                                t = rec[0]
                                new_value = rec[0]
                                break
                        if t == 0:
                            errors.append("Нет такого типа")
                    elif row_index == 5:
                        error = self.string_validate(new_value, "Состояние")
                        if error != "":
                            errors.append(error)
                    elif row_index == 6:
                        error = self.int_validate(new_value, "Стоимость")
                        if error != "":
                            errors.append(error)
                    if len(errors) != 0:
                        self.window.message.setText(errors[0])
                        self.window.message.exec_()
                        self.window.tableWidget.item(previous_cell[0], previous_cell[1]).setText(previous_cell[2])
                        return
                elif table_name == "Поставщики":
                    record = self.validate_providers_addition(*record[1:])
                elif table_name == "Типы имущества":
                    table_name = "Типы"
                    record = self.validate_types_addition(*record[1:])
                if record is None:
                    self.window.tableWidget.item(previous_cell[0], previous_cell[1]).setText(previous_cell[2])
                    return
                record = list(record)
                record.insert(0, identifier)
                self.table.update_record_in_table(table_name, identifier, row_index, new_value)
                self.table.display_table(table_name)

                break

    def filter_combobox_changed(self):
        self.filter_table_enable(self.window.filterCombobox.currentIndex())
        index = self.window.filterCombobox.currentIndex()
        if index == 0:
            self.table.display_table("Сотрудники")
            self.window.tablesTabs.setCurrentIndex(0)
        elif index == 1:
            self.table.display_table("Имущество")
            self.window.tablesTabs.setCurrentIndex(3)
        elif index == 2:
            self.table.display_table("Поставщики")
            self.window.tablesTabs.setCurrentIndex(4)

    def filter_table_enable(self, tabindex):
        for index in range(0, self.window.filterTabs.count()):
            self.window.filterTabs.setTabEnabled(index, False)

        self.window.filterTabs.setTabEnabled(tabindex, True)
        self.window.filterTabs.setCurrentIndex(tabindex)

    def removal_return_button_clicked(self):
        table_name = self.__deleted_records[1]
        records = self.__deleted_records[0]

        if len(records) == 0:
            self.window.message.setText("Буфер удалённых записей пуст")
            self.window.message.exec_()
            return

        with_id = False
        if table_name == "Имущество" or table_name == "Отделы":
            with_id = True
        else:
            for i in range(0, len(records)):
                records[i] = records[i][1:]

        for record in records:
            self.table.insert_into_table(table_name, *record, with_id=with_id)

        if table_name == "Типы":
            table_name = "Типы имущества"
        self.table.display_table(table_name)

        self.__deleted_records = [[], ""]

    def removal_delete_button_clicked(self):
        records = []

        index = self.window.tablesTabs.currentIndex()
        table_name = self.table.get_table_name(index)
        table = self.table.get_table(table_name, with_all_ids=True)
        if table_name == "Типы имущества":
            table_name = "Типы"
        for item in self.window.tableWidget.selectedItems():
            for i, record in enumerate(table):
                if i == item.row():
                    records.append(record)
        self.delete_records(table_name, records)

    def delete_records(self, table_name, records):
        if table_name == "Типы":
            button_reply = QMessageBox.question(MainWindow, "Удаление данных НЕОБРАТИМО",
                                                "Если вы удалите тип(ы) имущества - удалятся все записи об имуществе,"
                                                " которе имеет соответствующий тип(ы). Вы согласны с этим?",
                                                QMessageBox.Yes, QMessageBox.No)
            if button_reply == QMessageBox.No:
                return
        elif table_name == "Расположения":
            QMessageBox.information(MainWindow, "Действие отмененно", "Нельзя удалять расположения")
            return
        elif table_name == "Отделы":
            button_reply = QMessageBox.question(MainWindow, "Удаляете отдел?",
                                                "Хотите отправить сотрудников этого отдела в другой?"
                                                " (при нажати кнопки \"Нет\" все сотрудники выбранного отдела"
                                                " будут удалены!", QMessageBox.Yes, QMessageBox.No)
            staff_table = self.table.get_table("Сотрудники", with_all_ids=True)
            employees = []
            for record in records:
                for employee in staff_table:
                    if record[0] == employee[6]:
                        employees.append(employee)
            self.form_2.show()
            return

        button_reply = QMessageBox.question(MainWindow, "Удаление данных НЕОБРАТИМО",
                                            "Вы уверены, что хотите удалить данные?", QMessageBox.Yes, QMessageBox.No)
        if button_reply == QMessageBox.No:
            return

        self.__deleted_records[0] = []
        self.__deleted_records[1] = ""

        for record in records:
            self.table.delete_record_from_table(record[0], table_name)
            self.__deleted_records[0].append(record)
            self.__deleted_records[1] = table_name

        if table_name == "Типы":
            table_name = "Типы имущества"

        self.table.display_table(table_name)

        self.reset()

    def filter_delete_button_clicked(self):
        filters = {
            "Сотрудники": self.filter_staff,
            "Имущество": self.filter_property,
            "Поставщики": self.filter_providers
        }
        records = []

        if self.window.filterTabs.currentIndex() == 2:
            table_name = "Поставщики"
        elif self.window.filterTabs.currentIndex() == 1:
            table_name = "Имущество"
        else:
            table_name = "Сотрудники"
        table = filters[table_name]()
        for record in table:
            for rec in self.table.get_table(table_name, with_all_ids=True):
                if rec[0] == record[0]:
                    record = rec
                    break
            records.append(record)
        self.delete_records(table_name, records)

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
            table = self.table.convert_table_to_string(table)
            table = self.table.left_found_records(table, self.window.filterPropSearchEdit.text(),
                                                  self.window.filterPropSearchCB.currentIndex() + 2)
            self.table.color_by_matching_with_another_table(table, (90, 200, 90))

        return table

    def filter_staff(self):
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = code_obj.co_name
        if code_obj_name == "reset":
            return

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
            table = self.table.convert_table_to_string(table)
            table = self.table.left_found_records(table, self.window.filterStaffSeachEdit.text(),
                                                  self.window.filterStaffSortNSearchCB.currentIndex() + 2)
            self.table.color_by_matching_with_another_table(table, (90, 200, 90))

        return table

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
        is_added = False
        if self.window.additionCombobox.currentIndex() == 0:
            is_added = self.add_record_to_staff(self.window.staffFNameEdit.text(), self.window.staffSNameEdit.text(),
                                                self.window.staffPatEdit.text(), self.window.staffExpEdit.text(),
                                                self.window.staffPostCB.currentText(),
                                                self.window.staffDepartmentCB.currentText())
        elif self.window.additionCombobox.currentIndex() == 1:
            is_added = self.add_record_to_posts(self.window.postsTitleEdit.text(),
                                                self.window.typesDiscEdit.toPlainText(),
                                                self.window.postsExpEdit.text())
        elif self.window.additionCombobox.currentIndex() == 2:
            is_added = self.add_record_to_departments(self.window.departmentsIdEdit.text(),
                                                      self.window.departmentsTitleEdit.text())
        elif self.window.additionCombobox.currentIndex() == 3:
            is_added = self.add_record_to_property(self.window.propertyIdEdit.text(),
                                                   self.window.propertyProviderCB.currentText(),
                                                   self.window.propertyEmplIdEdit.text(),
                                                   self.window.propertyLocationCB.currentText(),
                                                   self.window.propertyTypeCB.currentText(),
                                                   self.window.propertyStateCB.currentText(),
                                                   self.window.propertyCostEdit.text())
        elif self.window.additionCombobox.currentIndex() == 4:
            is_added = self.add_record_to_providers(self.window.providersTitleEdit.text(),
                                                    self.window.providersPhoneEdit.text())
        elif self.window.additionCombobox.currentIndex() == 5:
            is_added = self.add_record_to_types(self.window.typesTypeEdit.text(),
                                                self.window.typesDiscEdit.toPlainText())
        #############################################################
        if is_added:
            self.table.update_table(self.window.additionCombobox.currentText())
            self.table.display_table(self.window.additionCombobox.currentText())
            self.reset()

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
        table_name = self.table.get_table_name(index)
        self.table.display_table(table_name)
        if table_name == "Расположения":
            self.window.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        else:
            self.window.tableWidget.setEditTriggers(QtWidgets.QTableWidget.DoubleClicked |
                                                    QtWidgets.QTableWidget.EditKeyPressed |
                                                    QtWidgets.QTableWidget.AnyKeyPressed)

    @staticmethod
    def string_validate(string, field):
        if len(string) == 0:
            return f"Поле \"{field}\" должно состоять как минимум из 1-го символа"
        elif True in [letter in digits for letter in string]:
            return f"В поле \"{field}\" не может быть чисел"
        elif len(string) > 45:
            return f"Поле \"{field}\" должно быть короче 45-ти символов"
        else:
            return ""

    @staticmethod
    def int_validate(string, field):
        try:
            int(string)
            return ""
        except ValueError:
            return f"Поле \"{field}\" должно быть целочисленным"

    def reset(self):
        self.configure_combo_boxes()
        self.window.staffPatEdit.setText("")
        self.window.staffFNameEdit.setText("")
        self.window.staffSNameEdit.setText("")
        self.window.staffExpEdit.setText("")
        self.window.postsTitleEdit.setText("")
        self.window.postsDicsEdit.setText("")
        self.window.postsExpEdit.setText("")
        self.window.departmentsTitleEdit.setText("")
        self.window.departmentsIdEdit.setText("")
        self.window.propertyCostEdit.setText("")
        self.window.propertyIdEdit.setText("")
        self.window.propertyEmplIdEdit.setText("")
        self.window.providersPhoneEdit.setText("")
        self.window.providersTitleEdit.setText("")
        self.window.typesTypeEdit.setText("")
        self.window.typesDiscEdit.setText("")
        #
        #
        self.window.filterStaffDepartCB.setCurrentIndex(0)
        self.window.filterStaffPostsCB.setCurrentIndex(0)
        self.window.filterStaffSortNSearchCB.setCurrentIndex(0)
        table = self.table.get_table("Сотрудники")
        maximum = max([record[4] for record in table])
        self.window.filterPropFromSpinBox.setValue(0)
        self.window.filterStaffExpToSpinB.setValue(maximum)
        self.window.filterStaffDecRadioB_2.setChecked(True)
        self.window.filterStaffSeachEdit.setText("")
        #
        self.window.filterPropLocationCB.setCurrentIndex(0)
        self.window.filterPropProvidersCB.setCurrentIndex(0)
        self.window.filterPropTypeCB.setCurrentIndex(0)
        self.window.filterPropStateCB.setCurrentIndex(0)
        self.window.filterPropDecRadioB_2.setChecked(True)
        self.window.filterPropFromSpinBox.setValue(0)
        table = self.table.get_table("Имущество")
        maximum = max([record[6] for record in table])
        self.window.filterPropToSpinBox.setValue(maximum)
        self.window.filterPropSearchEdit.setText("")
        #
        self.window.filterProvidersSearchEdit.setText("")

    # Имущество
    def validate_property_addition(self, idd_str, provider_str, responsible_person_str, location_str, t_str, state_str,
                                   cost_str):
        error = ""
        errors = [self.int_validate(idd_str, "Код предмета"), self.int_validate(cost_str, "Стоимость"),
                  self.int_validate(responsible_person_str, "Ответственное лицо")]
        try:
            if self.table.is_id_in_table("Имущество", int(idd_str)):
                errors.append("Такой код предмета уже существует")

            if not self.table.is_id_in_table("Сотрудники", int(responsible_person_str)):
                errors.append("Такой код сотрудника не существует")
        except ValueError:
            pass

        for err in errors:
            if err != "":
                error = err
                break

        self.window.message.setText(error)

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        t = 0
        types_table = self.table.get_table("Типы имущества", with_id=True)
        provider = 0
        providers_table = self.table.get_table("Поставщики", with_id=True)
        location = 0
        locations_table = self.table.get_table("Расположения", with_id=True)

        idd = int(idd_str)

        cost = int(cost_str)

        state = state_str

        for record in types_table:
            if record[1] == t_str:
                t = record[0]

        for record in locations_table:
            if str(record[1]) + str(record[2]) + str(record[3]) == location_str:
                location = record[0]

        for record in providers_table:
            if record[1] == provider_str:
                provider = record[0]

        responsible_person = int(responsible_person_str)

        result = (idd, provider, responsible_person, location, t, state, cost)

        return result

    def add_record_to_property(self, idd_str, provider_str, responsible_person_str, location_str, t_str, state_str,
                               cost_str):
        record = self.validate_property_addition(idd_str, provider_str, responsible_person_str, location_str, t_str,
                                                 state_str, cost_str)

        if record is None:
            return False

        idd, provider, responsible_person, location, t, state, cost = record

        self.table.insert_into_table("Имущество", idd, provider, responsible_person,
                                     location, t, state, cost, with_id=True)

        return True

    # Поставщики
    def validate_providers_addition(self, org_name_str, phone_str):
        error = ""
        errors = [self.string_validate(org_name_str, "Наименование организации"),
                  self.int_validate(phone_str, "Номер телефона")]

        if len(phone_str) != 12:
            errors.append("Не верный формат номера")

        for err in errors:
            if err != "":
                error = err
                break

        self.window.message.setText(error)

        if self.window.message.text() != "":
            self.window.message.exec_()
            return

        org_name = org_name_str

        phone = phone_str

        result = (org_name, phone)

        return result

    def add_record_to_providers(self, org_name_str, phone_str):
        record = self.validate_providers_addition(org_name_str, phone_str)

        if record is None:
            return False

        org_name, phone = record

        self.table.insert_into_table("Поставщики", org_name, phone)

        return True

    # Типы имущество
    def validate_types_addition(self, property_type_str, disc_str):
        error = ""
        errors = [self.string_validate(property_type_str, "Тип")]

        for err in errors:
            if err != "":
                error = err
                break

        self.window.message.setText(error)

        if self.window.message.text() != "":
            self.window.message.exec_()
            return None

        property_type = property_type_str

        disc = disc_str

        result = (property_type, disc)

        return result

    def add_record_to_types(self, property_type_str, disc_str):
        record = self.validate_types_addition(property_type_str, disc_str)

        if record is None:
            return False

        property_type, disc = record

        self.table.insert_into_table("Типы", property_type, disc)

        return True

    # Сотрудники
    def validate_staff_addition(self, name_str, surname_str, patronymic_str, experience_str, post_str, department_str,
                                fk_is_not_number=False):
        result = ["", ""]
        error = ""
        post = 0
        posts_table = self.table.get_table("Должности", with_id=True)
        department = 0
        depart_table = self.table.get_table("Отделы")

        errors = [self.string_validate(name_str, "Имя"), self.int_validate(experience_str, "Опыт работы"),
                  self.string_validate(surname_str, "Фамилия"), self.string_validate(patronymic_str, "Отчество")]

        if fk_is_not_number:
            post_str = "".join([letter.lower() for letter in post_str])

            for record in posts_table:
                p = "".join([letter.lower() for letter in record[1]])
                if post_str == p:
                    post_str = post_str[0].upper() + post_str[1:]
                    result[0] = post_str
                    post = int(record[0])
            if len(result[0]) == 0:
                errors.append("Нет такой должности")

            department_str = "".join([letter.lower() for letter in department_str])

            for record in depart_table:
                d = "".join([letter.lower() for letter in record[1]])
                if department_str == d:
                    department_str = department_str[0].upper() + department_str[1:]
                    result[1] = department_str
                    department = int(record[0])
            if len(result[1]) == 0:
                errors.append("Нет такого отдела")

        for err in errors:
            if err != "":
                error = err
                break

        self.window.message.setText(error)

        if self.window.message.text() != "":
            self.window.message.exec_()
            return None

        name = name_str

        surname = surname_str

        patronymic = patronymic_str

        experience = int(experience_str)

        if not fk_is_not_number:
            for record in posts_table:
                if record[1] == post_str:
                    post = int(record[0])

            for record in depart_table:
                if record[1] == department_str:
                    department = int(record[0])

        result.insert(0, (name, surname, patronymic, experience, post, department))

        return result

    def add_record_to_staff(self, name_str, surname_str, patronymic_str, experience_str, post_str, department_str):
        record = self.validate_staff_addition(name_str, surname_str, patronymic_str, experience_str, post_str,
                                              department_str)

        if record is None:
            return False

        name, surname, patronymic, experience, post, department = record[0]

        self.table.insert_into_table("Сотрудники", name, surname, patronymic, experience, post, department)

        return True

    # Должности
    def validate_posts_addition(self, title_str, disc_str, experience_str):
        error = ""
        errors = [self.string_validate(title_str, "Название"), self.int_validate(experience_str, "Требуемый опыт")]

        for err in errors:
            if err != "":
                error = err
                break

        self.window.message.setText(error)

        if self.window.message.text() != "":
            self.window.message.exec_()
            return None

        title = title_str

        experience = int(experience_str)

        disc = disc_str

        result = (title, experience, disc)

        return result

    def add_record_to_posts(self, title_str, disc_str, experience_str):
        record = self.validate_posts_addition(title_str, disc_str, experience_str)

        if record is None:
            return False

        title, experience, disc = record

        self.table.insert_into_table("Должности", title, disc, experience)

        return True

    # Отделы
    def validate_department_addition(self, id_str, title_str):
        error = ""
        errors = [self.string_validate(title_str, "Название отдела"),
                  self.int_validate(self.window.departmentsIdEdit.text(), "Номер отдела")]

        if self.table.is_id_in_table("Отделы", int(id_str)):
            errors.append("Такой номер отдела уже существует")

        for err in errors:
            if err != "":
                error = err
                break

        self.window.message.setText(error)

        if self.window.message.text() != "":
            self.window.message.exec_()
            return None

        title = title_str

        i = int(id_str)

        result = (i, title)

        return result

    def add_record_to_departments(self, id_str, title_str):
        record = self.validate_department_addition(id_str, title_str)

        if record is None:
            return False

        i, title = record

        self.table.insert_into_table("Отделы", i, title, with_id=True)

        return True


class Table:
    def __init__(self, window, headers):
        self.table = window.tableWidget
        self.db = None
        self.tables = {}
        self.tables_with_id = {}
        self.tables_with_all_ids = {}
        self.headers = headers
        self.connect_base()

    def connect_base(self):
        self.db = Mdb.connect('localhost', 'root', '321Ilyxazc', 'trpo_db')
        self.db.set_character_set("utf8")
        self.select_tables()

    def select_tables(self):
        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.Название, отделы.Название
                                            FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                            сотрудники.idДолжности = должности.idДолжности) 
                                            ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT Наименование, Описание FROM типы'''
        location_sql = '''SELECT Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, поставщики.НаименованиеОрганизации,
                 concat(сотрудники.Фамилия,' ', сотрудники.Имя,' ', сотрудники.Отчество),
                             concat(расположения.Корпус, расположения.Этаж, расположения.Кабинет)
                              AS Расположение, типы.Наименование,
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

        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.idДолжности, отделы.idОтделы
                                                            FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                                            сотрудники.idДолжности = должности.idДолжности) ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT idДолжности, Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT idПоставщики, НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT idТипы, Наименование, Описание FROM типы'''
        location_sql = '''SELECT idРасположения, Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, имущество.idПоставщики, имущество.idОтветственноеЛицо,
                                             имущество.idРасположения, имущество.idТипы,
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
            self.tables_with_all_ids[key] = cursor.fetchall()

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

        staff_sql = '''SELECT idСотрудники, Имя, Фамилия, Отчество, ОпытРаботы, должности.idДолжности, отделы.idОтделы
                                                                   FROM отделы INNER JOIN (сотрудники INNER JOIN должности ON
                                                                   сотрудники.idДолжности = должности.idДолжности) ON отделы.idОтделы = сотрудники.idОтделы ORDER BY сотрудники.idСотрудники'''
        departments_sql = '''SELECT * FROM отделы'''
        posts_sql = '''SELECT idДолжности, Название, Описание, ТребуемыйОпыт FROM должности'''
        providers_sql = '''SELECT idПоставщики, НаименованиеОрганизации, телефон FROM поставщики'''
        types_sql = '''SELECT idТипы, Наименование, Описание FROM типы'''
        location_sql = '''SELECT idРасположения, Корпус, Этаж, Кабинет FROM расположения'''
        property_sql = '''SELECT имущество.idИмущество, имущество.idПоставщики, имущество.idОтветственноеЛицо,
                                                    имущество.idРасположения, имущество.idТипы,
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
        self.tables_with_all_ids[table_name] = cursor.fetchall()

    def get_table(self, table_name, with_id=False, with_all_ids=False):
        if with_id:
            return self.tables_with_id[table_name]
        if with_all_ids:
            return self.tables_with_all_ids[table_name]

        return self.tables[table_name]

    def get_table_name(self, index):
        names = list(self.headers.keys())
        return names[index]

    def insert_into_table(self, table_name, *values, with_id=False):
        cursor = self.db.cursor()
        if table_name == "Типы":
            table = self.get_table("Типы имущества", with_id=True)
        else:
            table = self.get_table(table_name, with_id=True)

        auto_increment = 0
        if table_name != "Имущество" and table_name != "Отделы":
            auto_increment = table[-1][0] + 1

            for i in range(0, len(table) - 1):
                if abs(table[i][0] - table[i + 1][0]) >= 2:
                    auto_increment = table[i][0] + 1
                    break

        cursor.execute(f"SELECT * FROM {table_name}")
        headers = cursor.description

        table_name = table_name[0].lower() + table_name[1:]
        sql = f"INSERT INTO {table_name} ("
        for header in headers:
            sql += header[0] + ", "
        sql = sql[0:-2]
        sql += ") VALUES("
        if with_id:
            for value in values:
                try:
                    sql += f"\'{int(value)}\', "
                except ValueError:
                    sql += f"\'{value}\', "
        else:
            sql += f"\'{int(auto_increment)}\', "
            for value in values:
                try:
                    sql += f"\'{int(value)}\', "
                except ValueError:
                    sql += f"\'{value}\', "
        sql = sql[0:-2]
        sql += ");"
        cursor.execute(sql)
        self.db.commit()
        if table_name == "типы":
            table_name = "Типы имущества"
        table_name = table_name[0].upper() + table_name[1:]
        self.update_table(table_name)

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
        if table_name == "Типы":
            table_name = "Типы имущества"
        self.update_table(table_name)

    def update_record_in_table(self, table_name, identifier, row_index, new_value):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        headers = []
        for header in cursor.description:
            headers.append(header[0])

        if isinstance(new_value, str):
            sql_query = f"UPDATE {table_name} SET {headers[row_index]} = '{new_value}' WHERE {headers[0]} = {identifier};"
        else:
            sql_query = f"UPDATE {table_name} SET {headers[row_index]} = {new_value} WHERE {headers[0]} = {identifier};"
        cursor.execute(sql_query)
        self.db.commit()
        self.update_table(table_name)

    def is_id_in_table(self, table_name, identifier):
        table = self.get_table(table_name, with_id=True)
        existing_ids = [record[0] for record in table]
        if identifier in existing_ids:
            return True
        return False

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
            if k == len(searching_word):
                result_table.append(record)

        return result_table

    @staticmethod
    def convert_table_to_string(table):
        new_table = []
        for record in table:
            new_record = []
            for value in record:
                new_record.append(str(value))
            new_table.append(new_record)

        return new_table

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
                if data is None:
                    data = ""
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        #
        self.table.setHorizontalHeaderLabels(self.headers[table_name])
        self.table.resizeColumnsToContents()


#
# QTabBar::tab:selected  {
#     background-color:rgb(255, 255, 0);
# }


qss = '''
* {
    color: rgb(255, 255, 255);
    background-color: rgb(34,34,47);
}

QTabBar::tab {
    background-color:rgb(255, 105, 91);
}
'''
if __name__ == "__main__":
    previous_cell = QtWidgets.QTableWidgetItem()
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
