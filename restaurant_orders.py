import tkinter as tk
from tkinter import messagebox, ttk


# ============================================================
# MENU DATA (10 burgers)
# ============================================================

MENU_ITEMS = [
    {"name": "Classic Burger", "icon": "🍔", "price": 18000,
     "description": "Beef patty, lettuce, tomato, onion and pickles."},
    {"name": "Cheese Burger", "icon": "🧀", "price": 20000,
     "description": "Beef patty with double melted cheddar cheese."},
    {"name": "Double Bacon", "icon": "🥓", "price": 28000,
     "description": "Two beef patties, crispy bacon and smoky sauce."},
    {"name": "BBQ Smokehouse", "icon": "🔥", "price": 26000,
     "description": "Grilled beef, onion rings and sweet BBQ sauce."},
    {"name": "Crispy Chicken", "icon": "🍗", "price": 23000,
     "description": "Fried chicken breast, lettuce and garlic mayo."},
    {"name": "Spicy Jalapeño", "icon": "🌶", "price": 25000,
     "description": "Beef patty, jalapeños, pepper jack and hot sauce."},
    {"name": "Mushroom Swiss", "icon": "🍄", "price": 25000,
     "description": "Sautéed mushrooms, Swiss cheese and garlic aioli."},
    {"name": "Veggie Garden", "icon": "🥗", "price": 22000,
     "description": "Plant-based patty, avocado, tomato and fresh greens."},
    {"name": "Hawaiian Burger", "icon": "🍍", "price": 25000,
     "description": "Beef patty, grilled pineapple, ham and teriyaki."},
    {"name": "Monster Triple", "icon": "👑", "price": 35000,
     "description": "Three beef patties, triple cheese, bacon and egg."},
]


def format_price(value):
    """Format a number as Colombian pesos, e.g. 18000 -> $18.000 COP"""
    return f"${value:,.0f}".replace(",", ".") + " COP"


# ============================================================
# DOUBLY LINKED LIST (generic, used for orders and for the menu)
# ============================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.previous = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def add(self, data):
        """Add a new node at the end of the list."""
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1
        return new_node

    def move_next(self):
        if self.current is not None and self.current.next is not None:
            self.current = self.current.next
            return True
        return False

    def move_previous(self):
        if self.current is not None and self.current.previous is not None:
            self.current = self.current.previous
            return True
        return False

    def set_current(self, node):
        if node is not None:
            self.current = node

    def delete_current(self):
        if self.current is None:
            return False

        node = self.current

        # Connect previous node
        if node.previous is not None:
            node.previous.next = node.next
        else:
            self.head = node.next

        # Connect next node
        if node.next is not None:
            node.next.previous = node.previous
        else:
            self.tail = node.previous

        # Select another node
        if node.next is not None:
            self.current = node.next
        elif node.previous is not None:
            self.current = node.previous
        else:
            self.current = None

        self.size -= 1
        return True

    def get_all_nodes(self):
        nodes = []
        node = self.head

        while node is not None:
            nodes.append(node)
            node = node.next

        return nodes

    def get_current_position(self):
        if self.current is None:
            return 0

        position = 1
        node = self.head

        while node is not None:
            if node == self.current:
                return position
            node = node.next
            position += 1

        return 0


class Order:
    def __init__(self, order_id, customer, burger, quantity):
        self.order_id = order_id
        self.customer = customer
        self.burger = burger
        self.quantity = quantity

    @property
    def total(self):
        return self.burger["price"] * self.quantity


# ============================================================
# APPLICATION
# ============================================================

