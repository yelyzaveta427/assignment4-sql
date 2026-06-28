--запит, що виводить пасажирів, що витратили суму на квитки більшу ніж середня витрачена сума будь-якого пасажира в базі даних
explain analyze

select p.first_name, p.last_name, sum(t.price) as total
from passengers p
join tickets t on p.passenger_id = t.passenger_id
group by p.passenger_id, p.first_name, p.last_name
having sum(t.price) > (
    select avg(total)
    from (
        select sum(t1.price) as total
        from tickets t1
        group by t1.passenger_id
    ) as sub
);
--створення індексу на ід пасажира
create index idx_tickets_passenger_id on tickets(passenger_id);

explain analyze

--рахує суму, що витратив пасажир на квитки
with passenger_payment as (
    select p.passenger_id, p.first_name, p.last_name, sum(t.price) as total
    from passengers p
    join tickets t on p.passenger_id = t.passenger_id
    group by p.passenger_id, p.first_name, p.last_name
)
--виводить ту суму, що більша за середнє значення витраченої суми пасажирів
select first_name, last_name, total
from passenger_payment
where total > (select avg(total) from passenger_payment);



--створення функції, що рахує загальний прибуток від кафе та магазинів з конкретного терміналу
create or replace function get_profit_from_terminal(p_terminal_id int)
returns int as $$
declare v_cafes_profit int;
		v_shops_profit int;
		v_total int;
begin
	v_cafes_profit = (select coalesce(sum(revenue),0) from cafes where terminal_id = p_terminal_id);
	v_shops_profit = (select coalesce(sum(revenue),0) from shops where terminal_id = p_terminal_id);
	
	select v_cafes_profit + v_shops_profit into v_total;
	return v_total;
		
end;
$$ language plpgsql;

--перевірка окремо прибутку кафе та магазинів в конкретному терміналі
select terminal_id, sum(revenue) as cafes_sum from cafes group by terminal_id;
select terminal_id, sum(revenue) as shops_sum from shops group by terminal_id;

select get_profit_from_terminal(10) as total_terminal_profit;


--свторення знижки для певного рейсу
create or replace procedure create_ticket_discount(p_schedule_id int, p_discount int)
as $$
begin
	update tickets
	set price = price - p_discount where schedule_id = p_schedule_id and price > p_discount;
end;
$$ language plpgsql;

-- перевірка ціни квитків до знижки
select ticket_id, schedule_id, price from tickets where schedule_id = 1;
--використання знижки на рейс
call create_ticket_discount(1, 100);
select ticket_id, schedule_id, price from tickets where schedule_id = 1;






