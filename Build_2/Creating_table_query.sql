drop database if exists DUKAAN;
create database DUKAAN;
use DUKAAN;

drop table if exists User;
 drop table if exists User_PhoneNumber;
 drop table if exists cart_entity;
 drop table if exists shop;
 drop table if exists shop_PhoneNumber;
 drop table if exists product_entity; 
drop table if exists container_relation;
drop table if exists dispatching_unit_PhoneNumber;
drop table if exists Delivery_unit_entity;
drop table if exists order_relation;
drop table if exists Transaction_entity;
drop table if exists delivery_unit_relation;
drop table if exists order_detail;


create table User
(user_id INT NOT NULL AUTO_INCREMENT,
username varchar(30) NOT NULL ,
password varchar(8) NOT NULL,
House_NO INT NOT NULL,
area varchar(20) NOT NULL,
state varchar(20) NOT NULL,
PINCODE INT(6) NOT NULL,
WALLET DOUBLE(16,2) DEFAULT '0.00',
DOB DATE NOT NULL,
age int default "0" not null,
primary key(user_id),
UNIQUE INDEX `user_id_UNIQUE` (user_id ASC) ,
UNIQUE INDEX `Username_UNIQUE` (username ASC) 
);

create table User_PhoneNumber(
user_id INT NOT NULL ,
phone_number VARCHAR(10) NOT NULL,
primary Key(user_id,phone_number),
unique(phone_number),
foreign key (user_id) references User(user_id),
INDEX `user_id_index` (user_id ASC) 
);

create table cart_entity(
super_user_id INT NOT NULL,
T_Price Double(16,2) DEFAULT '0.00',
primary key(super_user_id),
foreign key (super_user_id) references user(user_id),
UNIQUE INDEX `super_user_id_UNIQUE` (super_user_id ASC));
 
create table shop
(shop_id INT NOT NULL AUTO_INCREMENT,
shopname varchar(30) NOT NULL ,
password varchar(8) NOT NULL,
shop_no INT NOT NULL,
area varchar(20) NOT NULL,
state varchar(20) NOT NULL,
PINCODE INT(6) NOT NULL,
primary key(shop_id),
UNIQUE INDEX `shop_id_UNIQUE` (shop_id ASC),
UNIQUE INDEX `shopname_UNIQUE` (shopname ASC)  );

create table shop_PhoneNumber(
shop_id INT NOT NULL,
phone_number VARCHAR(10) NOT NULL,
primary Key(shop_id,phone_number),
unique(phone_number),
foreign key (shop_id) references shop(shop_id),
INDEX `shop_id_index` (shop_id ASC) 
);
 create table product_entity(
P_id INT NOT NULL auto_increment,
P_name varchar(30) NOT NULL,
Categories varchar(30) NOT NULL,
Price Double(16,2) NOT NULL,
Quantity INT Default 0,
shop_id int not null,
primary Key(P_id),
foreign key (shop_id) references shop(shop_id),
UNIQUE INDEX `P_id_UNIQUE` (P_id ASC),
INDEX `P_name_UNIQUE` (P_name ASC),
INDEX `shop_id_UNIQUE` (shop_id ASC)
);

create table container_relation(
super_user_id INT NOT NULL,
P_ID INT NOT NULL,
Product_quantity INT NOT NULL,
primary key(super_user_id,P_ID),
foreign Key(super_user_id) references cart_entity(super_user_id),
foreign Key(P_ID) references product_entity(P_id),
INDEX `super_user_id_UNIQUE` (super_user_id ASC),
INDEX `P_id_UNIQUE` (P_ID ASC)
);


create table Transaction_entity(
Transcation_id INT NOT NULL auto_increment,
T_Amount Double(16,2) NOT NULL,
T_quantity INT(16) default 0 NOT NULL,
Super_User_Id INT NOT NULL,
primary key(Transcation_id),
foreign key (Super_User_Id) references cart_entity(super_user_id),
UNIQUE INDEX `Transcation_id_UNIQUE` (Transcation_id ASC),
INDEX `super_user_id_UNIQUE` (super_user_id ASC));

create table Delivery_unit_entity(
Shop_id int not null,
License_id int not null,
unit_name varchar(20) not null,
password varchar(10) not null,
primary key(Shop_id,License_id),
foreign Key (Shop_id) references shop(shop_id),
UNIQUE INDEX `shop_id_UNIQUE` (shop_id ASC),
UNIQUE INDEX `License_id_UNIQUE` (License_id ASC));

create table dispatching_unit_PhoneNumber(
License_id INT NOT NULL,
phone_number  VARCHAR(10) NOT NULL,
primary Key(License_id,phone_number),
unique(phone_number),
foreign key (License_id) references Delivery_unit_entity(License_id),
INDEX `License_id_index` (License_id ASC) 
);
create table order_relation(
transaction_id int not null,
shop_id int not null,
primary key(transaction_id,shop_id),
foreign key (transaction_id) references Transaction_entity(Transcation_id),
foreign key (shop_id) references shop(shop_id),
INDEX `shop_id_UNIQUE` (shop_id ASC),
 INDEX `Transcation_id_UNIQUE` (transaction_id ASC));
 
 create view shows as
 select p_id,p_name from product;
 
 
 create view soo as
 select order_id,order_name from order_detail;
 

 
 create table delivery_unit_relation(
 shop_id int not null,
 license_id int not null,
 super_user_id int not null,
 order_id int not null auto_increment,
 primary key(shop_id,license_id ,super_user_id,order_id),
 foreign key (license_id) references Delivery_unit_entity(License_id),
foreign Key (Shop_id) references shop(shop_id),
foreign Key(super_user_id) references user(user_id),
INDEX `shop_id` (shop_id ASC),
INDEX `License_id` (License_id ASC),
INDEX `super_user_id` (super_user_id ASC),
Unique INDEX `order_id_UNIQUE` (order_id ASC));

create table order_detail(
order_id int not null,
order_name varchar(30) not null,
order_status varchar(20) not null default "on the way",
quantity int not null,
Price decimal(10,2) not null,
date_of_order date not null,
date_of_delivery date  not null,
foreign key (order_id) references Delivery_unit_relation(order_id),
primary key(order_id,order_name),
INDEX `order_id` (order_id ASC),
INDEX `order_name` (order_name ASC));

 create view usr as
 select user_name,user_id,wallet from user;
 
delimiter //
create trigger Price_verify
before insert on product_entity
for each row 
if new.Price <= 0 then set new.Price = 0;
end if; //

delimiter //
 create trigger upd_cart
 before update on  cart_entity
 for each row
 begin
 if new.T_Price is null then 
 set new.T_Price = 0.00;
 end if; 
 end//
 delimiter ;


ALTER TABLE shop
ADD Account DOUBLE(16,2) DEFAULT '0.00';


show tables;
