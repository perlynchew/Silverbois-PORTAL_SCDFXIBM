CREATE TABLE scdf (
row_number SERIAL,
event_id VARCHAR,
event VARCHAR,
location VARCHAR,
description VARCHAR,
CFR VARCHAR,
status VARCHAR,
date_done timestamp without time zone,
result VARCHAR);

CREATE TABLE celery_tasksetmeta (
id INTEGER NOT NULL,
taskset_id VARCHAR(155),
result BYTEA,
date_done TIMESTAMP WITHOUT TIME ZONE,
PRIMARY KEY (id),
UNIQUE (taskset_id)
);

CREATE TABLE celery_taskmeta (
id INTEGER NOT NULL,
task_id VARCHAR(155),
status VARCHAR(50),
result BYTEA,
date_done TIMESTAMP WITHOUT TIME ZONE,
traceback TEXT,
name VARCHAR(155),
args BYTEA,
kwargs BYTEA,
worker VARCHAR(155),
retries INTEGER,
queue VARCHAR(155),
PRIMARY KEY (id),
UNIQUE (task_id)
);

CREATE SEQUENCE task_id_sequence START 1;

create or replace function send_message(channel text, message text) returns void as $$
	select pg_notify(channel, message);
$$ stable language sql;

create or replace function on_row_change() returns trigger as $$
  declare
    routing_key text;
    row record;
  begin
    routing_key := 'row_change'
                   '.table-'::text || TG_TABLE_NAME::text || 
                   '.event-'::text || TG_OP::text;
    if (TG_OP = 'DELETE') then
        row := old;
    elsif (TG_OP = 'UPDATE') then
        row := new;
    elsif (TG_OP = 'INSERT') then
        row := new;
    end if;
    perform send_message('pgchannel2', row_to_json(row)::text);
    return null;
  end;
$$ stable language plpgsql;

create trigger scdf_trigger
after insert on scdf
for each row execute procedure on_row_change();

CREATE OR REPLACE FUNCTION function_update() RETURNS TRIGGER AS
$BODY$
BEGIN
UPDATE scdf set status = celery_taskmeta.status, date_done = celery_taskmeta.date_done, result = celery_taskmeta.result FROM celery_taskmeta where scdf.event_id = celery_taskmeta.task_id;
RETURN new;
END;
$BODY$
language plpgsql;

CREATE TRIGGER update_status
AFTER INSERT OR UPDATE ON celery_taskmeta FOR EACH ROW EXECUTE PROCEDURE function_update();
