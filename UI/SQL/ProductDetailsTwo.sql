CREATE TABLE Products (
    `Product ID` INT AUTO_INCREMENT PRIMARY KEY,
    `Name` VARCHAR(40),
    `Date` DATE,
    `ImagePath` VARCHAR(255),
    `ImagePath1` VARCHAR(255),
    `ImagePath2` VARCHAR(255),
    `ImagePath3` VARCHAR(255),
    `origin` VARCHAR(50)
);

CREATE TABLE PricingDetails (
  `Product ID` INT NOT NULL,
  `Title` VARCHAR(255) NOT NULL,
  `Highest Price` VARCHAR(20) NOT NULL,
  `Date of Highest Price` VARCHAR(100) NOT NULL,
  `Lowest Price` VARCHAR(20) NOT NULL,
  `Date of Lowest Price` VARCHAR(100) NOT NULL,
  `Average Price` VARCHAR(20) NOT NULL,
  `Date of Average Price` VARCHAR(100) NOT NULL,
  `Current Price` VARCHAR(20) NOT NULL,
  `Label Price` VARCHAR(20) NOT NULL,
  `Savings` VARCHAR(20) NOT NULL,
  `Discount` VARCHAR(30) NOT NULL,
  `Suggestion` VARCHAR(255) NOT NULL,
  `Status` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`Product ID`),
  FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Product ID`) ON DELETE CASCADE
);

CREATE TABLE ReviewClassifier (
  `Product ID` INT NOT NULL,
  `CNN Positive` INT NOT NULL,
  `CNN Negative` INT NOT NULL,
  `LSTM Positive` INT NOT NULL,
  `LSTM Negative` INT NOT NULL,
  `Transformer Positive` INT NOT NULL,
  `Transformer Negative` INT NOT NULL,
  `Total Number of Reviews` INT NOT NULL,
  `Total number of Reviews Present in Web` INT NOT NULL,
  PRIMARY KEY (`Product ID`),
  FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Product ID`) ON DELETE CASCADE
);

CREATE TABLE ReviewSummary (
  `Product ID` INT NOT NULL,
  `Extractive Positive Summary` TEXT NOT NULL,
  `Extractive Negative Summary` TEXT NOT NULL,
  `Abstractive Positive Summary` TEXT NOT NULL,
  `Abstractive Negative Summary` TEXT NOT NULL,
  `Product detail` TEXT NOT NULL,
  PRIMARY KEY (`Product ID`),
  FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Product ID`) ON DELETE CASCADE
);

CREATE TABLE AmazonSummary (
  `Product ID` INT NOT NULL,
  `Amazon Summary` TEXT NOT NULL,
  PRIMARY KEY (`Product ID`),
  FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Product ID`) ON DELETE CASCADE
);

CREATE TABLE imageDirs (
  `Product ID` INT NOT NULL,
  `imagePath1` VARCHAR(255),
  `imagePath2` VARCHAR(255),
  `imagePath3` VARCHAR(255),
  `imagePath4` VARCHAR(255),
  PRIMARY KEY (`Product ID`),
  FOREIGN KEY (`Product ID`) REFERENCES `Products` (`Product ID`) ON DELETE CASCADE
);
