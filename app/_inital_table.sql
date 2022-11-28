-- Create VCARD Table
CREATE TABLE IF NOT EXISTS vcard (
  ID INTEGER PRIMARY KEY,
  N_FIRST TEXT NOT NULL,
  N_LAST TEXT,
  N_ADD TEXT,
  N_PRE TEXT,
  N_SUF TEXT,
  NICKNAME TEXT,
  GENDER TEXT,
  ORG TEXT,
  ROLE TEXT,
  TITLE TEXT,
  EMAIL TEXT,
  URL TEXT,
  NOTE TEXT,
  ADR_HOME TEXT,
  ADR_WORK TEXT,
  TEL_WORK_CELL TEXT,
  TEL_WORK_VOICE TEXT,
  TEL_HOME_CELL TEXT,
  TEL_HOME_VOICE TEXT,
  CATEGORIES TEXT,
  BDAY TEXT,
  ANNIVERSARY TEXT,
  TZ TEXT,
  REV DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- inital data
INSERT INTO vcard(N_FIRST, N_LAST)
  VALUES
  ("John", "Doe"),
  ("Max", "Musterman");

-- add colum to table
-- ALTER TABLE customers ADD last_update_ts TIMESTAMP;

-- delete table
-- DROP TABLE addresses;

-- Direct shell exec:
-- sqlite3 app.db '.table'
-- sqlite3 app.db '.read _inital_table.sql'
-- sqlite3 app.db 'SELECT N_FIRST, N_LAST, EMAIL, REV FROM vcard;' -box
-- sqlite3 app.db 'SELECT * FROM vcard;' -box
-- sqlite3 app.db 'DROP TABLE vcard'
-- sqlite3 app.db 'SELECT ID, N_FIRST, N_LAST, ORG, EMAIL, TEL_WORK_VOICE, TITLE, NOTE FROM vcard WHERE id = 1;' -box
-- List all columns:
-- sqlite3 app.db 'PRAGMA table_info(vcard)' -box;
-- Add new column:
-- sqlite3 app.db 'ALTER TABLE vcard ADD COLUMN CATEGORIES TEXT';