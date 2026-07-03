-- =========================================================
-- Mock data: ~50 records total across all tables
-- Assumes the CREATE TABLE statements you provided already ran.
-- IDs are assigned manually since no AUTO_INCREMENT/IDENTITY exists.
-- =========================================================

-- adminTable (1 record)
INSERT INTO adminTable (adminID, businessName, pochiNumber, dateActivated)
VALUES (1, 'Cereal Board PoS', '174379', '2026-01-01');

-- productsTable (8 records, cereals only)
INSERT INTO productsTable (productID, productName, buyingPrice, sellingPrice, profit_margin, currentStock, reorderLevel) VALUES
(1, 'Weetabix 500g', 350, 480, 130, 60, 15),
(2, 'Cornflakes 500g', 300, 420, 120, 55, 15),
(3, 'Oats 1kg', 250, 360, 110, 70, 20),
(4, 'Bran Flakes 500g', 280, 390, 110, 40, 10),
(5, 'Muesli 750g', 420, 580, 160, 30, 10),
(6, 'Rice Krispies 400g', 320, 450, 130, 45, 12),
(7, 'Wheat Biscuits 500g', 310, 430, 120, 50, 12),
(8, 'Coco Pops 400g', 340, 470, 130, 35, 10);

-- customersTable (8 records)
INSERT INTO customersTable (customerID, FirstName, lastName, PhoneNumber, DateRegistered) VALUES
(1, 'Jane', 'Wanjiru', '0712345001', '2026-01-05'),
(2, 'Peter', 'Otieno', '0712345002', '2026-01-06'),
(3, 'Grace', 'Achieng', '0712345003', '2026-01-10'),
(4, 'Samuel', 'Kiprop', '0712345004', '2026-01-12'),
(5, 'Mercy', 'Njeri', '0712345005', '2026-01-15'),
(6, 'Brian', 'Mutua', '0712345006', '2026-01-18'),
(7, 'Faith', 'Chebet', '0712345007', '2026-01-20'),
(8, 'David', 'Omondi', '0712345008', '2026-01-22');

-- salesTable (15 records — 8 MPESA, 7 CASH, respecting the mutual-exclusivity rule manually)
INSERT INTO salesTable (saleID, customer_ID, productID, quantitySold, sale_date, TotalAmount, ISMPESA, transcation_recept, IsCash) VALUES
(1, 1, 1, 2, '2026-05-04', 960,  1, 'QAI100234', 0),
(2, 2, 2, 1, '2026-05-04', 420,  0, NULL,        1),
(3, 3, 3, 3, '2026-05-11', 1080, 1, 'QAI100455', 0),
(4, 4, 4, 2, '2026-05-11', 780,  0, NULL,        1),
(5, 5, 5, 1, '2026-05-18', 580,  1, 'QAI100678', 0),
(6, 6, 6, 4, '2026-05-18', 1800, 0, NULL,        1),
(7, 7, 7, 2, '2026-05-25', 860,  1, 'QAI100890', 0),
(8, 8, 8, 1, '2026-05-25', 470,  0, NULL,        1),
(9, 1, 2, 3, '2026-06-01', 1260, 1, 'QAI101023', 0),
(10, 2, 3, 2, '2026-06-01', 720, 0, NULL,        1),
(11, 3, 4, 1, '2026-06-08', 390, 1, 'QAI101245', 0),
(12, 4, 5, 2, '2026-06-08', 1160,0, NULL,        1),
(13, 5, 6, 3, '2026-06-15', 1350,1, 'QAI101467', 0),
(14, 6, 7, 1, '2026-06-15', 430, 0, NULL,        1),
(15, 7, 8, 2, '2026-06-22', 940, 1, 'QAI101689', 0);

-- MPESATRANSACTION (10 records — 8 matched to the sales above, 2 deliberately unmatched)
INSERT INTO MPESATRANSACTION (transactionID, mpesaReceptNumber, phoneNumber, Amount, transactionDate, saleID, status_of_sale) VALUES
(1, 'QAI100234', '0712345001', 960,  '2026-05-04', 1,  'Matched'),
(2, 'QAI100455', '0712345003', 1080, '2026-05-11', 3,  'Matched'),
(3, 'QAI100678', '0712345005', 580,  '2026-05-18', 5,  'Matched'),
(4, 'QAI100890', '0712345007', 860,  '2026-05-25', 7,  'Matched'),
(5, 'QAI101023', '0712345001', 1260, '2026-06-01', 9,  'Matched'),
(6, 'QAI101245', '0712345003', 390,  '2026-06-08', 11, 'Matched'),
(7, 'QAI101467', '0712345005', 1350, '2026-06-15', 13, 'Matched'),
(8, 'QAI101689', '0712345007', 940,  '2026-06-22', 15, 'Matched'),
(9, 'QAI109981', '0712399999', 650,  '2026-06-25', NULL, 'Unmatched'),
(10,'QAI109982', '0712399998', 410,  '2026-06-26', NULL, 'Unmatched');

-- audtTable (8 records — opening stock movements, one per product)
INSERT INTO audtTable (movementID, productID, changeAmount, Reason, movementDAte) VALUES
(1, 1, 60, 'Restock', '2026-04-01'),
(2, 2, 55, 'Restock', '2026-04-01'),
(3, 3, 70, 'Restock', '2026-04-01'),
(4, 4, 40, 'Restock', '2026-04-01'),
(5, 5, 30, 'Restock', '2026-04-01'),
(6, 6, 45, 'Restock', '2026-04-01'),
(7, 7, 50, 'Restock', '2026-04-01'),
(8, 8, 35, 'Restock', '2026-04-01');