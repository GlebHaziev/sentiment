create table if not exists tcs_pulse_posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    post_id text null,
    user_id text null,
    user_name text null,
    likes integer null,
    comments integer null,
    inserted text null,
    instruments text null,
    hashtags text null,
    content text null,
    parse_dt text not null
);

create table if not exists tcs_pulse_users (
    id integer PRIMARY KEY AUTOINCREMENT,
    user_id text not null,
    nickname text null,
    followers int null,
    following int null,
    service_tags text null,
    month_operations_count int null,
    year_relative_yield numeric null,
    amount_from int null,
    amount_to int null,
    popular_hashtags text null,
    strategies text null,
    description text null,
    parse_dt not null
);


create table if not exists tcs_pulse_users_posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    post_id text not null,
    message text null,
    likes int null,
    comments int null,
    inserted text null,
    user_id text null,
    nickname text null,
    parse_dt text not null
)