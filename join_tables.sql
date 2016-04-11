SELECT Customers.CustomerName
FROM Products
	JOIN OrderDetails
		ON OrderDetails.ProductID = Products.ProductID
	JOIN Orders
		ON Orders.OrderID = OrderDetails.OrderID
	JOIN Customers
		ON Customers.CustomerID = Orders.CustomerID

WHERE ProductName = 'Gorgonzola Telino';
