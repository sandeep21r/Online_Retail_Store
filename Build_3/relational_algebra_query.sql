use dukaan;

-- 1) 
update user
set wallet = 1000000;

-- 2)
select * from cart_entity;
update cart_entity
set T_price = (select sum(product_quantity*price) from container_relation ,product_entity where container_relation.p_id=product_entity.p_id and super_user_id = cart_entity.super_user_id group by container_relation.super_user_id);

 update cart_entity
set t_price =0.00
where t_price is null;
    
select * from cart_entity;


-- 3) 
insert into transaction_entity values(121,0,0,2);   


UPDATE transaction_entity
SET T_quantity = 3,
t_amount = (select 3*price from container_relation,product_entity 
where container_relation.p_id=product_entity.p_id and super_user_id = 2 and container_relation.p_id = 54)
WHERE 
    transaction_entity.Transcation_id = 121 
    AND transaction_entity.super_user_id = 2 
    AND 3 <= (
        SELECT product_quantity 
        FROM container_relation 
      WHERE super_user_id = 2 AND container_relation.p_id = 54
    );

-- 4)

update product_entity
set Quantity = Quantity-3
 where product_entity.p_id = 54;

update container_relation
set product_quantity = product_quantity -3
where p_id = 54 and super_user_id = 2;

update cart_entity
 set T_price = (select sum(product_quantity*price) from container_relation ,product_entity where container_relation.p_id=product_entity.p_id and super_user_id = cart_entity.super_user_id group by super_user_id);

 update cart_entity
set t_price =0.00
where t_price is null;
--  5)
update user
set wallet = wallet -(select T_amount from transaction_entity where transaction_entity.transcation_id = 121 and transaction_entity.super_user_id  = 2)
where user_id = 2;

-- 6)
update product_entity
set Categories = "cloth" where p_id >= 1 and p_id <= 35;

update product_entity
 set Categories = "grocery" where p_id >= 36 and p_id <= 70;

 update product_entity
set Categories = "accessories" where p_id >= 71 and p_id <= 100;

select Categories,count(*) as product_type from product_entity group by Categories;

select * from product_entity where  Categories = "cloth" and quantity > 0 order by price desc;

update product_entity
set quantity = 0
where p_id%13 = 0;


select * from product_entity where  Categories = "cloth" and quantity > 0 order by price desc;

 -- 7)
select * from user,transaction_entity where area like "A%" and (state = "Berlin" or state = "Brandenburg")  and user_id = transaction_entity.super_user_id;

-- 8)
select p_name, Categories,Price from product_entity where product_entity.shop_id IN ( select shop.shop_id from order_relation,shop where order_relation.shop_id = shop.shop_id );


-- 9)
delete from user_phonenumber where user_id = 78 and  phone_number =  404902759;

-- 10)
select shop.shop_id , shop.shopname, t.user_id,t.username,t.house_no as user_house_no,t.area as user_area,t.state as user_state,t.pincode as user_pincode,t.license_id from shop ,(select * from user,delivery_unit_relation where user.user_id = delivery_unit_relation.super_user_id) as t where shop.shop_id = t.shop_id;

-- 11)

select * from ( select order_id,house_no,area,state, pincode,shop_id from delivery_unit_relation,user where user.user_id = delivery_unit_relation.super_user_id ) as t,(select order_id,order_status,datediff(date_of_delivery,date_of_order) as time_of_arrival from order_detail  ) as p where t.order_id = p.order_id and t.shop_id = 2 order by time_of_arrival ;


-- error on constraint

-- 12)
-- foreign key error
-- insert into user_phonenumber values(101,2323232); 


-- 13)
-- inserting wrong value
-- INSERT INTO `User` (`user_id`, `username`, `password`, `House_NO`, `area`, `state`, `PINCODE`, `WALLET`, `DOB`) VALUES (73, 'Milan', 'f64eab96', 989, 'Suite 553', 'Mecklenburg-Vorpomme', 55768, khkjh, '1985-03-11');
-- insert into  container_relation values(qw,86,59);

