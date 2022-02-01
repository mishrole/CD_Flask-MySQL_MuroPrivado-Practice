Create database private_wall_schema;
Use private_wall_schema;

Create table users (
	id int primary key auto_increment,
    firstname varchar(45),
    lastname varchar(45),
    birthday date,
    gender varchar(100),
    email varchar(100),
    password text,
    created_at datetime,
    updated_at datetime,
    isBlocked boolean default false
);

Create table messages (
    id int primary key auto_increment,
    sender_id int not null,
    receiver_id int not null,
    message text,
    created_at datetime,
    updated_at datetime,
    isDeleted boolean default false,
    foreign key (sender_id) references users (id),
    foreign key (receiver_id) references users (id)
);

Create table reports (
    id int primary key auto_increment,
    user_id int not null,
    user_ip varchar(45),
    created_at datetime,
    updated_at datetime,
    foreign key (user_id) references users (id)
);
