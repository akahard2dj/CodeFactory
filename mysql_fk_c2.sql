create table c2(
c1_index int,
c2_index int NOT NULL AUTO_INCREMENT PRIMARY KEY,
c2Code char(10),
c2NameKR char(12),
c2CoordX float(9,6),
c2CoordY float(9,6),
timestamp char(10),
index idx_c2_index(c2_index),
foreign key(c1_index) references c1(c1_index) on delete set null)engine=innodb;
