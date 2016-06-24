create table c4List(
id int not null auto_increment,
timestamp char(10),
c4Code char(10),
c4SellingType char(10)
c4SellingDate char(20)
c4SellingStatus char(10)
c4SellingStatusCaption varchar(1024)
c4SellingDetailLink varchar(1024)
c4SellingAreaType char(20) 
c4SellingSupplyArea char(20)
c4SellingNetArea char(20)
c4SellingComplex char(10)
c4SellingFloor char(10)
c4SellingTotalFloor char(5)
c4SellingPrice char(25)
c4SellingAgentName varchar(200)
c4SellingAgentTel char(50)
c4SellingAgentCode char(20)
c4SellingAgentComment varchar(1024)
c4SellingSource char(50)
c4SellingSourceLink varchar(1024)
c4SellingClass char(20),
primary key(id));
