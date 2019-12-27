create extension if not exists "uuid-ossp";

create table if not exists card (
	id uuid not null primary key default uuid_generate_v4(),
	card_number varchar(20),
	exp_month varchar(5),
	exp_year varchar(5),
	cvn varchar(5),
	created_at timestamp with time zone default current_timestamp,
	updated_at timestamp with time zone default current_timestamp
);