--головний директор, що має доступ до змінення усіх таблиць
create role airport_director with password 'slcnwciif';
grant select, insert, update on all tables in schema public to airport_director;

--персонал, що узгоджує інформацію про пасажира при проходженні ним перевірки
create role manager with password 'wdwqibneuyfgo';
grant select on all tables in schema public to manager;

--пасажир, що може лише дивитись на розклад рейсів і іншу інформацію в таблицях 
create role passenger with password 'asevae';
grant read_only to passenger;