import mysql.connector

db = mysql.connector.connect(host = "localhost",user="sree",passwd="sree",database="user")

cur = db.cursor()

cur.execute("select * from tasks")

output = cur.fetchall()

for i in output:
    print(i)

#2021-05-23
# STR_TO_DATE('1-01-2012', '%d-%m-%Y')

'''
{
  "task": "leankloud assignment",
  "dueby": "2021-05-23",
  "status": "In progress"
}


CREATE TABLE `user`.`user` (
  `name` VARCHAR(45) NOT NULL,
  `access` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`name`));


CREATE TABLE `user`.`tasks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `task` VARCHAR(45) NOT NULL,
  `dueby` DATE NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));'''
