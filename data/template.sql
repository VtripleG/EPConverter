CREATE TABLE IF NOT EXISTS "disciplines" (
  "id"  INTEGER NOT NULL UNIQUE,
  "code"  NUMERIC NOT NULL UNIQUE,
  "educational_program_id"  INTEGER,
  "name"  INTEGER,
  "department_code"  INTEGER,
  PRIMARY KEY("id" AUTOINCREMENT),
  FOREIGN KEY("educational_program_id") REFERENCES "educational_programs"("id")
);
CREATE TABLE IF NOT EXISTS "educational_programs" (
  "id"  INTEGER NOT NULL UNIQUE,
  "direction_code"  TEXT NOT NULL,
  "direction_name"  TEXT NOT NULL,
  "profile"  TEXT NOT NULL,
  "start_year"  INTEGER,
  "education_form"  TEXT,
  PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "competencies_guide" (
  "id"  INTEGER NOT NULL UNIQUE,
  "competence_code"  INTEGER NOT NULL,
  "educational_program_id"  INTEGER NOT NULL,
  FOREIGN KEY("educational_program_id") REFERENCES "educational_programs"("id"),
  PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "competencies_list" (
  "id"  INTEGER NOT NULL UNIQUE,
  "discipline_id"  INTEGER NOT NULL,
  "competence_guide_id"  INTEGER NOT NULL,
  "know"  TEXT,
  "can"  TEXT,
  "master"  TEXT,
  FOREIGN KEY("competence_guide_id") REFERENCES "competencies_guide"("id"),
  FOREIGN KEY("discipline_id") REFERENCES "disciplines"("id"),
  PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "laboriousness" (
  "id"  INTEGER NOT NULL UNIQUE,
  "descipline_id"  INTEGER NOT NULL,
  "semester_number"  INTEGER NOT NULL DEFAULT 0,
  "work_type"  TEXT,
  "hours_number"  INTEGER,
  FOREIGN KEY("descipline_id") REFERENCES "disciplines"("id"),
  PRIMARY KEY("id" AUTOINCREMENT)
);
