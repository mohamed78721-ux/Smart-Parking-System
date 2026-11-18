
import sys
import os

# Add project root directory to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QGridLayout,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QComboBox,
    QMessageBox
)

from vehicles import get_vehicles, add_vehicle , delete_vehicle

from parking_spaces import (
    get_parking_spaces,
    add_parking_space,
    update_parking_space
)

class DashboardWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Parking System")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================

        sidebar = QFrame()
        sidebar.setFixedWidth(230)

        sidebar.setStyleSheet("""
            QFrame {
                background-color: #14213D;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 20)
        sidebar_layout.setSpacing(15)

        logo = QLabel("SMART PARKING")

        logo.setStyleSheet("""
            color: white;
            font-size: 19px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(logo)
        sidebar_layout.addSpacing(30)

        # ================= PAGES =================

        self.pages = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.vehicles_page = self.create_vehicles_page()
        self.parking_spaces_page = self.create_parking_spaces_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.vehicles_page)
        self.pages.addWidget(self.parking_spaces_page)

        # ================= MENU BUTTONS =================

        dashboard_button = QPushButton("Dashboard")
        vehicles_button = QPushButton("Vehicles")
        parking_button = QPushButton("Parking Spaces")
        sessions_button = QPushButton("Parking Sessions")
        payments_button = QPushButton("Payments")

        menu_buttons = [
            dashboard_button,
            vehicles_button,
            parking_button,
            sessions_button,
            payments_button
        ]

        for button in menu_buttons:

            button.setFixedHeight(45)

            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 12px;
                    font-size: 14px;
                }

                QPushButton:hover {
                    background-color: #2563EB;
                    border-radius: 6px;
                }
            """)

            sidebar_layout.addWidget(button)

        # Navigation
        dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        vehicles_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )
        parking_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        sidebar_layout.addStretch()

        logout_button = QPushButton("Logout")
        logout_button.setFixedHeight(45)

        sidebar_layout.addWidget(logout_button)

        # ================= MAIN WINDOW =================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

    # ================= DASHBOARD PAGE =================

    def create_dashboard_page(self):

        page = QWidget()
        page.setStyleSheet(
            "background-color: #F4F7FB;"
        )

        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        title = QLabel("Dashboard")

        title.setStyleSheet("""
            color: #14213D;
            font-size: 28px;
            font-weight: bold;
        """)

        subtitle = QLabel(
            "Welcome to Smart Parking Management System"
        )

        subtitle.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Statistics cards

        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        statistics = [
            ("Total Vehicles", "0"),
            ("Total Parking Spaces", "0"),
            ("Available Spaces", "0"),
            ("Occupied Spaces", "0")
        ]

        for index, (name, value) in enumerate(statistics):

            card = QFrame()

            card.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border-radius: 10px;
                }
            """)

            card_layout = QVBoxLayout(card)

            name_label = QLabel(name)

            name_label.setStyleSheet("""
                color: #64748B;
                font-size: 14px;
            """)

            value_label = QLabel(value)

            value_label.setStyleSheet("""
                color: #2563EB;
                font-size: 30px;
                font-weight: bold;
            """)

            card_layout.addWidget(name_label)
            card_layout.addWidget(value_label)

            cards_layout.addWidget(
                card,
                index // 2,
                index % 2
            )

        layout.addLayout(cards_layout)
        layout.addStretch()

        return page

    # ================= VEHICLES PAGE =================

    def create_vehicles_page(self):


        page = QWidget()
        page.setStyleSheet(
            "background-color: #F4F7FB;"
        )

        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        # Page title

        title = QLabel("Vehicles Management")

        title.setStyleSheet("""
            color: #14213D;
            font-size: 28px;
            font-weight: bold;
        """)

        description = QLabel(
            "Manage and view registered vehicles"
        )

        description.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
        """)

        layout.addWidget(title)
        layout.addWidget(description)

        
        # Search and Refresh

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter plate number to search...")

        search_button = QPushButton("Search")
        search_button.setFixedHeight(40)

        refresh_button = QPushButton("Refresh Vehicles")
        refresh_button.setFixedHeight(40)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(refresh_button)

        layout.addLayout(search_layout)



        # ================= ADD VEHICLE FORM =================

        form_layout = QHBoxLayout()

        self.plate_input = QLineEdit()
        self.plate_input.setPlaceholderText("Plate Number")

        self.type_input = QComboBox()
        self.type_input.addItems([
            "Car",
            "Motorcycle",
            "Truck",
            "Bus"
        ])

        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Owner Name")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Owner Phone")

        add_button = QPushButton("Add Vehicle")
        add_button.setFixedHeight(40)

        add_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        form_layout.addWidget(self.plate_input)
        form_layout.addWidget(self.type_input)
        form_layout.addWidget(self.owner_input)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(add_button)

        layout.addLayout(form_layout)

        # ================= VEHICLES TABLE =================

        self.vehicles_table = QTableWidget()

        self.vehicles_table.setColumnCount(5)

        self.vehicles_table.setHorizontalHeaderLabels([
            "Vehicle ID",
            "Plate Number",
            "Vehicle Type",
            "Owner Name",
            "Owner Phone"
        ])

        self.vehicles_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #E2E8F0;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #14213D;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        self.vehicles_table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(self.vehicles_table)

    # Delete vehicle button

        delete_button = QPushButton("Delete Selected Vehicle")
        delete_button.setFixedHeight(40)

        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)

        layout.addWidget(delete_button)

        delete_button.clicked.connect(self.delete_selected_vehicle)
        # Connect buttons

        refresh_button.clicked.connect(
            self.load_vehicles
        )
        search_button.clicked.connect(
            self.search_vehicles
        )
        add_button.clicked.connect(
            self.add_new_vehicle
        )

        # Load vehicles automatically

        self.load_vehicles()

        return page
    
    # ================= PARKING SPACES PAGE =================

    def create_parking_spaces_page(self):

        page = QWidget()
        page.setStyleSheet(
            "background-color: #F4F7FB;"
        )

        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        # Page title

        title = QLabel("Parking Spaces Management")

        title.setStyleSheet("""
            color: #14213D;
            font-size: 28px;
            font-weight: bold;
        """)

        description = QLabel(
            "Manage and view available parking spaces"
        )

        description.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
        """)

        layout.addWidget(title)
        layout.addWidget(description)

        # Search and Refresh

        search_layout = QHBoxLayout()

        self.space_search_input = QLineEdit()
        self.space_search_input.setPlaceholderText(
            "Enter space number to search..."
        )

        search_button = QPushButton("Search")
        search_button.setFixedHeight(40)

        refresh_button = QPushButton("Refresh Spaces")
        refresh_button.setFixedHeight(40)

        search_layout.addWidget(self.space_search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(refresh_button)

        layout.addLayout(search_layout)
                # ================= ADD PARKING SPACE FORM =================

        form_layout = QHBoxLayout()

        self.space_number_input = QLineEdit()
        self.space_number_input.setPlaceholderText("Space Number")

        self.space_type_input = QComboBox()
        self.space_type_input.addItems([
            "Regular",
            "VIP"
        ])

        self.space_location_input = QLineEdit()
        self.space_location_input.setPlaceholderText("Location")

        add_space_button = QPushButton("Add Parking Space")
        add_space_button.setFixedHeight(40)

        add_space_button.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        form_layout.addWidget(self.space_number_input)
        form_layout.addWidget(self.space_type_input)
        form_layout.addWidget(self.space_location_input)
        form_layout.addWidget(add_space_button)

        layout.addLayout(form_layout)

        add_space_button.clicked.connect(
            self.add_new_parking_space
        )

        # Parking Spaces Table

        self.parking_spaces_table = QTableWidget()

        self.parking_spaces_table.setColumnCount(5)

        self.parking_spaces_table.setHorizontalHeaderLabels([
            "Space ID",
            "Space Number",
            "Space Type",
            "Status",
            "Location"
        ])

        self.parking_spaces_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #E2E8F0;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #14213D;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        self.parking_spaces_table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(self.parking_spaces_table)
        # ================= UPDATE PARKING SPACE FORM =================

        update_layout = QHBoxLayout()

        self.update_space_type = QComboBox()
        self.update_space_type.addItems([
            "Regular",
            "VIP"
        ])

        self.update_space_status = QComboBox()
        self.update_space_status.addItems([
            "available",
            "occupied",
            "reserved"
        ])

        self.update_space_location = QLineEdit()
        self.update_space_location.setPlaceholderText(
            "New Location"
        )

        update_button = QPushButton("Update Selected Space")
        update_button.setFixedHeight(40)

        update_button.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #047857;
            }
        """)

        update_layout.addWidget(self.update_space_type)
        update_layout.addWidget(self.update_space_status)
        update_layout.addWidget(self.update_space_location)
        update_layout.addWidget(update_button)

        layout.addLayout(update_layout)

        update_button.clicked.connect(
            self.update_selected_parking_space
        )

        # Connect Buttons

        refresh_button.clicked.connect(
            self.load_parking_spaces
        )

        search_button.clicked.connect(
            self.search_parking_spaces
        )

        # Load data automatically

        self.load_parking_spaces()

        return page
    # ================= LOAD VEHICLES =================

    def load_vehicles(self):

        vehicles = get_vehicles()

        self.vehicles_table.setRowCount(0)

        for row_number, vehicle in enumerate(vehicles):

            self.vehicles_table.insertRow(row_number)

            for column_number, value in enumerate(vehicle):

                item = QTableWidgetItem(str(value))

                self.vehicles_table.setItem(
                    row_number,
                    column_number,
                    item
                )
    # ================= LOAD PARKING SPACES =================

    def load_parking_spaces(self):

        spaces = get_parking_spaces()

        self.parking_spaces_table.setRowCount(0)

        for row_number, space in enumerate(spaces):

            self.parking_spaces_table.insertRow(row_number)

            for column_number, value in enumerate(space):

                item = QTableWidgetItem(str(value))

                self.parking_spaces_table.setItem(
                    row_number,
                    column_number,
                    item
                )
    # ================= SEARCH PARKING SPACES =================

    def search_parking_spaces(self):

        space_number = self.space_search_input.text().strip().lower()

        if not space_number:
            self.load_parking_spaces()
            return

        spaces = get_parking_spaces()

        self.parking_spaces_table.setRowCount(0)

        for space in spaces:

            if space_number in str(space[1]).lower():

                row_number = self.parking_spaces_table.rowCount()

                self.parking_spaces_table.insertRow(row_number)

                for column_number, value in enumerate(space):

                    item = QTableWidgetItem(str(value))

                    self.parking_spaces_table.setItem(
                        row_number,
                        column_number,
                        item
                    )
    # ================= SEARCH VEHICLES =================

    def search_vehicles(self):

        plate_number = self.search_input.text().strip().lower()

        if not plate_number:
            self.load_vehicles()
            return

        vehicles = get_vehicles()

        self.vehicles_table.setRowCount(0)

        for vehicle in vehicles:

            if plate_number in str(vehicle[1]).lower():

                row_number = self.vehicles_table.rowCount()

                self.vehicles_table.insertRow(row_number)

                for column_number, value in enumerate(vehicle):

                    item = QTableWidgetItem(str(value))

                    self.vehicles_table.setItem(
                        row_number,
                        column_number,
                        item
                    )
    
    # ================= DELETE VEHICLE =================

    def delete_selected_vehicle(self):

        selected_row = self.vehicles_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a vehicle first."
            )
            return

        vehicle_id = int(
            self.vehicles_table.item(selected_row, 0).text()
        )

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this vehicle?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        result = delete_vehicle(vehicle_id)

        if result == "success":

            QMessageBox.information(
                self,
                "Success",
                "Vehicle deleted successfully!"
            )

            self.load_vehicles()

        elif result == "has_sessions":

            QMessageBox.warning(
                self,
                "Cannot Delete",
                "This vehicle has parking records and cannot be deleted."
            )

        elif result == "not_found":

            QMessageBox.warning(
                self,
                "Not Found",
                "Vehicle was not found."
            )

        else:

            QMessageBox.critical(
                self,
                "Error",
                "An error occurred while deleting the vehicle."
            )

    # ================= ADD NEW VEHICLE =================

    def add_new_vehicle(self):

        plate_number = self.plate_input.text().strip()

        vehicle_type = self.type_input.currentText()

        owner_name = self.owner_input.text().strip()

        owner_phone = self.phone_input.text().strip()

        # Validate required fields

        if not plate_number or not owner_name:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter plate number and owner name."
            )

            return

        # Save vehicle in database

        success = add_vehicle(
            plate_number,
            vehicle_type,
            owner_name,
            owner_phone if owner_phone else None
        )

        if success:

            QMessageBox.information(
                self,
                "Success",
                "Vehicle added successfully!"
            )

            # Clear input fields

            self.plate_input.clear()
            self.owner_input.clear()
            self.phone_input.clear()

            # Refresh table

            self.load_vehicles()

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Could not add vehicle. Check the information."
            )

    # ================= ADD NEW PARKING SPACE =================

    def add_new_parking_space(self):

        space_number = self.space_number_input.text().strip()

        space_type = self.space_type_input.currentText()

        location = self.space_location_input.text().strip()

        # Validate required fields

        if not space_number or not location:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter space number and location."
            )

            return

        # Save parking space in database

        success = add_parking_space(
            space_number,
            space_type,
            location
        )

        if success:

            QMessageBox.information(
                self,
                "Success",
                "Parking space added successfully!"
            )

            # Clear input fields

            self.space_number_input.clear()
            self.space_type_input.setCurrentIndex(0)
            self.space_location_input.clear()

            # Refresh table

            self.load_parking_spaces()

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Could not add parking space. Check the information."
            )
            
    # ================= UPDATE SELECTED PARKING SPACE =================

    def update_selected_parking_space(self):

        selected_row = self.parking_spaces_table.currentRow()

        # Check if a parking space is selected

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a parking space first."
            )

            return

        # Get selected parking space number

        space_number = self.parking_spaces_table.item(
            selected_row, 1
        ).text()

        # Get new values from input fields

        space_type = self.update_space_type.currentText()

        status = self.update_space_status.currentText()

        location = self.update_space_location.text().strip()

        if not location:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the parking space location."
            )

            return

        # Update database

        result = update_parking_space(
            space_number,
            space_type,
            status,
            location
        )

        if result == "success":

            QMessageBox.information(
                self,
                "Success",
                "Parking space updated successfully!"
            )

            self.update_space_location.clear()

            self.load_parking_spaces()

        elif result == "active_session":

            QMessageBox.warning(
                self,
                "Active Session",
                "Cannot change the status while a vehicle is parked in this space."
            )

        elif result == "not_found":

            QMessageBox.warning(
                self,
                "Not Found",
                "Parking space was not found."
            )

        else:

            QMessageBox.critical(
                self,
                "Error",
                "An error occurred while updating the parking space."
            )
# ================= RUN APPLICATION =================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = DashboardWindow()
    window.showMaximized()

    sys.exit(app.exec())