class RestaurantApp:

    VIEW_TITLES = {
        "dashboard": "🏠  Order Management",
        "new_order": "🍔  New Order",
        "orders": "📋  All Orders",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Burger House - Orders")
        self.root.geometry("1150x720")
        self.root.resizable(False, False)

        # Colors
        self.background = "#F5F7FB"
        self.sidebar_color = "#202A44"
        self.sidebar_active = "#2D3857"
        self.primary = "#FF6B35"
        self.primary_dark = "#E85A28"
        self.primary_light = "#FFF0EA"
        self.white = "#FFFFFF"
        self.text_dark = "#202A44"
        self.text_gray = "#7A8194"
        self.border = "#E5E7EF"
        self.green = "#27AE60"
        self.red = "#D64545"

        self.root.configure(bg=self.background)

        # Data structures
        self.order_list = DoublyLinkedList()
        self.menu_list = DoublyLinkedList()
        self.order_counter = 1

        for item in MENU_ITEMS:
            self.menu_list.add(item)

        self.views = {}
        self.nav_buttons = {}
        self.menu_cards = []

        self.create_interface()
        self.update_menu_selection()
        self.update_interface()
        self.show_view("dashboard")

    # ========================================================
    # INTERFACE
    # ========================================================

    def create_interface(self):
        self.create_sidebar()

        self.main = tk.Frame(self.root, bg=self.background)
        self.main.pack(side="left", fill="both", expand=True)

        # Header
        header = tk.Frame(self.main, bg=self.background)
        header.pack(fill="x", padx=35, pady=(25, 5))

        self.title_label = tk.Label(
            header, text="", font=("Arial", 24, "bold"),
            bg=self.background, fg=self.text_dark
        )
        self.title_label.pack(side="left")

        self.order_counter_label = tk.Label(
            header, text="🧾 0 orders", font=("Arial", 10, "bold"),
            bg=self.primary_light, fg=self.primary, padx=12, pady=6
        )
        self.order_counter_label.pack(side="right")

        # Container for the three views
        self.container = tk.Frame(self.main, bg=self.background)
        self.container.pack(fill="both", expand=True)

        self.views["dashboard"] = self.build_dashboard_view()
        self.views["new_order"] = self.build_new_order_view()
        self.views["orders"] = self.build_orders_view()

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        logo_frame.pack(pady=(35, 35))

        tk.Label(
            logo_frame, text="🍔🍟🥤", font=("Arial", 26),
            bg=self.sidebar_color, fg=self.white
        ).pack()

        tk.Label(
            logo_frame, text="BURGER HOUSE", font=("Arial", 16, "bold"),
            bg=self.sidebar_color, fg=self.white
        ).pack(pady=(5, 0))

        tk.Label(
            logo_frame, text="FAST FOOD ORDER SYSTEM", font=("Arial", 8),
            bg=self.sidebar_color, fg="#AEB6CC"
        ).pack()

        self.create_menu_button("dashboard", "🏠   Dashboard")
        self.create_menu_button("new_order", "➕   New Order")
        self.create_menu_button("orders", "📋   All Orders")

        # Bottom status
        status_frame = tk.Frame(self.sidebar, bg="#182137")
        status_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        tk.Label(
            status_frame, text="●", font=("Arial", 14),
            bg="#182137", fg=self.green
        ).pack(side="left", padx=(10, 5), pady=12)

        tk.Label(
            status_frame, text="Jair_restaurant", font=("Arial", 9, "bold"),
            bg="#182137", fg=self.white
        ).pack(side="left")

    def create_menu_button(self, view_name, text):
        button = tk.Button(
            self.sidebar, text=text, font=("Arial", 11, "bold"),
            bg=self.sidebar_color, fg="#DDE2F0",
            activebackground=self.sidebar_active, activeforeground=self.white,
            relief="flat", anchor="w", padx=25, height=2, cursor="hand2",
            command=lambda: self.open_view(view_name)
        )
        button.pack(fill="x", pady=2)
        self.nav_buttons[view_name] = button

    # --------------------------------------------------------
    # DASHBOARD VIEW
    # --------------------------------------------------------

    def build_dashboard_view(self):
        view = tk.Frame(self.container, bg=self.background)

        # Statistics
        stats = tk.Frame(view, bg=self.background)
        stats.pack(fill="x", padx=35, pady=(10, 5))

        self.stat_orders = self.create_stat_card(stats, "🧾", "Orders")
        self.stat_burgers = self.create_stat_card(stats, "🛍", "Items sold")
        self.stat_sales = self.create_stat_card(stats, "💰", "Total sales")

        # Current order card
        card = tk.Frame(
            view, bg=self.white,
            highlightbackground=self.border, highlightthickness=1
        )
        card.pack(fill="x", padx=35, pady=15)

        card_header = tk.Frame(card, bg=self.white)
        card_header.pack(fill="x", padx=30, pady=(20, 5))

        tk.Label(
            card_header, text="CURRENT ORDER", font=("Arial", 10, "bold"),
            bg=self.white, fg=self.text_gray
        ).pack(side="left")

        self.position_label = tk.Label(
            card_header, text="Order 0 of 0", font=("Arial", 10),
            bg=self.white, fg=self.text_gray
        )
        self.position_label.pack(side="right")

        self.order_number_label = tk.Label(
            card, text="No orders yet", font=("Arial", 24, "bold"),
            bg=self.white, fg=self.text_dark
        )
        self.order_number_label.pack(pady=(5, 2))

        self.customer_label = tk.Label(
            card, text="", font=("Arial", 12),
            bg=self.white, fg=self.text_gray
        )
        self.customer_label.pack(pady=2)

        self.product_label = tk.Label(
            card, text="", font=("Arial", 18, "bold"),
            bg=self.white, fg=self.primary
        )
        self.product_label.pack(pady=(5, 2))

        self.total_label = tk.Label(
            card, text="", font=("Arial", 12, "bold"),
            bg=self.white, fg=self.green
        )
        self.total_label.pack(pady=(0, 10))

        navigation = tk.Frame(card, bg=self.white)
        navigation.pack(pady=(5, 25))

        self.previous_button = tk.Button(
            navigation, text="◀  Previous", font=("Arial", 10, "bold"),
            width=15, height=2, bg="#EEF1F7", fg=self.text_dark,
            activebackground="#E1E5EE", relief="flat", cursor="hand2",
            command=self.previous_order
        )
        self.previous_button.pack(side="left", padx=10)

        self.next_button = tk.Button(
            navigation, text="Next  ▶", font=("Arial", 10, "bold"),
            width=15, height=2, bg=self.primary, fg=self.white,
            activebackground=self.primary_dark, activeforeground=self.white,
            relief="flat", cursor="hand2", command=self.next_order
        )
        self.next_button.pack(side="left", padx=10)

        # Bottom buttons
        actions = tk.Frame(view, bg=self.background)
        actions.pack(fill="x", padx=35)

        tk.Button(
            actions, text="🍟  Take a New Order", font=("Arial", 10, "bold"),
            bg=self.primary, fg=self.white,
            activebackground=self.primary_dark, activeforeground=self.white,
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=lambda: self.open_view("new_order")
        ).pack(side="left")

        tk.Button(
            actions, text="🗑  Delete Current Order", font=("Arial", 10, "bold"),
            bg=self.background, fg=self.red,
            activebackground=self.background, activeforeground=self.red,
            relief="flat", cursor="hand2", command=self.delete_order
        ).pack(side="right")

        return view

    def create_stat_card(self, parent, icon, caption):
        card = tk.Frame(
            parent, bg=self.white,
            highlightbackground=self.border, highlightthickness=1
        )
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))

        tk.Label(
            card, text=icon, font=("Arial", 22),
            bg=self.white
        ).pack(side="left", padx=(18, 10), pady=12)

        info = tk.Frame(card, bg=self.white)
        info.pack(side="left", pady=12)

        value = tk.Label(
            info, text="0", font=("Arial", 16, "bold"),
            bg=self.white, fg=self.text_dark
        )
        value.pack(anchor="w")

        tk.Label(
            info, text=caption, font=("Arial", 9),
            bg=self.white, fg=self.text_gray
        ).pack(anchor="w")

        return value

    # --------------------------------------------------------
    # NEW ORDER VIEW (menu + form)
    # --------------------------------------------------------

    def build_new_order_view(self):
        view = tk.Frame(self.container, bg=self.background)

        tk.Label(
            view, text="Choose a burger from our menu 👇",
            font=("Arial", 13, "bold"), bg=self.background, fg=self.text_dark
        ).pack(anchor="w", padx=35, pady=(8, 8))

        # Menu grid: 5 columns x 2 rows, one card per burger
        grid = tk.Frame(view, bg=self.background)
        grid.pack(padx=35, anchor="w")

        for index, node in enumerate(self.menu_list.get_all_nodes()):
            burger = node.data

            card = tk.Frame(
                grid, bg=self.white, width=156, height=112,
                highlightbackground=self.border, highlightthickness=2,
                cursor="hand2"
            )
            card.grid(row=index // 5, column=index % 5, padx=(0, 8), pady=(0, 8))
            card.pack_propagate(False)

            icon = tk.Label(card, text=burger["icon"], font=("Arial", 26), bg=self.white)
            icon.pack(pady=(10, 0))

            name = tk.Label(
                card, text=burger["name"], font=("Arial", 9, "bold"),
                bg=self.white, fg=self.text_dark
            )
            name.pack()

            price = tk.Label(
                card, text=format_price(burger['price']), font=("Arial", 10, "bold"),
                bg=self.white, fg=self.primary
            )
            price.pack()

            labels = [icon, name, price]

            for widget in [card] + labels:
                widget.bind("<Button-1>", lambda event, n=node: self.select_burger(n))
                widget.configure(cursor="hand2")

            self.menu_cards.append((node, card, labels))

        # Selection + order form
        form = tk.Frame(
            view, bg=self.white,
            highlightbackground=self.border, highlightthickness=1
        )
        form.pack(fill="x", padx=35, pady=(6, 0))

        # Selected burger (top part)
        selected = tk.Frame(form, bg=self.white)
        selected.pack(fill="x", padx=25, pady=(15, 5))

        self.menu_previous_button = tk.Button(
            selected, text="◀", font=("Arial", 12, "bold"), width=3,
            bg="#EEF1F7", fg=self.text_dark, activebackground="#E1E5EE",
            relief="flat", cursor="hand2", command=self.previous_burger
        )
        self.menu_previous_button.pack(side="left")

        self.selected_icon = tk.Label(
            selected, text="🍔", font=("Arial", 32), bg=self.white
        )
        self.selected_icon.pack(side="left", padx=15)

        info = tk.Frame(selected, bg=self.white)
        info.pack(side="left")

        self.selected_name = tk.Label(
            info, text="", font=("Arial", 14, "bold"),
            bg=self.white, fg=self.text_dark
        )
        self.selected_name.pack(anchor="w")

        self.selected_description = tk.Label(
            info, text="", font=("Arial", 10),
            bg=self.white, fg=self.text_gray
        )
        self.selected_description.pack(anchor="w")

        self.menu_next_button = tk.Button(
            selected, text="▶", font=("Arial", 12, "bold"), width=3,
            bg=self.primary, fg=self.white,
            activebackground=self.primary_dark, activeforeground=self.white,
            relief="flat", cursor="hand2", command=self.next_burger
        )
        self.menu_next_button.pack(side="right")

        self.selected_price = tk.Label(
            selected, text="", font=("Arial", 16, "bold"),
            bg=self.white, fg=self.primary
        )
        self.selected_price.pack(side="right", padx=20)

        tk.Frame(form, bg=self.border, height=1).pack(fill="x", padx=25, pady=8)

        # Customer data (bottom part)
        fields = tk.Frame(form, bg=self.white)
        fields.pack(fill="x", padx=25, pady=(0, 15))

        tk.Label(
            fields, text="👤  Customer name", font=("Arial", 9, "bold"),
            bg=self.white, fg=self.text_gray
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            fields, text="🔢  Quantity", font=("Arial", 9, "bold"),
            bg=self.white, fg=self.text_gray
        ).grid(row=0, column=1, sticky="w", padx=(20, 0))

        self.customer_entry = tk.Entry(
            fields, font=("Arial", 11), width=32, relief="flat", bg="#F4F6FA"
        )
        self.customer_entry.grid(row=1, column=0, ipady=8, pady=(4, 0))
        self.customer_entry.bind("<Return>", lambda event: self.add_order())

        self.quantity_spinbox = tk.Spinbox(
            fields, from_=1, to=20, width=5, font=("Arial", 12),
            relief="flat", bg="#F4F6FA", justify="center"
        )
        self.quantity_spinbox.grid(row=1, column=1, ipady=7, padx=(20, 0), pady=(4, 0))

        tk.Button(
            fields, text="+  Add Order", font=("Arial", 10, "bold"),
            width=17, height=2, bg=self.primary, fg=self.white,
            activebackground=self.primary_dark, activeforeground=self.white,
            relief="flat", cursor="hand2", command=self.add_order
        ).grid(row=0, column=2, rowspan=2, padx=(25, 0))

        return view

    # --------------------------------------------------------
    # ALL ORDERS VIEW
    # --------------------------------------------------------

    def build_orders_view(self):
        view = tk.Frame(self.container, bg=self.background)

        style = ttk.Style()
        style.configure("Orders.Treeview", rowheight=34, font=("Arial", 11))
        style.configure("Orders.Treeview.Heading", font=("Arial", 10, "bold"))

        table_frame = tk.Frame(
            view, bg=self.white,
            highlightbackground=self.border, highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True, padx=35, pady=(10, 10))

        columns = ("order", "customer", "burger", "quantity", "total")

        self.orders_table = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            style="Orders.Treeview", selectmode="browse"
        )

        headings = {
            "order": ("🧾 Order", 90),
            "customer": ("👤 Customer", 200),
            "burger": ("🍔 Burger", 250),
            "quantity": ("🔢 Qty", 70),
            "total": ("💵 Total", 110),
        }

        for column, (text, width) in headings.items():
            self.orders_table.heading(column, text=text)
            self.orders_table.column(column, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.orders_table.yview
        )
        self.orders_table.configure(yscrollcommand=scrollbar.set)

        self.orders_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.orders_table.bind("<Double-1>", lambda event: self.open_selected_order())

        actions = tk.Frame(view, bg=self.background)
        actions.pack(fill="x", padx=35, pady=(0, 15))

        tk.Button(
            actions, text="👁  Open Selected Order", font=("Arial", 10, "bold"),
            bg=self.primary, fg=self.white,
            activebackground=self.primary_dark, activeforeground=self.white,
            relief="flat", cursor="hand2", padx=15, pady=8,
            command=self.open_selected_order
        ).pack(side="left")

        tk.Button(
            actions, text="🗑  Delete Selected Order", font=("Arial", 10, "bold"),
            bg=self.background, fg=self.red,
            activebackground=self.background, activeforeground=self.red,
            relief="flat", cursor="hand2", command=self.delete_selected_order
        ).pack(side="right")

        return view

    # ========================================================
    # NAVIGATION BETWEEN VIEWS
    # ========================================================

    def show_view(self, view_name):
        for view in self.views.values():
            view.pack_forget()

        self.views[view_name].pack(fill="both", expand=True)
        self.title_label.config(text=self.VIEW_TITLES[view_name])

        for name, button in self.nav_buttons.items():
            button.config(
                bg=self.sidebar_active if name == view_name else self.sidebar_color
            )

    def open_view(self, view_name):
        self.show_view(view_name)

        if view_name == "new_order":
            self.customer_entry.focus()

    # ========================================================
    # MENU (doubly linked list navigation)
    # ========================================================

    def select_burger(self, node):
        self.menu_list.set_current(node)
        self.update_menu_selection()

    def next_burger(self):
        if not self.menu_list.move_next():
            messagebox.showinfo("Menu", "That is the last burger on the menu.")
        self.update_menu_selection()

    def previous_burger(self):
        if not self.menu_list.move_previous():
            messagebox.showinfo("Menu", "That is the first burger on the menu.")
        self.update_menu_selection()

    def update_menu_selection(self):
        burger = self.menu_list.current.data

        self.selected_icon.config(text=burger["icon"])
        self.selected_name.config(text=burger["name"])
        self.selected_description.config(text=burger["description"])
        self.selected_price.config(text=format_price(burger['price']))

        for node, card, labels in self.menu_cards:
            is_selected = node is self.menu_list.current
            bg = self.primary_light if is_selected else self.white

            card.config(
                bg=bg,
                highlightbackground=self.primary if is_selected else self.border
            )

            for label in labels:
                label.config(bg=bg)

    # ========================================================
    # ORDER ACTIONS
    # ========================================================

    def add_order(self):
        customer = self.customer_entry.get().strip()

        if customer == "":
            messagebox.showwarning(
                "Missing information",
                "Please enter the customer name."
            )
            self.customer_entry.focus()
            return

        try:
            quantity = int(self.quantity_spinbox.get())
            if quantity < 1 or quantity > 20:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid quantity",
                "Quantity must be a whole number between 1 and 20."
            )
            return

        burger = self.menu_list.current.data

        order = Order(self.order_counter, customer, burger, quantity)
        node = self.order_list.add(order)
        self.order_list.set_current(node)

        self.order_counter += 1

        self.customer_entry.delete(0, tk.END)
        self.quantity_spinbox.delete(0, tk.END)
        self.quantity_spinbox.insert(0, "1")

        self.update_interface()

        messagebox.showinfo(
            "Order added",
            f"Order #{order.order_id:03d} added:\n"
            f"{quantity} x {burger['name']} {burger['icon']}\n"
            f"Total: {format_price(order.total)}"
        )

    def next_order(self):
        if not self.order_list.move_next():
            messagebox.showinfo("Navigation", "There is no next order.")

        self.update_interface()

    def previous_order(self):
        if not self.order_list.move_previous():
            messagebox.showinfo("Navigation", "There is no previous order.")

        self.update_interface()

    def delete_order(self):
        if self.order_list.current is None:
            messagebox.showwarning("Delete Order", "There is no order to delete.")
            return

        order = self.order_list.current.data

        if messagebox.askyesno("Delete Order", f"Delete Order #{order.order_id:03d}?"):
            self.order_list.delete_current()
            self.update_interface()

    def get_selected_node(self):
        selection = self.orders_table.selection()

        if not selection:
            messagebox.showwarning("All Orders", "Please select an order from the list.")
            return None

        order_id = int(selection[0])

        for node in self.order_list.get_all_nodes():
            if node.data.order_id == order_id:
                return node

        return None

    def open_selected_order(self):
        node = self.get_selected_node()

        if node is not None:
            self.order_list.set_current(node)
            self.update_interface()
            self.show_view("dashboard")

    def delete_selected_order(self):
        node = self.get_selected_node()

        if node is not None:
            self.order_list.set_current(node)
            self.delete_order()

    # ========================================================
    # UPDATE INTERFACE
    # ========================================================

    def update_interface(self):
        total = self.order_list.size
        orders = [node.data for node in self.order_list.get_all_nodes()]

        # Header and statistics
        self.order_counter_label.config(text=f"🧾 {total} orders")
        self.stat_orders.config(text=str(total))
        self.stat_burgers.config(text=str(sum(o.quantity for o in orders)))
        self.stat_sales.config(text=format_price(sum(o.total for o in orders)))

        # Current order card
        position = self.order_list.get_current_position()
        self.position_label.config(text=f"Order {position} of {total}")

        current = self.order_list.current

        if current is None:
            self.order_number_label.config(text="No orders yet")
            self.customer_label.config(text="Create an order to get started")
            self.product_label.config(text="🍔🍟🥤")
            self.total_label.config(text="")
        else:
            order = current.data
            self.order_number_label.config(text=f"ORDER #{order.order_id:03d}")
            self.customer_label.config(text=f"👤  Customer: {order.customer}")
            self.product_label.config(
                text=f"{order.burger['icon']}  {order.quantity} x {order.burger['name']}"
            )
            self.total_label.config(text=f"💵  Total: {format_price(order.total)}")

        # Orders table
        self.orders_table.delete(*self.orders_table.get_children())

        for order in orders:
            self.orders_table.insert(
                "", "end", iid=str(order.order_id),
                values=(
                    f"#{order.order_id:03d}",
                    order.customer,
                    f"{order.burger['icon']} {order.burger['name']}",
                    order.quantity,
                    format_price(order.total),
                )
            )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()