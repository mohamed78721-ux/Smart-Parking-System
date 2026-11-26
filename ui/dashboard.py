
import sys
import os
from vehicles import get_vehicles
from parking_spaces import get_parking_spaces
import vehicles

from parking_sessions import get_parking_sessions
from payments import get_total_revenue
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
    QDateEdit,
    QScrollArea,
    QMessageBox
)
from PySide6.QtCore import QDate 

from vehicles import get_vehicles, add_vehicle , delete_vehicle

from parking_spaces import (
    get_parking_spaces,
    add_parking_space,
    update_parking_space
)
from parking_sessions import (
    get_parking_sessions,
    register_vehicle_entry,
    register_vehicle_exit
)
from payments import (
    register_payment,
    get_unpaid_sessions,
    get_payments,
    search_payments,
    get_total_revenue,
    get_daily_revenue,
    get_monthly_revenue
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
        self.sessions_page = self.create_sessions_page()
        self.payments_page = self.create_payments_page()
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.vehicles_page)
        self.pages.addWidget(self.parking_spaces_page)
        self.pages.addWidget(self.sessions_page)
        self.pages.addWidget(self.payments_page)
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
            self.show_dashboard
        )
        vehicles_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )
        parking_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )
        sessions_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )
        payments_button.clicked.connect(
            self.show_payments
        )
        sidebar_layout.addStretch()

        logout_button = QPushButton("Logout")
        logout_button.setFixedHeight(45)
        logout_button.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(logout_button)

        # ================= MAIN WINDOW =================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)
   
    # ================= SHOW DASHBOARD =================
   
    def show_dashboard(self):
        self.refresh_dashboard()
        self.pages.setCurrentIndex(0)

    #===================== SHOW PAYMENTS =================
    
    def show_payments(self):

        self.load_unpaid_sessions()
        self.pages.setCurrentIndex(4)
    
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
        vehicles = get_vehicles()
        parking_spaces = get_parking_spaces()

        total_vehicles = len(vehicles)
        total_parking_spaces = len(parking_spaces)

        available_spaces = sum(
            1 for space in parking_spaces
            if space[3] == "available"
        )

        occupied_spaces = sum(
            1 for space in parking_spaces
            if space[3] == "occupied"
        )
        sessions = get_parking_sessions()

        active_sessions = sum(
            1 for session in sessions
            if session[9] == "active"
        )

        completed_sessions = sum(
            1 for session in sessions
            if session[9] == "completed"
        )

        total_revenue = get_total_revenue()
        

        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        statistics = [
        ("Total Vehicles", str(total_vehicles)),
        ("Total Parking Spaces", str(total_parking_spaces)),
        ("Available Spaces", str(available_spaces)),
        ("Occupied Spaces", str(occupied_spaces)),
        ("Active Sessions", str(active_sessions)),
        ("Completed Sessions", str(completed_sessions)),
        ("Total Revenue", f"{total_revenue:,.2f} SDG")
]

        self.dashboard_labels = {}

        for index, (name, value) in enumerate(statistics):

            card = QFrame()

            card.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
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
            self.dashboard_labels[name] = value_label   
            
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
   
    # ================= REFRESH DASHBOARD =================
   
    def refresh_dashboard(self):

        vehicles = get_vehicles()
        parking_spaces = get_parking_spaces()
        sessions = get_parking_sessions()

        total_vehicles = len(vehicles)
        total_parking_spaces = len(parking_spaces)

        available_spaces = sum(
            1 for space in parking_spaces
            if space[3] == "available"
        )

        occupied_spaces = sum(
            1 for space in parking_spaces
            if space[3] == "occupied"
        )

        active_sessions = sum(
            1 for session in sessions
            if session[9] == "active"
        )

        completed_sessions = sum(
            1 for session in sessions
            if session[9] == "completed"
        )

        total_revenue = get_total_revenue()

        statistics = {
            "Total Vehicles": str(total_vehicles),
            "Total Parking Spaces": str(total_parking_spaces),
            "Available Spaces": str(available_spaces),
            "Occupied Spaces": str(occupied_spaces),
            "Active Sessions": str(active_sessions),
            "Completed Sessions": str(completed_sessions),
            "Total Revenue": f"{total_revenue:,.2f} SDG"
        }

        for name, value in statistics.items():
            self.dashboard_labels[name].setText(value)
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

    
    # ================= PARKING SESSIONS PAGE =================

    def create_sessions_page(self):

        page = QWidget()
        page.setStyleSheet(
            "background-color: #F4F7FB;"
        )

        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        # Page title

        title = QLabel("Parking Sessions Management")

        title.setStyleSheet("""
            color: #14213D;
            font-size: 28px;
            font-weight: bold;
        """)

        description = QLabel(
            "Manage vehicle entry, exit and parking sessions"
        )

        description.setStyleSheet("""
            color: #64748B;
            font-size: 14px;
        """)

        layout.addWidget(title)
        layout.addWidget(description)

        # ================= ENTRY FORM =================

        entry_label = QLabel("Register Vehicle Entry")

        entry_label.setStyleSheet("""
            color: #14213D;
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addWidget(entry_label)

        entry_layout = QHBoxLayout()

        self.entry_vehicle_input = QComboBox()
        self.entry_vehicle_input.setMinimumHeight(40)

        self.entry_space_input = QComboBox()
        self.entry_space_input.setMinimumHeight(40)

        entry_button = QPushButton("Register Entry")
        entry_button.setFixedHeight(40)

        entry_button.setStyleSheet("""
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

        entry_layout.addWidget(self.entry_vehicle_input)
        entry_layout.addWidget(self.entry_space_input)
        entry_layout.addWidget(entry_button)

        layout.addLayout(entry_layout)

        # ================= EXIT FORM =================

        exit_label = QLabel("Register Vehicle Exit")

        exit_label.setStyleSheet("""
            color: #14213D;
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addWidget(exit_label)

        exit_layout = QHBoxLayout()

        self.exit_vehicle_input = QComboBox()
        self.exit_vehicle_input.setMinimumHeight(40)

        exit_button = QPushButton("Register Exit")
        exit_button.setFixedHeight(40)

        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)

        exit_layout.addWidget(self.exit_vehicle_input)
        exit_layout.addWidget(exit_button)

        layout.addLayout(exit_layout)

        # ================= SESSIONS TABLE =================

        self.sessions_table = QTableWidget()

        self.sessions_table.setColumnCount(8)

        self.sessions_table.setHorizontalHeaderLabels([
            "Session ID",
            "Plate Number",
            "Space Number",
            "Entry Time",
            "Exit Time",
            "Duration (Minutes)",
            "Fee (SDG)",
            "Status"
        ])

        self.sessions_table.setStyleSheet("""
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

        self.sessions_table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(self.sessions_table)

        # Connect buttons

        entry_button.clicked.connect(
            self.register_entry_from_ui
        )

        exit_button.clicked.connect(
            self.register_exit_from_ui
        )

        # Load initial data

        self.load_entry_options()
        self.load_exit_options()
        self.load_sessions()

        return page

    # ================= PAYMENTS PAGE =================
    
    def create_payments_page(self):

        page = QWidget()
        page.setStyleSheet("background-color: #F4F7FB;")

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        # Scroll Content
        content = QWidget()

        layout = QVBoxLayout(content)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        title = QLabel("Payments Management")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #14213D;
        """)

        description = QLabel(
            "Manage payments and view revenue reports."
        )
        description.setStyleSheet("""
            font-size: 14px;
            color: #64748B;
        """)

        layout.addWidget(title)
        layout.addWidget(description)
        # Unpaid Sessions Section
        unpaid_title = QLabel("Unpaid Parking Sessions")
        unpaid_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(unpaid_title)
        
        self.unpaid_table = QTableWidget()
        self.unpaid_table.setColumnCount(5)

        self.unpaid_table.setHorizontalHeaderLabels([
            "Session ID",
            "Vehicle ID",
            "Plate Number",
            "Fee",
            "Status"
        ])

        layout.addWidget(self.unpaid_table)

        # Payment Method
        payment_method_title = QLabel("Payment Method")

        payment_method_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(payment_method_title)

        self.payment_method_combo = QComboBox()

        self.payment_method_combo.addItems([
            "cash",
            "card",
            "other"
        ])

        layout.addWidget(self.payment_method_combo)

        # Register Payment Button
        self.register_payment_button = QPushButton("Register Payment")

        self.register_payment_button.setStyleSheet("""
            QPushButton {
                background-color: #14213D;
                color: #FFFFFF;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #243B64;
            }
        """)

        self.register_payment_button.clicked.connect(
            self.register_payment_from_ui
        )

        layout.addWidget(self.register_payment_button)


        # Payment Records Section
        records_title = QLabel("Payment Records")

        records_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(records_title)

        # Payment Search
        search_layout = QHBoxLayout()

        self.payment_search_input = QLineEdit()
        self.payment_search_input.setPlaceholderText(
            "Search by Payment ID or Plate Number..."
        )

        self.payment_search_button = QPushButton("Search")

        search_layout.addWidget(self.payment_search_input)
        search_layout.addWidget(self.payment_search_button)

        layout.addLayout(search_layout)
        self.payment_search_button.clicked.connect(
        self.search_payments_from_ui
        )

        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(7)

        self.payments_table.setHorizontalHeaderLabels([
            "Payment ID",
            "Session ID",
            "Plate Number",
            "Amount",
            "Payment Method",
            "Payment Time",
            "Status"
        ])
        

        layout.addWidget(self.payments_table)

        self.load_payments()
        self.load_unpaid_sessions()

                # Revenue Reports Section
        revenue_title = QLabel("Revenue Reports")

        revenue_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(revenue_title)

        self.total_revenue_label = QLabel("Total Revenue: 0.00 SDG")

        self.total_revenue_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(self.total_revenue_label)
        self.load_total_revenue()

        # Daily Revenue
        daily_title = QLabel("Daily Revenue")

        daily_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(daily_title)

        self.daily_date_input = QDateEdit()
        self.daily_date_input.setCalendarPopup(True)
        self.daily_date_input.setDate(QDate.currentDate())
        self.daily_date_input.setDisplayFormat("yyyy-MM-dd")

        layout.addWidget(self.daily_date_input)

        # Daily Revenue Button
        self.daily_revenue_button = QPushButton("Calculate Daily Revenue")

        layout.addWidget(self.daily_revenue_button)
        
        self.daily_revenue_button.clicked.connect(
        self.calculate_daily_revenue
        )
        # Daily Revenue Result
        self.daily_revenue_label = QLabel(
            "Daily Revenue: 0.00 SDG"
        )

        self.daily_revenue_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(self.daily_revenue_label)
        # Monthly Revenue
        monthly_title = QLabel("Monthly Revenue")

        monthly_title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(monthly_title)
        # Monthly Revenue Button
        self.monthly_revenue_button = QPushButton(
            "Calculate Monthly Revenue"
        )

        layout.addWidget(self.monthly_revenue_button)
        self.monthly_revenue_button.clicked.connect(
        self.calculate_monthly_revenue
        )
        # Monthly Revenue Result
        self.monthly_revenue_label = QLabel(
            "Monthly Revenue: 0.00 SDG"
        )

        self.monthly_revenue_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #14213D;
        """)

        layout.addWidget(self.monthly_revenue_label)
        # Set Scroll Content
        scroll_area.setWidget(content)

        # Main Page Layout
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        page_layout.addWidget(scroll_area)
        return page
  
    # ================= LOAD ENTRY OPTIONS =================
    
    def load_entry_options(self):

        # Load vehicles

        vehicles = get_vehicles()

        self.entry_vehicle_input.clear()

        for vehicle in vehicles:

            vehicle_id = vehicle[0]
            plate_number = vehicle[1]

            self.entry_vehicle_input.addItem(
                plate_number,
                vehicle_id
            )

        # Load available parking spaces

        spaces = get_parking_spaces()

        self.entry_space_input.clear()

        for space in spaces:

            space_id = space[0]
            space_number = space[1]
            status = space[3]

            if status == "available":

                self.entry_space_input.addItem(
                    space_number,
                    space_id
                )

    # ================= LOAD EXIT OPTIONS =================

    def load_exit_options(self):

        sessions = get_parking_sessions()

        self.exit_vehicle_input.clear()

        for session in sessions:

            vehicle_id = session[1]
            plate_number = session[3]
            status = session[9]

            if status == "active":

                self.exit_vehicle_input.addItem(
                    plate_number,
                    vehicle_id
                )

    # ================= LOAD SESSIONS =================

    def load_sessions(self):

        sessions = get_parking_sessions()

        self.sessions_table.setRowCount(0)

        for session in sessions:

            row = self.sessions_table.rowCount()

            self.sessions_table.insertRow(row)

            values = [
                session[0],  # Session ID
                session[3],  # Plate Number
                session[4],  # Space Number
                session[5],  # Entry Time
                session[6],  # Exit Time
                session[7],  # Duration
                session[8],  # Fee
                session[9]   # Status
            ]

            for column, value in enumerate(values):

                display_value = "" if value is None else str(value)

                self.sessions_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(display_value)
                )

    #================== enter 
   
    def register_entry_from_ui(self):
        vehicle_id = self.entry_vehicle_input.currentData()
        space_id = self.entry_space_input.currentData()
        
        if vehicle_id is None or space_id is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a vehicle and a parking space."
            )
            return
        
        session_id = register_vehicle_entry(vehicle_id, space_id)
        
        if session_id is not None:
            QMessageBox.information(
                self,
                "Success",
                "Vehicle entry registered successfully."
            )
            self.load_entry_options()
            self.load_exit_options()
            self.load_sessions()
        else:
            QMessageBox.warning(
                self,
                "Warning",
                "Failed to register vehicle entry."
            )
   
    #================== exit
   
    def register_exit_from_ui(self):
        vehicle_id = self.exit_vehicle_input.currentData()

        if vehicle_id is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select a vehicle."
            )
            return
        fee = register_vehicle_exit(vehicle_id)
        
        if fee is not None:
            QMessageBox.information(
                self,
                "Success",
                f"Vehicle exit registered successfully.\nFee: {fee} SDG"
            )
            self.load_entry_options()
            self.load_exit_options()
            self.load_sessions()
        else:
            QMessageBox.warning(
                self,
                "Warning",
                "Failed to register vehicle exit."
            )
   
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
   
    # ================= LOAD UNPAID SESSIONS =================
    
    def load_unpaid_sessions(self):

        # Get unpaid parking sessions from database
        sessions = get_unpaid_sessions()

        # Set the number of rows
        self.unpaid_table.setRowCount(len(sessions))

        # Fill the table with data
        for row, session in enumerate(sessions):

            self.unpaid_table.setItem(
                row, 0, QTableWidgetItem(str(session[0]))
            )

            self.unpaid_table.setItem(
                row, 1, QTableWidgetItem(str(session[1]))
            )

            self.unpaid_table.setItem(
                row, 2, QTableWidgetItem(str(session[2]))
            )

            self.unpaid_table.setItem(
                row, 3, QTableWidgetItem(str(session[3]))
            )

            self.unpaid_table.setItem(
                row, 4, QTableWidgetItem(str(session[4]))
            )

    #================= LOAD PAYMENTS =================

    def load_payments(self):

        # Get all payment records
        payments = get_payments()

        # Set the number of rows
        self.payments_table.setRowCount(len(payments))

        # Fill the table
        for row, payment in enumerate(payments):

            for column in range(7):
                value = payment[column]

                self.payments_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value))
                )
    
    #================= LOAD TOTAL REVENUE =================

    def load_total_revenue(self):

        # Get total revenue from database
        total_revenue = get_total_revenue()

        # Display total revenue
        self.total_revenue_label.setText(
            f"Total Revenue: {total_revenue:.2f} SDG"
        )
    
    #================= CALCULATE DAILY REVENUE =================

    def calculate_daily_revenue(self):

        # Get selected date
        report_date = self.daily_date_input.date().toString("yyyy-MM-dd")

        # Get daily revenue from database
        daily_revenue = get_daily_revenue(report_date)

        # Display result
        self.daily_revenue_label.setText(
            f"Daily Revenue: {daily_revenue:.2f} SDG"
        )

    #================= CALCULATE MONTHLY REVENUE =================
    def calculate_monthly_revenue(self):

        # Get selected date
        selected_date = self.daily_date_input.date()

        # Extract year and month
        year = selected_date.year()
        month = selected_date.month()

        # Get monthly revenue from database
        monthly_revenue = get_monthly_revenue(year, month)

        # Display result
        self.monthly_revenue_label.setText(
            f"Monthly Revenue: {monthly_revenue:.2f} SDG"
        )

    # ================= REGISTER PAYMENT =================
   
    def register_payment_from_ui(self):

        # Get selected row
        selected_row = self.unpaid_table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(
                self,
                "Warning",
                "Please select an unpaid session."
            )
            return

        # Get session ID
        session_item = self.unpaid_table.item(selected_row, 0)

        if session_item is None:
            QMessageBox.warning(
                self,
                "Warning",
                "Invalid session selection."
            )
            return

        session_id = int(session_item.text())

        # Get payment method
        payment_method = self.payment_method_combo.currentText()

        # Register payment
        payment_id = register_payment(session_id, payment_method)

        if payment_id is None:
            QMessageBox.warning(
                self,
                "Payment Failed",
                "Could not register the payment."
            )
            return

        QMessageBox.information(
            self,
            "Success",
            f"Payment registered successfully.\nPayment ID: {payment_id}"
        )

        # Refresh unpaid sessions
        self.load_unpaid_sessions()

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

    #================= SEARCH PAYMENTS =================

    def search_payments_from_ui(self):

        # Get search value
        search_value = self.payment_search_input.text().strip()

        if not search_value:
            QMessageBox.warning(
                self,
                "Warning",
                "Please enter a Payment ID or Plate Number."
            )
            return

        # Search in database
        payments = search_payments(search_value)

        # Update table
        self.payments_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):

            for column in range(7):

                self.payments_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(payment[column]))
                )

        if not payments:
            QMessageBox.information(
                self,
                "Search Result",
                "No payment records found."
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

    #================== Perform logout actions here ====================
    def handle_logout(self):

        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        from ui.login import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.showMaximized()

        self.close()
    # ================= RUN APPLICATION =================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = DashboardWindow()
    window.showMaximized()

    sys.exit(app.exec())
