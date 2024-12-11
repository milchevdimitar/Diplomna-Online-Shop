from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QVBoxLayout, QPushButton, QMessageBox, QListWidget
from PyQt5.QtCore import Qt
import sys
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Product, Category, Manufacturer, Model, Partmanufacturer

# Създаване на основния клас Base
Base = declarative_base()

engine = create_engine('postgresql://postgres:postgres@localhost/diplomna_v2')
Session = sessionmaker(bind=engine)
session = Session()

# Дефиниция на таблицата за много към много релация между продукти и модели
product_model = Table('product_model', Base.metadata,
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
    Column('model_id', Integer, ForeignKey('model.id'), primary_key=True)
)

class AddProductApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавяне на продукт')
        self.setGeometry(100, 100, 400, 650)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Име:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.description_label = QLabel("Описание:")
        self.description_input = QTextEdit()
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)

        self.serial_number_label = QLabel("Сериен номер:")
        self.serial_number_input = QLineEdit()
        layout.addWidget(self.serial_number_label)
        layout.addWidget(self.serial_number_input)

        self.manufactor_label = QLabel("Производител (на продукта):")
        self.manufactor_dropdown = QComboBox()
        self.populate_manufactors()
        layout.addWidget(self.manufactor_label)
        layout.addWidget(self.manufactor_dropdown)

        self.car_manufacturer_label = QLabel("Производител на автомобила:")
        self.car_manufacturer_dropdown = QComboBox()
        layout.addWidget(self.car_manufacturer_label)
        layout.addWidget(self.car_manufacturer_dropdown)

        self.model_compatibility_label = QLabel("Съвместимост с модели:")
        self.model_compatibility_list = QListWidget()
        self.model_compatibility_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.model_compatibility_label)
        layout.addWidget(self.model_compatibility_list)

        self.category_label = QLabel("Категория:")
        self.category_dropdown = QComboBox()
        self.populate_categories()
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_dropdown)

        self.price_label = QLabel("Цена (BGN):")
        self.price_input = QLineEdit()
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)

        self.add_button = QPushButton("Добавяне на продукт")
        self.add_button.clicked.connect(self.add_product)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.populate_car_manufacturers()

    def populate_manufactors(self):
        self.manufactor_dropdown.clear()
        manufactors = session.query(Partmanufacturer).all()
        for manufactor in manufactors:
            self.manufactor_dropdown.addItem(manufactor.name, manufactor.name)

    def populate_car_manufacturers(self):
        self.car_manufacturer_dropdown.clear()
        manufacturers = session.query(Manufacturer).all()
        for manufacturer in manufacturers:
            self.car_manufacturer_dropdown.addItem(manufacturer.name, manufacturer.id)
        
        self.car_manufacturer_dropdown.currentIndexChanged.connect(self.populate_models)

        self.populate_models()

    def populate_models(self):
        self.model_compatibility_list.clear()
        manufacturer_id = self.car_manufacturer_dropdown.currentData()
        if manufacturer_id:
            models = session.query(Model).filter_by(manufacturer_id=manufacturer_id).all()
            for model in models:
                self.model_compatibility_list.addItem(model.name)
                self.model_compatibility_list.item(self.model_compatibility_list.count() - 1).setData(Qt.UserRole, model.id)

    def populate_categories(self):
        self.category_dropdown.clear()
        categories = session.query(Category).all()
        for category in categories:
            self.category_dropdown.addItem(category.name, category.name)

    def add_product(self):
        try:
            name = self.name_input.text()
            description = self.description_input.toPlainText()
            serial_number = self.serial_number_input.text()
            manufacturer_name = self.manufactor_dropdown.currentData()
            category_name = self.category_dropdown.currentData()
            price_bgn = self.price_input.text()

            # Вземане на избраните модели
            selected_models = []
            for item in self.model_compatibility_list.selectedItems():
                selected_models.append(item.data(Qt.UserRole))

            if not name or not description or not serial_number or not manufacturer_name or not category_name or not price_bgn or not selected_models:
                raise ValueError("Моля, попълнете всички полета!")

            try:
                price_bgn = float(price_bgn)
            except ValueError:
                raise ValueError("Моля, въведете валидна цена!")

            # Създаване на нов продукт
            new_product = Product(
                name=name,
                description=description,
                serial_num=serial_number,  # Добавяне на сериен номер
                manufacturer=manufacturer_name,
                category=category_name,
                price_bgn=price_bgn
            )
            session.add(new_product)
            session.flush()

            # Добавяне на асоциациите с моделите
            for model_id in selected_models:
                session.execute(product_model.insert().values(product_id=new_product.id, model_id=model_id))

            session.commit()

            QMessageBox.information(self, "Успех", "Продуктът беше добавен успешно!")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Грешка", f"Неуспешно добавяне: {e}")

    def clear_form(self):
        self.name_input.clear()
        self.description_input.clear()
        self.serial_number_input.clear()
        self.price_input.clear()
        self.manufactor_dropdown.setCurrentIndex(0)
        self.car_manufacturer_dropdown.setCurrentIndex(0)
        self.model_compatibility_list.clearSelection()
        self.category_dropdown.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddProductApp()
    window.show()
    sys.exit(app.exec_())
