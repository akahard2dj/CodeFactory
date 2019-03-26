password changes

UPDATE user SET password=PASSWORD('passphrase') where user='USER';
FLUSH PRIVILEGES;

granting

GRANT ALL PRIVILEGES ON db.* to 'USER'@'%';
