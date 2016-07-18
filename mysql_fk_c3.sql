create table c3(
c2_index int,
c3_index int NOT NULL AUTO_INCREMENT PRIMARY KEY,
c3Code char(10),
c3NameKR char(12),
c3CoordX float(9,6),
c3CoordY float(9,6),
c3TotalCounts int,
timestamp char(10),
index idx_c2_index(c2_index),
foreign key(c2_index) references c2(c2_index) on delete set null)engine=innodb;
