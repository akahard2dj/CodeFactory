create table pricehistory(
id int not null auto_increment,
tradePrice char(10),
tradeYear char(5),
c3NameKR char(12),
c4NameKR char(100),
tradeMonth char(3),
tradePeriod char(6),
tradeArea char(10),
address char(10),
tradeFloor char(3),
c4Code char(10),
primary key(id));
