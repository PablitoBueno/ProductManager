# Professional Product Management System

## Description

This project is a **Professional Product Management System** developed in Python using the Tkinter library for the graphical user interface (GUI). This system was created as a learning endeavor to deepen my understanding of Python programming, GUI development, and data management practices. Through this project, I aimed to apply theoretical knowledge in a practical context while addressing real-world inventory management challenges.

The system is designed to provide a comprehensive solution for adding, listing, and monitoring products in inventory, making it suitable for use in commercial environments. While it demonstrates core functionalities typical of a product management application, it's important to acknowledge the limitations inherent in its current implementation, including potential scalability issues and the need for enhanced error handling.

## Features

- **Add Products**: Users can input new product information through a user-friendly form. This includes essential details such as:
  - **Code**: A unique identifier for each product.
  - **Name**: The name of the product.
  - **Quantity**: The number of items currently in stock.
  - **Value**: The price of the product.
  - **Description**: A brief overview of the product.
  - **Category**: The category under which the product is classified.
  - **Minimum Stock Level**: A threshold that triggers alerts when stock is low.

- **List Products**: The system displays a comprehensive table of all registered products, allowing users to view and sort product information quickly. The table includes columns for each of the product attributes, making it easy to compare different products.

- **Low Stock Alert**: This feature monitors stock levels and provides notifications for products that fall below their minimum stock threshold. This helps prevent stockouts and ensures that users can take timely action to replenish inventory.

- **Export to Excel**: Users can generate well-structured Excel reports that include all product information. This functionality facilitates easy sharing and analysis of data, providing a professional format suitable for business use.

- **Quantity by Category Charts**: The system visually represents the distribution of products across categories using bar charts. This feature allows users to quickly assess inventory levels by category, aiding in strategic decision-making.

## Limitations

While the **Professional Product Management System** serves its intended purpose, it has several limitations:
- **Scalability**: The current implementation is suitable for small to medium-sized inventories. For larger inventories, enhancements may be required to ensure optimal performance.
- **Error Handling**: The system lacks comprehensive error handling, which may lead to unexpected behaviors if users enter invalid data.
- **User Authentication**: The application does not currently include user authentication or authorization features, which would be necessary for multi-user environments.

This project represents an important step in my journey of learning Python and software development, providing practical experience in building a functional application while highlighting areas for future improvement.
