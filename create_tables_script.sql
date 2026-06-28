create table aircrafts(
	aircraft_id varchar(10) primary key,
	model varchar(200) not null
);

create table airports(
	airport_id int primary key,
	airport_name varchar(100) not null,
	country varchar(100) not null,
	city varchar(100) not null
);

create table terminals(
	terminal_id int primary key,
	airport_id int not null,
	terminal_name varchar(10) not null,
	foreign key (airport_id) references airports(airport_id)
);

create table passengers(
	passenger_id int primary key,
	first_name varchar(30) not null,
	last_name varchar(30) not null 
);

create table passports_of_passengers(
	passenger_id int primary key,
	passport_number int not null,
	foreign key (passenger_id) references passengers(passenger_id)
	);

create table flights (
	flight_id int primary key,
	departure_airport int not null,
	arrival_airport int not null,
	foreign key (departure_airport) references airports(airport_id),
	foreign key (arrival_airport) references airports(airport_id)
);

create table schedule_of_flights(
	schedule_id int primary key,
	flight_id int not null,
	aircraft_id varchar(10) not null,
	departure_terminal_id int not null,
	arrival_terminal_id int not null,
	departure_date date not null,
	arrival_date date not null,
	status varchar(20) not null,
	foreign key (flight_id) references flights(flight_id),
	foreign key (aircraft_id) references aircrafts(aircraft_id),
	foreign key (departure_terminal_id) references terminals(terminal_id),
	foreign key (arrival_terminal_id) references terminals(terminal_id)
);

create table tickets(
	ticket_id int primary key,
	passenger_id int not null, 
	schedule_id int not null,
	class varchar(30) not null,
	price int not null,
	foreign key(schedule_id) references schedule_of_flights(schedule_id),
	foreign key(passenger_id) references passengers(passenger_id)
);

create table cafes(
cafe_id int primary key,
name_of_cafe varchar(50) not null,
food_type varchar(50) not null,
terminal_id int not null,
revenue int not null,
foreign key (terminal_id) references terminals(terminal_id)

);

create table shops(
shop_id int primary key,
name_of_shop varchar(50) not null,
type_of_shop varchar(50) not null,
terminal_id int not null,
revenue int not null,
foreign key (terminal_id) references terminals(terminal_id)
);

