--виводить загальну кількість проданих квитків на певний рейс
create view ticket_count as
select 
	s.schedule_id,
	s.flight_id,
	s.departure_date,
	count(t.ticket_id) as sold_tickets
	from schedule_of_flights s 
	left join tickets t on s.schedule_id = t.schedule_id
	group by s.schedule_id, s.flight_id, s.departure_date;


select schedule_id, flight_id, departure_date, sold_tickets from ticket_count;